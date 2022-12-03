# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Test the main IO functionality
"""
import pooch

from .._read import load_scene


def test_load_scene_minimal():
    "Minimal check that things don't crash."
    path = pooch.retrieve(
        "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    scene = load_scene(path)
    assert scene.attrs["title"] == "Landsat 8 scene from 2019-01-30 (path/row=218/74)"
