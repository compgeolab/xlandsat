# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Calculate indices based on data in xarray.Datasets
"""


def ndvi(scene, red_band="red", nir_band="nir"):
    r"""
    Normalized Difference Vegetation Index

    Calculate the NDVI for the given scene, defined as:

    .. math::

        NDVI = \dfrac{NIR - Red}{NIR + Red}

    Parameters
    ----------
    scene : :class:`xarray.Dataset`
        A Landsat scene, as read with :func:`xlandsat.load_scene`.
    red_band : str
        The name of the variable in ``scene`` that corresponds to the red band.
    nir_band : str
        The name of the variable in ``scene`` that corresponds to the NIR band.

    Returns
    -------
    ndvi : :class:`xarray.DataArray`
        The calculated NDVI, with the metadata attributes from the original
        scene.
    """
    red = scene[red_band]
    nir = scene[nir_band]
    result = (nir - red) / (nir + red)
    result.name = "ndvi"
    attrs = {"long_name": "normalized difference vegetation index"}
    attrs.update(scene.attrs)
    result = result.assign_attrs(attrs)
    return result
