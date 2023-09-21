# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Functions for downloading and caching sample datasets.
"""
import pathlib

import pooch

from ._version import __version__

POOCH = pooch.create(
    path=pooch.os_cache("xlandsat"),
    base_url="https://github.com/compgeolab/xlandsat/raw/{version}/data/",
    version=__version__,
    version_dev="main",
    registry={
        # Brumadinho - after
        "LC08_L2SP_218074_20190130_20200829_02_T1-cropped.tar.gz": "md5:4ae61a2d7a8b853c727c0c433680cece",
        # Brumadinho - before
        "LC08_L2SP_218074_20190114_20200829_02_T1-cropped.tar.gz": "md5:d2a503c944bb7ef3b41294d44b77e98c",
        # Liverpool
        "LC08_L2SP_204023_20200927_20201006_02_T1-cropped.tar.gz": "md5:3c07e343ccf959be4e5dd5c9aca4e0a4",
        # Liverpool - Panchromatic
        "LC08_L1TP_204023_20200927_20201006_02_T1-cropped.tar.gz": "md5:7d43f8580b8e583d137a93f9ae51a73d",
        # Momotombo
        "LC08_L2SP_017051_20151205_20200908_02_T1-cropped.tar.gz": "md5:8cc2e4c15e65940a7152fc1c8b412aa9",
        # Roraima
        "LC08_L2SP_232056_20151004_20200908_02_T1-cropped.tar.gz": "md5:f236a8b024aa4a4c62bee294d3bd737f",
        # Manaus
        "LC09_L2SP_231062_20230723_20230802_02_T1-cropped.tar.gz": "md5:ffe2003e665dc7a1a3155011f700a61d",
    },
)


def _fetch(fname, untar):
    """
    Fetch a file and handle untaring the archive if requested.
    """
    if untar:
        processor = pooch.Untar()
    else:
        processor = None
    path = POOCH.fetch(
        fname,
        processor=processor,
    )
    if untar:
        # Get the folder name in case we unpacked the archive
        path = pathlib.Path(path[0]).parent
    return path


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
    return _fetch("LC08_L2SP_218074_20190130_20200829_02_T1-cropped.tar.gz", untar)


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
    return _fetch(
        "LC08_L2SP_218074_20190114_20200829_02_T1-cropped.tar.gz",
        untar,
    )


def fetch_liverpool(untar=False):
    """
    Download a sample scene from the city of Liverpool, UK

    This is a cropped version of a Landsat 8 scene from 2020/09/27. It was
    taken on a virtually cloud-free day and shows the Mersey river delta and
    some off-shore wind turbines.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.22041353
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
    return _fetch(
        "LC08_L2SP_204023_20200927_20201006_02_T1-cropped.tar.gz",
        untar,
    )


def fetch_liverpool_panchromatic(untar=False):
    """
    Download a sample panchromatic band from the city of Liverpool, UK

    This is a cropped version of the panchromatic band from a Landsat 8 Level 1
    scene from 2020/09/27. It was taken on a virtually cloud-free day and shows
    the Mersey river delta and some off-shore wind turbines.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.22041353
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
    return _fetch(
        "LC08_L1TP_204023_20200927_20201006_02_T1-cropped.tar.gz",
        untar,
    )


def fetch_momotombo(untar=False):
    """
    Download a sample scene from the December 2015 Momotombo volcano eruption

    This is a cropped version of a Landsat 8 scene from 2015/12/05. It was
    taken during the December 2015 eruption of `Momotombo volcano
    <https://en.wikipedia.org/wiki/Momotombo>`__, Nicaragua.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.21931089.v3
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
    return _fetch(
        "LC08_L2SP_017051_20151205_20200908_02_T1-cropped.tar.gz",
        untar,
    )


def fetch_roraima(untar=False):
    """
    Download a sample scene from Mount Roraima surrounded by clouds

    Roraima is a *tepui* located in the junction of Brazil, Guyana, and
    Venezuela. It's famous for the near-constant cloud coverage.

    This is a cropped version of a Landsat 8 scene from 2015/10/04, which is
    one of the rare relatively cloud-free scenes available.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.24143622.v1
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
    return _fetch("LC08_L2SP_232056_20151004_20200908_02_T1-cropped.tar.gz", untar)


def fetch_manaus(untar=False):
    """
    Download a sample scene from Manaus, Brazil

    Manaus is located in the Brazilian Amazon. The scene shows a part of the
    city and the meeting of the Solimões and Negro rivers to form the Amazon
    river.

    This is a cropped version of a Landsat 9 scene from 2023/07/23, during
    the annual Amazon river floods.

    The scene was downloaded from `USGS Earth Explorer
    <https://earthexplorer.usgs.gov/>`__. Original data are in the public
    domain and are redistributed here in accordance with the `Landsat Data
    Distribution Policy
    <https://www.usgs.gov/media/files/landsat-data-distribution-policy>`__.

    Source: https://doi.org/10.6084/m9.figshare.24167235.v1
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
    return _fetch("LC09_L2SP_231062_20230723_20230802_02_T1-cropped.tar.gz", untar)
