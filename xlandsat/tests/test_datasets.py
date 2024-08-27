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
    fetch_corumba_after,
    fetch_corumba_before,
    fetch_liverpool,
    fetch_liverpool_panchromatic,
    fetch_manaus,
    fetch_momotombo,
    fetch_roraima,
)


@pytest.mark.parametrize("untar", [False, True], ids=["archive", "folder"])
@pytest.mark.parametrize(
    "fetcher",
    [
        fetch_brumadinho_after,
        fetch_brumadinho_before,
        fetch_corumba_after,
        fetch_corumba_before,
        fetch_liverpool,
        fetch_liverpool_panchromatic,
        fetch_manaus,
        fetch_roraima,
    ],
)
def test_fetching_functions(untar, fetcher):
    "Check that the download functions work"
    path = pathlib.Path(fetcher(untar=untar))
    assert path.exists()
    if untar:
        assert path.is_dir()
    else:
        assert not path.is_dir()


@pytest.mark.parametrize("untar", [False, True], ids=["archive", "folder"])
@pytest.mark.parametrize("level", [1, 2], ids=["L1", "L2"])
@pytest.mark.parametrize(
    "fetcher",
    [
        fetch_momotombo,
    ],
)
def test_fetching_functions_levels(untar, level, fetcher):
    "Check that the download functions work"
    path = pathlib.Path(fetcher(untar=untar, level=level))
    assert path.exists()
    if untar:
        assert path.is_dir()
    else:
        assert not path.is_dir()
