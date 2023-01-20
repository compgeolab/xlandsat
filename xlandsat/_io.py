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

BAND_NAMES = {
    1: "coastal_aerosol",
    2: "blue",
    3: "green",
    4: "red",
    5: "nir",
    6: "swir1",
    7: "swir2",
    10: "thermal",
}
BAND_TITLES = {
    1: "coastal aerosol",
    2: "blue",
    3: "green",
    4: "red",
    5: "near-infrared",
    6: "short-wave infrared 1",
    7: "short-wave infrared 2",
    10: "thermal",
}
BAND_UNITS = {
    1: "reflectance",
    2: "reflectance",
    3: "reflectance",
    4: "reflectance",
    5: "reflectance",
    6: "reflectance",
    7: "reflectance",
    10: "Kelvin",
}


def load_scene(path, bands=None, region=None, dtype="float16"):
    """
    Load a Landsat scene downloaded from USGS EarthExplorer.

    Can read from a folder with ``*.TIF`` files and an ``*_MTL.txt`` file or
    directly from a tar archive (compressed or not) without the need to first
    unpack the archive. The bands are converted to reflectance/temperature
    units using appropriate scaling parameters and UTM coordinates are set in
    the returned :class:`xarray.Dataset`.

    .. important::

        Do not rename the TIF or MTL files. The folder/archive can have any
        name but TIF and MTL files need their original names.

    .. note::

        Only supports Landsat 8 and 9 Collection 2 Level 2 scenes.

    Parameters
    ----------
    path : str or :class:`pathlib.Path`
        The path to a folder or tar archive containing the files for a given
        scene. **Must** include the ``*_MTL.txt`` metadata file. Not all band
        files need to be present.
    bands : None or list
        List of band names to load. If None, will load all bands present in the
        folder/archive. See below for valid band names. Default is None.
    region : None or list
        Crop the scene to this bounding box given as a list of West, East,
        South, and North coordinate values (UTM in meters). If None, no
        cropping is performed on the scene. Default is None.
    dtype : str or numpy dtype object
        The type used for the band arrays. Integer types will result in
        rounding so floating point is recommended. Default is float16.

    Returns
    -------
    scene : :class:`xarray.Dataset`
        The loaded scene including UTM easting and northing as dimensional
        coordinates, bands as 2D arrays of the given type as variables, and
        metadata read from the MTL file and other CF compliant fields in the
        ``attrs`` attribute.

    Notes
    -----

    The valid band names for Landsat 8 and 9 are:

    ====== =====================
    Number         Name
    ====== =====================
    1      ``"coastal_aerosol"``
    2      ``"blue"``
    3      ``"green"``
    4      ``"red"``
    5      ``"nir"``
    6      ``"swir1"``
    7      ``"swir2"``
    10     ``"thermal"``
    ====== =====================

    """
    path = pathlib.Path(path)
    if bands is None:
        bands = BAND_NAMES.values()
    if path.is_file() and ".tar" in path.suffixes:
        reader_class = TarReader
    else:
        reader_class = FolderReader
    with reader_class(path) as reader:
        metadata = reader.read_metadata()
        available_bands = [int(str(f).split("_B")[-1][:-4]) for f in reader.band_files]
        scene_region = (
            metadata["corner_ll_projection_x_product"],
            metadata["corner_lr_projection_x_product"],
            metadata["corner_ll_projection_y_product"],
            metadata["corner_ul_projection_y_product"],
        )
        shape = (metadata["reflective_lines"], metadata["reflective_samples"])
        coords = {
            "easting": np.linspace(*scene_region[:2], shape[1]),
            "northing": np.linspace(*scene_region[2:], shape[0]),
        }
        data_vars = {}
        dims = ("northing", "easting")
        for number, fname in zip(available_bands, reader.band_files):
            if BAND_NAMES[number] not in bands:
                continue
            mult, add = None, None
            mult_entries = [f"mult_band_{number}", f"mult_band_st_b{number}"]
            add_entries = [f"add_band_{number}", f"add_band_st_b{number}"]
            for key in metadata:
                if any(key.endswith(entry) for entry in mult_entries):
                    mult = metadata[key]
                if any(key.endswith(entry) for entry in add_entries):
                    add = metadata[key]
            band = reader.read_band(fname).astype(dtype)[::-1, :]
            band[band == 0] = np.nan
            band *= mult
            band += add
            band_attrs = {
                "long_name": BAND_TITLES[number],
                "units": BAND_UNITS[number],
                "number": number,
                "filename": pathlib.Path(fname).name,
                "scaling_mult": mult,
                "scaling_add": add,
            }
            data_vars[BAND_NAMES[number]] = xr.DataArray(
                data=band,
                dims=dims,
                coords=coords,
                attrs=band_attrs,
                name=BAND_NAMES[number],
            )
            if region is not None:
                data_vars[BAND_NAMES[number]] = data_vars[BAND_NAMES[number]].sel(
                    easting=slice(*region[:2]), northing=slice(*region[2:])
                )
    attrs = {
        "Conventions": "CF-1.8",
        "title": (
            f"{metadata['spacecraft_id'].replace('_', ' ').title()} scene from "
            f"{metadata['date_acquired']} "
            f"(path/row={metadata['wrs_path']}/{metadata['wrs_row']})"
        ),
    }
    metadata_to_keep = [
        "digital_object_identifier",
        "origin",
        "landsat_product_id",
        "processing_level",
        "collection_number",
        "collection_category",
        "spacecraft_id",
        "sensor_id",
        "map_projection",
        "utm_zone",
        "datum",
        "ellipsoid",
        "date_acquired",
        "scene_center_time",
        "wrs_path",
        "wrs_row",
        "mtl_file",
    ]
    attrs.update({key: metadata[key] for key in metadata_to_keep})
    scene = xr.Dataset(data_vars, attrs=attrs)
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
    metadata["mtl_file"] = "\n".join(text)
    return metadata


