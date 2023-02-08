# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Test the main IO functionality
"""
import pathlib
import shutil
import tempfile

import numpy.testing as npt
import pytest

from .._io import load_scene, save_scene
from ..datasets import fetch_brumadinho_after


@pytest.mark.parametrize("compression", ["", ".gz"], ids=["none", "gz"])
def test_save_scene_round_trip(compression):
    "Save a scene and load it back again to check if the round trip works"
    path = fetch_brumadinho_after()
    scene_original = load_scene(path, dtype="float32")
    with tempfile.TemporaryDirectory() as tmpdir:
        path_copy = pathlib.Path(tmpdir) / f"scene-copy.tar{compression}"
        save_scene(path_copy, scene_original)
        scene = load_scene(path_copy, dtype="float32")
        assert (
            scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
        )
        assert set(scene.data_vars) == set(
            ["red", "green", "blue", "nir", "swir1", "swir2"]
        )
        assert scene.red.shape == (300, 400)
        npt.assert_allclose(
            scene.red.values, scene_original.red.values, rtol=0, atol=1e-4
        )
        npt.assert_allclose(
            scene.easting.values, scene_original.easting.values, rtol=0, atol=1e-4
        )
        npt.assert_allclose(
            scene.northing.values, scene_original.northing.values, rtol=0, atol=1e-4
        )


@pytest.mark.parametrize("compression", ["", ".gz"], ids=["none", "gz"])
def test_save_scene_cropped(compression):
    "Save a cropped scene and load it back again to check"
    path = fetch_brumadinho_after()
    scene_original = load_scene(path, dtype="float32").sel(
        northing=slice(-2.226e6, -2.224e6), easting=slice(5.9e5, 5.92e5)
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        path_copy = pathlib.Path(tmpdir) / f"scene-copy.tar{compression}"
        save_scene(path_copy, scene_original)
        scene = load_scene(path_copy, dtype="float32")
        assert (
            scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
        )
        assert set(scene.data_vars) == set(
            ["red", "green", "blue", "nir", "swir1", "swir2"]
        )
        assert scene.red.shape == scene_original.red.shape
        npt.assert_allclose(
            scene.red.values, scene_original.red.values, rtol=0, atol=1e-4
        )
        npt.assert_allclose(
            scene.easting.values, scene_original.easting.values, rtol=0, atol=1e-4
        )
        npt.assert_allclose(
            scene.northing.values, scene_original.northing.values, rtol=0, atol=1e-4
        )


def test_load_scene_archive():
    "Check basic things about loading a scene from a tar archive"
    path = fetch_brumadinho_after()
    scene = load_scene(path)
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    assert set(scene.data_vars) == set(
        ["red", "green", "blue", "nir", "swir1", "swir2"]
    )
    assert scene.red.shape == (300, 400)


def test_load_scene_folder():
    "Check basic things about loading a scene from a folder"
    path = fetch_brumadinho_after(untar=True)
    assert path.is_dir()
    scene = load_scene(path)
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    bands = ["red", "green", "blue", "nir", "swir1", "swir2"]
    assert set(scene.data_vars) == set(bands)
    assert all(scene[band].shape == (300, 400) for band in bands)


def test_load_scene_crop():
    "Check that loading only a portion of a scene works"
    path = fetch_brumadinho_after()
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
    path = fetch_brumadinho_after()
    scene = load_scene(path, bands=["red", "swir1"])
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
    assert set(scene.data_vars) == set(["red", "swir1"])
    assert scene.red.shape == (300, 400)


def test_load_scene_fail_multiple_mtl_files():
    "Check that loading fails when there are multiple MTL.txt files"
    path = fetch_brumadinho_after(untar=True)
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
    path = fetch_brumadinho_after(untar=True)
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
