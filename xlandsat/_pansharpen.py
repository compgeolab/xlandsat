# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Pansharpening methods.
"""


def pansharpen(scene, panchromatic, weights=(1, 1, 0.2)):
    """
    Pansharpen the red, green, and blue bands of a scene.

    The pansharpened scene will have the same coordinate values of the given
    panchromatic band. Uses a weighted version of the Brovey Transform
    [Pohl_and_VanGenderen1998]_ to account for the smaller blue footprint in
    Landsat 8/9 panchromatic band, following
    https://github.com/mapbox/rio-pansharpen (MIT license).

    Parameters
    ----------
    scene : :class:`xarray.Dataset`
        A Landsat scene, as read with :func:`xlandsat.load_scene`. The scene
        must contain the red, green, and blue bands. Other bands are ignored.
    panchromatic : :class:`xarray.DataArray`
        A Landsat panchromatic band, as read with
        :func:`xlandsat.load_panchromatic`.
    weights : tuple
        The weights applied to the red, green, and blue bands, respectively.

    Returns
    -------
    scene_sharpened : :class:`xarray.Dataset`
        The pandsharpened scene including the red, green, and blue bands only.
        Metadata from the original scene is copied into the pandsharpened
        version.
    """
    bands = ["red", "green", "blue"]
    sharp = scene[bands].interp_like(panchromatic, method="nearest", kwargs={"fill_value": "extrapolate"})
    band_average = sum(sharp[band] * weight for band, weight in zip(bands, weights)) / sum(weights)
    sharp *= panchromatic
    sharp /= band_average
    sharp.attrs = {key: value for key, value in scene.attrs.items() if key not in ("mtl_file")}
    sharp.attrs["title"] = f"Pansharpend {scene.attrs['title']}"
    sharp.attrs["pansharpening_method"] = "Weighted Brovey Transform"
    sharp.attrs["pansharpening_rgb_weights"] = weights
    sharp.attrs["pansharpening_band_filename"] = panchromatic.attrs["filename"]
    for band in sharp:
        sharp[band].attrs = scene[band].attrs
    return sharp