class TarReader:
    """
    Context manager for reading metadata and bands from a tar archive.
    """

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        """
        Enter the context by opening the archive for reading.
        """
        self._archive = tarfile.open(self.path)
        self._members = [f.name for f in self._archive.getmembers()]
        self.metadata_files = [f for f in self._members if f.endswith("MTL.txt")]
        self.band_files = sorted(
            [f for f in self._members if re.search(r".*_B[0-9]+.TIF", f) is not None]
        )
        return self

    def read_metadata(self):
        """
        Return a list of lines read from the metadata file.
        """
        _check_metadata(self.metadata_files, self.path)
        with io.TextIOWrapper(
            self._archive.extractfile(self.metadata_files[0])
        ) as fobj:
            metadata = parse_metadata(fobj.read().split("\n"))
        return metadata

    def read_band(self, fname):
        """
        Read a band file using scikit-image.
        """
        with self._archive.extractfile(fname) as fobj:
            band = skimage.io.imread(fobj)
        return band

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: U100
        """
        Clean up the context by closing the archive.
        """
        self._archive.close()


class FolderReader:
    """
    Context manager for reading metadata and bands from a local folder.
    """

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        """
        Enter the context by grabbing a list of files.
        """
        self.metadata_files = list(self.path.glob("*_MTL.txt"))
        self.band_files = sorted(self.path.glob("*_B*.TIF"))
        return self

    def read_metadata(self):
        """
        Return a list of lines read from the metadata file.
        """
        _check_metadata(self.metadata_files, self.path)
        metadata = parse_metadata(self.metadata_files[0].read_text().split("\n"))
        return metadata

    def read_band(self, fname):
        """
        Read a band file using scikit-image.
        """
        band = skimage.io.imread(fname)
        return band

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: U100
        """
        No clean up needed for this context.
        """
        pass


def _check_metadata(files, path):
    """
    Check the number of metadata files found and raise appropriate exceptions.
    """
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


