# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Test the main IO functionality
"""
import pathlib
import shutil
import tempfile

import pooch
import pytest

from .._read import load_scene


def test_load_scene_archive():
    "Check basic things about loading a scene from a tar archive"
    path = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    scene = load_scene(path)
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    assert set(scene.data_vars) == set(
        ["red", "green", "blue", "nir", "swir1", "swir2"]
    )
    assert scene.red.shape == (300, 400)


def test_load_scene_folder():
    "Check basic things about loading a scene from a folder"
    paths = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
        processor=pooch.Untar(),
    )
    # Unpack the archive and get the folder name
    path = pathlib.Path(paths[0]).parent
    assert path.is_dir()
    scene = load_scene(path)
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    bands = ["red", "green", "blue", "nir", "swir1", "swir2"]
    assert set(scene.data_vars) == set(bands)
    assert all(scene[band].shape == (300, 400) for band in bands)


def test_load_scene_crop():
    "Check that loading only a portion of a scene works"
    path = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    region = [584400, 596070, -2231670, -2223000]
    scene = load_scene(path, region=region)
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    bands = ["red", "green", "blue", "nir", "swir1", "swir2"]
    assert set(scene.data_vars) == set(bands)
    assert scene.easting.min() == region[0]
    assert scene.easting.max() == region[1]
    assert scene.northing.min() == region[2]
    assert scene.northing.max() == region[3]
    assert all(scene[band].shape == (290, 390) for band in bands)


def test_load_scene_select_bands():
    "Check that loading only a few selected bands works"
    path = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    scene = load_scene(path, bands=["red", "swir1"])
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    assert set(scene.data_vars) == set(["red", "swir1"])
    assert scene.red.shape == (300, 400)


def test_load_scene_fail_multiple_mtl_files():
    "Check that loading fails when there are multiple MTL.txt files"
    paths = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
        processor=pooch.Untar(),
    )
    # Unpack the archive and get the folder name
    path = pathlib.Path(paths[0]).parent
    assert path.is_dir()
    # Find the name of the MTL file
    mtl = list(path.glob("*_MTL.txt"))
    assert len(mtl) == 1
    mtl = mtl[0].name
    # Duplicate the scene into a temporary folder and add an extra file
    with tempfile.TemporaryDirectory() as tmpdir:
        duplicate = pathlib.Path(tmpdir) / "duplicate_scene"
        shutil.copytree(path, duplicate)
        shutil.copy(pathlib.Path(path) / mtl, duplicate / ("copy_" + mtl))
        with pytest.raises(ValueError) as error:
            load_scene(duplicate)
        assert "Found 2" in str(error)


def test_load_scene_fail_missing_mtl_file():
    "Check that loading fails when there is no MTL.txt file"
    paths = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
        processor=pooch.Untar(),
    )
    # Unpack the archive and get the folder name
    path = pathlib.Path(paths[0]).parent
    assert path.is_dir()
    # Duplicate the scene into a temporary folder and add an extra file
    with tempfile.TemporaryDirectory() as tmpdir:
        duplicate = pathlib.Path(tmpdir) / "duplicate_scene"
        shutil.copytree(path, duplicate)
        # Delete the MTL tiles
        for mtl_file in duplicate.glob("*_MTL.txt"):
            mtl_file.unlink()
        assert not list(duplicate.glob("*_MTL.txt"))
        with pytest.raises(ValueError) as error:
            load_scene(duplicate)
        assert "Couldn't find" in str(error)
