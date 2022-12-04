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

    The composite will be an RGBA array if NaNs are present in any band (with
    transparency of the NaN pixels set to full), or RGB is no NaNs are present.
    The RGB(A) array is encoded as unsigned 8-bit integers for easier plotting
    with matplotlib and smaller memory footprint.

    Optionally rescale each band to the given range for improved contrast.

    Parameters
    ----------
    scene : :class:`xarray.Dataset`
        A Landsat scene, as read with :func:`xlandsat.load_scene`.
    bands : list of str
        A list of variable names from the scene that will be used as the
        composite's red, green, and blue channels, respectively.
    rescale_to : None or list
        If not None, then should be a list/tuple with the minimum and maximum
        reflectance ranges to use for rescaling. The same values are used for
        each band. Bands are rescaled separately. Example: ``rescale_to=[0,
        0.5]``. Default is None.

    Returns
    -------
    composite : :class:`xarray.DataArray`
        The composite as a 3D ``DataArray`` of type uint8. The first 2
        dimensions are the same as the scene with the ``"channel"`` added as
        third dimension. Metadata from the scene is copied to the composite.

    Notes
    -----

    .. tip::

        Use the :meth:`xarray.DataArray.plot.imshow` method to plot the
        composite using matplotlib.

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
