# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Functions for downloading and caching sample datasets.
"""
import pathlib

import pooch


def fetch_brumadinho_after(untar=False):
    """
    Download a sample scene from after the Brumadinho tailings dam disaster

    This is a cropped version of a Landsat 8 scene from 2019/01/30. It was
    taken after the `Brumadinho tailings dam in Brazil
    <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__ collapsed,
    flooding a whole region.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.21665630
    (`CC0 <https://creativecommons.org/publicdomain/zero/1.0/>`__)

    Parameters
    ----------
    untar : bool
        If True, unpack the tar archive after downloading and return a path to
        the folder containing the unpacked files instead. Default is False.

    Returns
    -------
    path : str
        The path to the downloaded `.tar` file that contains the scene.
    """
    if untar:
        processor = pooch.Untar()
    else:
        processor = None
    path = pooch.retrieve(
        "https://figshare.com/ndownloader/files/38902290",
        fname="LC08_L2SP_218074_20190130_20200829_02_T1-cropped.tar.gz",
        known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
        processor=processor,
    )
    if untar:
        # Get the folder name in case we unpacked the archive
        path = pathlib.Path(path[0]).parent
    return path


def fetch_brumadinho_before(untar=False):
    """
    Download a sample scene from before the Brumadinho tailings dam disaster

    This is a cropped version of a Landsat 8 scene from 2019/01/14. It was
    taken before the `Brumadinho tailings dam in Brazil
    <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__ collapsed,
    flooding a whole region.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.21665630
    (`CC0 <https://creativecommons.org/publicdomain/zero/1.0/>`__)

    Parameters
    ----------
    untar : bool
        If True, unpack the tar archive after downloading and return a path to
        the folder containing the unpacked files instead. Default is False.

    Returns
    -------
    path : str
        The path to the downloaded `.tar` file that contains the scene.
    """
    if untar:
        processor = pooch.Untar()
    else:
        processor = None
    path = pooch.retrieve(
        "https://figshare.com/ndownloader/files/38902284",
        fname="LC08_L2SP_218074_20190114_20200829_02_T1-cropped.tar.gz",
        known_hash="md5:d2a503c944bb7ef3b41294d44b77e98c",
        processor=processor,
    )
    if untar:
        # Get the folder name in case we unpacked the archive
        path = pathlib.Path(path[0]).parent
    return path
