# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Interpolation methods for scenes.
"""
import numpy as np
import scipy as sp


def interpolate_missing(scene, pixel_radius=20, method="cubic"):
    """
    Fill missing values (NaNs) in a scene by cubic interpolation

    Each missing value is filled by interpolating the pixels within a
    neighboring region (controlled by ``pixel_radius``) using a piecewise cubic
    2D interpolator. Interpolation is done for each band in a scene separately.

    Note that this is mostly good if there are a few missing values, not large
    regions of the scene.

    Parameters
    ----------
    scene : :class:`xarray.Dataset`
        A Landsat scene, as read with :func:`xlandsat.load_scene`.
    pixel_radius : int
        Number of pixels to the east, west, south, and north of a missing value
        that will be used for interpolation. Smaller values make for faster
        interpolation but may lead to bad results if many missing values are
        grouped together.

    Returns
    -------
    filled_scene : :class:`xarray.Dataset`
        The scene with missing values filled in.
    """
    valid_methods = {"cubic": sp.interpolate.CloughTocher2DInterpolator, "nn": sp.interpolate.NearestNDInterpolator}
    if method not in valid_methods:
        raise ValueError(f"Invalid interpolation method '{method}. Must be one of: {tuple(valid_methods.keys())}")

    filled_scene = scene.copy(deep=True)
    rows, columns = np.meshgrid(
        np.arange(scene.northing.size),
        np.arange(scene.easting.size),
        indexing="ij",
    )
    for band in scene:
        values = filled_scene[band].values
        nans = np.isnan(values)
        for i, j in zip(rows[nans], columns[nans]):
            imin, imax = _search_range(i, pixel_radius, scene.northing.size)
            jmin, jmax = _search_range(j, pixel_radius, scene.easting.size)
            valid = ~np.isnan(values[imin:imax, jmin:jmax])
            interpolator = valid_methods[method](
                (
                    rows[imin:imax, jmin:jmax][valid],
                    columns[imin:imax, jmin:jmax][valid],
                ),
                values[imin:imax, jmin:jmax][valid],
            )
            values[i, j] = interpolator(i, j)
    return filled_scene


def _search_range(index, pixel_radius, dim_size):
    """
    Get a valid range around the index to search for interpolation data.
    Mostly used to avoid overflowing the image boundaries.
    """
    left, right = index - pixel_radius, index + pixel_radius
    if left < 0:
        left = 0
    if right > dim_size:
        right = dim_size
    return left, right