def save_scene(path, scene):
    """
    Save a Landsat scene to a tar archive in the USGS EarthExplorer format.

    Requires the scene to be in the format returned by
    :func:`~xlandsat.load_scene`, including all of the original metadata.

    The tar archive will contain the bands saved as ``*.TIF`` files in unscaled
    16-bit unsigned-integers. The metadata is saved to a corresponding
    ``*_MTL.txt`` file. If the scene was cropped, the file metadata will be
    adjusted to reflect the new UTM bounding box. The lat/lon bounding box
    **will not be updated**.

    .. tip::

        **Do not use this function** as a general output format for the scene
        unless you require compatibility with EarthExplorer. The best way to
        save a scene is with :meth:`xarray.Dataset.to_netcdf` since it will
        result in a single file with all metadata preserved. To load the saved
        scene, use :func:`xarray.load_dataset`. NetCDF files can also be loaded
        lazily with :func:`xarray.open_dataset` to avoid loading the entire
        scene into memory.

    .. note::

        Only supports Landsat 8 and 9 Collection 2 Level 2 scenes.

    Parameters
    ----------
    path : str or :class:`pathlib.Path`
        The desired path of the output tar archive. The file extension can be
        ``.tar`` (uncompressed) or ``.tar.gz``, ``.tar.xz``, or ``.tar.bz2`` to
        make a compressed archive.
    scene : :class:`xarray.Dataset`
        The scene including UTM easting and northing as dimensional
        coordinates, bands as 2D arrays of the given type as variables, and
        metadata read from the MTL file and other CF compliant fields in the
        ``attrs`` attribute.
    """
    path = pathlib.Path(path)
    mode = "w"
    if len(path.suffixes) > 1:
        mode = f"{mode}:{path.suffixes[-1][1:]}"
    with tarfile.open(path, mode=mode) as archive:
        # Edit the bounding box of the scene
        # NOTE: the lat/lon information will be wrong. Fixing it would mean
        # adding a pyproj dependency
        mtl_file_original = scene.attrs["mtl_file"].split("\n")
        mtl_file = []
        for line in mtl_file_original:
            if (
                "CORNER_UL_PROJECTION_X_PRODUCT" in line
                or "CORNER_LL_PROJECTION_X_PRODUCT" in line
            ):
                line = line.split(" = ")[0] + f" = {scene.easting.min().values}"
            if (
                "CORNER_UR_PROJECTION_X_PRODUCT" in line
                or "CORNER_LR_PROJECTION_X_PRODUCT" in line
            ):
                line = line.split(" = ")[0] + f" = {scene.easting.max().values}"
            if (
                "CORNER_LL_PROJECTION_Y_PRODUCT" in line
                or "CORNER_LR_PROJECTION_Y_PRODUCT" in line
            ):
                line = line.split(" = ")[0] + f" = {scene.northing.min().values}"
            if (
                "CORNER_UL_PROJECTION_Y_PRODUCT" in line
                or "CORNER_UR_PROJECTION_Y_PRODUCT" in line
            ):
                line = line.split(" = ")[0] + f" = {scene.northing.max().values}"
            if "REFLECTIVE_LINES" in line or "THERMAL_LINES" in line:
                line = line.split(" = ")[0] + f" = {scene.dims['northing']}"
            if "REFLECTIVE_SAMPLES" in line or "THERMAL_SAMPLES" in line:
                line = line.split(" = ")[0] + f" = {scene.dims['easting']}"
            mtl_file.append(line)
        mtl_file = "\n".join(mtl_file)
        # Add the MTL file to the archive
        info = tarfile.TarInfo(f"{scene.attrs['landsat_product_id']}_MTL.txt")
        info.size = len(mtl_file.encode())
        archive.addfile(info, fileobj=io.BytesIO(mtl_file.encode()))
        # Add the scenes to the archive
        for name in scene:
            band = scene[name]
            unscaled = (band.values - band.attrs["scaling_add"]) / band.attrs[
                "scaling_mult"
            ]
            unscaled[np.isnan(unscaled)] = 0
            file = io.BytesIO()
            skimage.io.imsave(
                file,
                unscaled.astype("uint16")[::-1, :],
                format=".tif",
            )
            info = tarfile.TarInfo(band.attrs["filename"])
            info.size = file.getbuffer().nbytes
            archive.addfile(info, fileobj=io.BytesIO(file.getbuffer()))
