# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Generate and manipulate composites.
"""
import numpy as np
import skimage.exposure
import xarray as xr


def composite(scene, bands=("red", "green", "blue"), rescale_to=None):
    """
    Create a composite using the given bands.
    """
    nrows, ncols = scene[bands[0]].shape
    if np.any((np.isnan(scene[b]) for b in bands)):
        ndim = 4
    else:
        ndim = 3
    composite = np.empty((nrows, ncols, ndim), dtype="uint8")
    for i, band in enumerate(bands):
        if rescale_to is None:
            in_range = (np.nanmin(scene[band].values), np.nanmax(scene[band].values))
        else:
            in_range = tuple(rescale_to)
        composite[:, :, i] = skimage.exposure.rescale_intensity(
            scene[band].values,
            out_range="uint8",
            in_range=in_range,
        )
    if ndim == 4:
        composite[:, :, 3] = np.where(
            np.any([np.isnan(scene[b]) for b in bands], axis=0),
            0,
            255,
        )
    long_name = (
        ", ".join(f"{scene[b].attrs['long_name']}" for b in bands) + " composite"
    )
    name = f"composite_{'_'.join(bands)}"
    coordinates = {"channel": ["red", "green", "blue", "alpha"][:ndim]}
    coordinates.update(scene.coords)
    attrs = {"long_name": long_name}
    attrs.update(scene.attrs)
    composite = xr.DataArray(
        data=composite,
        dims=(scene[bands[0]].dims[0], scene[bands[0]].dims[1], "channel"),
        coords=coordinates,
        attrs=attrs,
        name=name,
    )
    return composite
