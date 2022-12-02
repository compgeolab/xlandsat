import skimage.exposure
import matplotlib.pyplot as plt
import numpy as np


def plot_composite(scene, bands=("red", "green", "blue"), ax=None, rescale_to=None):
    """
    Create a plot a composite using the given bands.
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
    if ax is None:
        plt.figure()
        ax = plt.subplot(111)
        ax.set_xlabel(
            f"{scene.easting.attrs['long_name']} [{scene.easting.attrs['units']}]"
        )
        ax.set_ylabel(
            f"{scene.northing.attrs['long_name']} [{scene.northing.attrs['units']}]"
        )
        composite_name = ", ".join(f"{scene[b].attrs['long_name']}" for b in bands)
        ax.set_title(
            f"{scene.attrs['title']}\nComposite: {composite_name}", linespacing=1.75
        )
    region = (
        scene.easting.min(),
        scene.easting.max(),
        scene.northing.min(),
        scene.northing.max(),
    )
    ax.imshow(composite, extent=region)
    return ax
