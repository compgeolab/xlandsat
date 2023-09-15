# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Test the download functions
"""
import pathlib

import pytest

from ..datasets import (
    fetch_brumadinho_after,
    fetch_brumadinho_before,
    fetch_liverpool,
    fetch_liverpool_panchromatic,
    fetch_momotombo,
    fetch_roraima,
)


@pytest.mark.parametrize("untar", [False, True], ids=["archive", "folder"])
def test_fetching_functions(untar):
    "Check that the download functions work"
    functions = [
        fetch_brumadinho_after,
        fetch_brumadinho_before,
        fetch_liverpool,
        fetch_liverpool_panchromatic,
        fetch_momotombo,
        fetch_roraima,
    ]
    for func in functions:
        path = pathlib.Path(func(untar=untar))
        assert path.exists()
        if untar:
            assert path.is_dir()
        else:
            assert not path.is_dir()
