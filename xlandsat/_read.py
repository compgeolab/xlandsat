# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Main I/O functions for loading the scenes into xarray.
"""
import io
import pathlib
import re
import tarfile

import numpy as np
import skimage.io
import xarray as xr


def load_scene(path, dtype="float32"):
    """
    Load a Landsat scene downloaded from EarthExplorer.
    """
    path = pathlib.Path(path)
    if path.is_file() and ".tar" in path.suffixes:
        reader_class = TarReader
    else:
        reader_class = FolderReader
    with reader_class(path) as reader:
        metadata = reader.read_metadata()
        region = (
            metadata["corner_ll_projection_x_product"],
            metadata["corner_lr_projection_x_product"],
            metadata["corner_ll_projection_y_product"],
            metadata["corner_ul_projection_y_product"],
        )
        shape = (metadata["reflective_lines"], metadata["reflective_samples"])
        band_names = {
            1: "coastal_aerosol",
            2: "blue",
            3: "green",
            4: "red",
            5: "nir",
            6: "swir1",
            7: "swir2",
            10: "thermal",
        }
        band_titles = {
            1: "coastal aerosol",
            2: "blue",
            3: "green",
            4: "red",
            5: "near-infrared",
            6: "short-wave infrared 1",
            7: "short-wave infrared 2",
            10: "thermal",
        }
        band_units = {
            1: "reflectance",
            2: "reflectance",
            3: "reflectance",
            4: "reflectance",
            5: "reflectance",
            6: "reflectance",
            7: "reflectance",
            10: "Kelvin",
        }
        band_numbers = [int(str(f).split("_B")[-1][:-4]) for f in reader.band_files]
        data_vars = {}
        dims = ("northing", "easting")
        for number, fname in zip(band_numbers, reader.band_files):
            band_attrs = {
                "long_name": band_titles[number],
                "units": band_units[number],
            }
            mult, add = None, None
            mult_entries = [f"mult_band_{number}", f"mult_band_st_b{number}"]
            add_entries = [f"add_band_{number}", f"add_band_st_b{number}"]
            for key in metadata:
                if any(key.endswith(entry) for entry in mult_entries):
                    mult = metadata[key]
                if any(key.endswith(entry) for entry in add_entries):
                    add = metadata[key]
            band = reader.read_band(fname).astype(dtype)
            band[band == 0] = np.nan
            band *= mult
            band += add
            data_vars[band_names[number]] = (dims, band, band_attrs)
    attrs = {
        "Conventions": "CF-1.8",
        "title": (
            f"{metadata['spacecraft_id'].replace('_', ' ').title()} scene from "
            f"{metadata['date_acquired']} "
            f"(path/row={metadata['wrs_path']}/{metadata['wrs_row']})"
        ),
    }
    attrs.update(metadata)
    scene = xr.Dataset(
        data_vars,
        coords={
            "easting": np.linspace(*region[:2], shape[1]),
            "northing": np.linspace(*region[2:], shape[0])[::-1],
        },
        attrs=attrs,
    )
    scene.easting.attrs = {
        "long_name": "UTM easting",
        "standard_name": "projection_x_coordinate",
        "units": "m",
    }
    scene.northing.attrs = {
        "long_name": "UTM northing",
        "standard_name": "projection_y_coordinate",
        "units": "m",
    }
    return scene


def parse_metadata(text):
    """
    Parse key metadata from ``*_MTL.txt`` files into a dictionary.
    """
    metadata_raw = [line.strip() for line in text]
    metadata = {}
    text_data = [
        "DIGITAL_OBJECT_IDENTIFIER",
        "ORIGIN",
        "LANDSAT_PRODUCT_ID",
        "PROCESSING_LEVEL",
        "COLLECTION_NUMBER",
        "COLLECTION_CATEGORY",
        "SPACECRAFT_ID",
        "SENSOR_ID",
        "MAP_PROJECTION",
        "DATUM",
        "ELLIPSOID",
        "DATE_ACQUIRED",
        "SCENE_CENTER_TIME",
    ]
    int_data = [
        "WRS_PATH",
        "WRS_ROW",
        "UTM_ZONE",
        "REFLECTIVE_LINES",
        "REFLECTIVE_SAMPLES",
        "THERMAL_LINES",
        "THERMAL_SAMPLES",
    ]
    float_data = [
        "ROLL_ANGLE",
        "SUN_AZIMUTH",
        "SUN_ELEVATION",
        "EARTH_SUN_DISTANCE",
        "CORNER_",
        "REFLECTANCE_MULT_BAND_",
        "REFLECTANCE_ADD_BAND_",
        "TEMPERATURE_MULT_BAND_",
        "TEMPERATURE_ADD_BAND_",
    ]
    for item in metadata_raw:
        for field in text_data:
            if item.startswith(field) and field.lower() not in metadata:
                metadata[field.lower()] = item.split(" = ")[-1].replace('"', "")
                break
        for field in int_data:
            if item.startswith(field) and field.lower() not in metadata:
                metadata[field.lower()] = int(item.split(" = ")[-1])
                break
        for field in float_data:
            if item.startswith(field) and field.lower() not in metadata:
                name, value = item.split(" = ")
                metadata[name.lower()] = float(value)
                break
    return metadata


class TarReader:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self._archive = tarfile.open(self.path)
        self._members = [f.name for f in self._archive.getmembers()]
        self.metadata_files = [f for f in self._members if f.endswith("MTL.txt")]
        self.band_files = sorted(
            [f for f in self._members if re.search(r".*_B[0-9]+.TIF", f) is not None]
        )
        return self

    def read_metadata(self):
        _check_metadata(self.metadata_files, self.path)
        with io.TextIOWrapper(
            self._archive.extractfile(self.metadata_files[0])
        ) as fobj:
            metadata = parse_metadata(fobj.readlines())
        return metadata

    def read_band(self, fname):
        with self._archive.extractfile(fname) as fobj:
            band = skimage.io.imread(fobj)
        return band

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: U100
        self._archive.close()


class FolderReader:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.metadata_files = list(self.path.glob("*_MTL.txt"))
        self.band_files = sorted(self.path.glob("*_B*.TIF"))
        return self

    def read_metadata(self):
        _check_metadata(self.metadata_files, self.path)
        metadata = parse_metadata(self.metadata_files[0].read_text().split("\n"))
        return metadata

    def read_band(self, fname):
        band = skimage.io.imread(fname)
        return band

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: U100
        pass


def _check_metadata(files, path):
    if len(files) > 1:
        raise ValueError(
            f"Found {len(files)} '*_MTL.txt' files in {str(path)}. "
            "Only file per folder/scene is supported."
        )
    elif len(files) < 1:
        raise ValueError(
            f"Couldn't find an '*_MTL.txt' file in {str(path)}. "
            "Download the corresponding file for this scene so we can read "
            "the metadata."
        )
