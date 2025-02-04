.. _indices:

Working with indices
--------------------

Indices calculated from multispectral satellite imagery are powerful ways to
quantitatively analyze these data.
They take advantage of different spectral properties of materials to
differentiate between them.
Many of these indices can be calculated with simple arithmetic operations.
So now that our data are in :class:`xarray.Dataset`'s, it's fairly easy to
calculate them.
Some commonly used indices are provided as functions in :mod:`xlandsat` but
any other index can be calculated using the power of :mod:`xarray`.

Here, we'll see some examples of indices that can be calculated.
First, we must import the required packages for the examples below.

.. jupyter-execute::

    import xlandsat as xls
    import matplotlib.pyplot as plt
    import numpy as np

NDVI
----

As an example, we'll use two scenes from before and after the
`Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__
to try to image and quantify the total area flooded by the damn collapse using
`NDVI <https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index>`__,
which is available in :func:`xlandsat.ndvi`.

.. admonition:: Trigger warning
    :class: warning

    This tutorial uses data from the tragic
    `Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__,
    in which over 250 people lost their lives. We use this dataset to
    illustrate the usefulness of remote sensing data for monitoring such
    disasters but we want to acknowledge its tragic human consequences.
    **Some readers may find this topic disturbing and may not wish to read
    futher.**

First, we must download the sample data and load the two scenes with
:func:`xlandsat.load_scene`:

.. jupyter-execute::

    path_before = xls.datasets.fetch_brumadinho_before()
    path_after = xls.datasets.fetch_brumadinho_after()
    before = xls.load_scene(path_before)
    after = xls.load_scene(path_after)
    after

Let's make RGB composites to get a sense of what these two scenes contain:

.. jupyter-execute::

    rgb_before = xls.composite(before, rescale_to=(0.03, 0.2))
    rgb_after = xls.composite(after, rescale_to=(0.03, 0.2))

    fig, axes = plt.subplots(2, 1, figsize=(10, 12), layout="tight")
    for ax, rgb in zip(axes, [rgb_before, rgb_after]):
        rgb.plot.imshow(ax=ax)
        ax.set_title(rgb.attrs["title"])
        ax.set_aspect("equal")
    plt.show()

The dam is located at around 592000 east and -2225000 north. The after scene
clearly shows all of the red mud that flooded the region to the southwest of
the dam. Notice also the red tinge of the Paraopeba River in the after image
as it was contaminated by the mud flow.

.. tip::

     See :ref:`composites` for more information on what we did above.

We can calculate the NDVI for these scenes to see if we can isolate the effect
of the flood following the dam collapse.
NDVI highlights vegetation, which we assume will have decreased in the after
scene due to the flood.
Calculating the NDVI is as simple as calling :func:`xlandsat.ndvi` with the
scene as an argument:

.. jupyter-execute::

    ndvi_before = xls.ndvi(before)
    ndvi_after = xls.ndvi(after)
    ndvi_after

And add some extra metadata for xarray to find when making plots:

.. jupyter-execute::

    ndvi_before.attrs["title"] = "NDVI before"
    ndvi_after.attrs["title"] = "NDVI after"

Now we can make pseudo-color plots of the NDVI from before and after the
disaster:

.. jupyter-execute::

    fig, axes = plt.subplots(2, 1, figsize=(10, 12), layout="tight")
    for ax, ndvi in zip(axes, [ndvi_before, ndvi_after]):
        # Limit the scale to [-1, +1] so the plots are easier to compare
        ndvi.plot(ax=ax, vmin=-1, vmax=1, cmap="RdBu_r")
        ax.set_title(ndvi.attrs["title"])
        ax.set_aspect("equal")
    plt.show()


Tracking differences
++++++++++++++++++++

An advantage of having our data in :class:`xarray.DataArray` format is that we
can perform **coordinate-aware** calculations. This means that taking the
difference between our two arrays will take into account the coordinates of
each pixel and only perform the operation where the coordinates align.

We can calculate the change in NDVI from one scene to the other by taking the
difference:

.. jupyter-execute::

    ndvi_change = ndvi_before - ndvi_after

    # Add som metadata for xarray
    ndvi_change.name = "ndvi_change"
    ndvi_change.attrs["long_name"] = "NDVI change"
    ndvi_change.attrs["title"] = (
        f"NDVI change between {before.attrs['date_acquired']} and "
        f"{after.attrs['date_acquired']}"
    )
    ndvi_change

.. admonition:: Did you notice?
    :class: hint

    The keen-eyed among you may have noticed that the number of points along
    the ``"easting"`` dimension has decreased. This is because :mod:`xarray`
    only makes the calculations for pixels where the two scenes coincide. In
    this case, there was an East-West shift between scenes but our calculations
    take that into account.

Now lets plot the difference:

.. jupyter-execute::


    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ndvi_change.plot(ax=ax, vmin=-1, vmax=1, cmap="PuOr")
    ax.set_aspect("equal")
    ax.set_title(ndvi_change.attrs["title"])
    plt.show()

There's some noise in the cloudy areas of both scenes in the northeast but
otherwise this plots highlights the area affected by flooding from the dam
collapse in purple at the center.


Estimating area
+++++++++++++++

One things we can do with indices and their differences in time is calculated
**area estimates**. If we know that the region of interest has index values
within a given value range, the area can be calculated by counting the number
of pixels within that range (a pixel in Landsat 8/9 scenes is 30 x 30 = 900 m²).

First, let's slice our NDVI difference to just the flooded area to avoid the
effect of the clouds in North. We'll use the :meth:`xarray.DataArray.sel`
method to slice using the UTM coordinates of the scene:

.. jupyter-execute::

    flood = ndvi_change.sel(
        easting=slice(587000, 594000),
        northing=slice(-2230000, -2225000),
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    flood.plot(ax=ax, vmin=-1, vmax=1, cmap="PuOr")
    ax.set_aspect("equal")
    plt.show()

Now we can create a mask of the flood area by selecting pixels that have a high
NDVI difference. Using a ``>`` comparison (or any other logical operator in
Python), we can create a boolean (``True`` or ``False``)
:class:`xarray.DataArray` as our mask:

.. jupyter-execute::

    # Threshold value determined by trial-and-error
    flood_mask = flood > 0.3

    # Add some metadata for xarray
    flood_mask.attrs["long_name"] = "flood mask"

    flood_mask

Plotting boolean arrays will use 1 to represent ``True`` and 0 to represent
``False``:

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    flood_mask.plot(ax=ax, cmap="gray")
    ax.set_aspect("equal")
    ax.set_title("Flood mask")
    plt.show()

.. seealso::

    Notice that our mask isn't perfect. There are little bloobs classified as
    flood pixels that are clearly outside the flood region. For more
    sophisticated analysis, see the image segmentation methods in
    `scikit-image <https://scikit-image.org/>`__.

Counting the number of ``True`` values is as easy as adding all of the boolean
values (remember that ``True`` corresponds to 1 and ``False`` to 0), which
we'll do with :meth:`xarray.DataArray.sum`:

.. jupyter-execute::

    flood_pixels = flood_mask.sum().values
    print(flood_pixels)

.. note::

    We use ``.values`` above because :meth:`~xarray.DataArray.sum` returns an
    :class:`xarray.DataArray` with a single value instead of the actual number.
    This is usually not a problem but it looks ugly when printed, so we grab
    the number with ``.values``.

Finally, the flood area is the number of pixels multiplied by the area of each
pixel (30 x 30 m²):

.. jupyter-execute::

    flood_area = flood_pixels * 30**2

    print(f"Flooded area is approximately {flood_area:.0f} m²")

Values in m² are difficult to imagine so a good way to communicate these
numbers is to put them into real-life context. In this case, we can use the
`football pitches <https://en.wikipedia.org/wiki/Football_pitch>`__ as a unit
that many people will understand:

.. jupyter-execute::

    flood_area_pitches = flood_area / 7140

    print(f"Flooded area is approximately {flood_area_pitches:.0f} football pitches")

.. warning::

   **This is a very rough estimate!** The final value will vary greatly if you
   change the threshold used to generate the mask (try it yourself).
   For a more thorough analysis of the disaster using remote-sensing data, see
   `Silva Rotta et al. (2020) <https://doi.org/10.1016/j.jag.2020.102119>`__.


NBR
---

The `Normalized Burn Ratio <https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-modis/normalized-burn-index-dNBR/>`__ is a useful tool to assess
areas affected by recent fires.
The NBR takes advantage of the relatively high reflectivity of burned areas in
the short-wave infrared (SWIR) range when compared with vegetated areas.
It's defined as

.. math::

    NBR = \dfrac{NIR - SWIR}{NIR + SWIR}

As an example, we can use our sample data from a fire that happened in near the
city of Corumbá, Brazil. The sample scene is generated from Level 1 Landsat 8
data. It contains only a section of the fire and we have scenes from before the
fire and from the very end of the fire.

.. jupyter-execute::

    before = xls.load_scene(xls.datasets.fetch_corumba_before())
    after = xls.load_scene(xls.datasets.fetch_corumba_after())
    after

Let's make RGB composites to get a sense of what these two scenes contain:

.. jupyter-execute::

    rgb_before = xls.adjust_l1_colors(
        xls.composite(before, rescale_to=(0, 0.2)),
        percentile=0,
    )
    rgb_after = xls.adjust_l1_colors(
        xls.composite(after, rescale_to=(0, 0.2)),
        percentile=0,
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 8), layout="constrained")
    for ax, rgb in zip(axes, [rgb_before, rgb_after]):
        rgb.plot.imshow(ax=ax)
        ax.set_title(rgb.attrs["title"])
        ax.set_aspect("equal")
    plt.show()

Now we can calculate the NBR for before and after:

.. jupyter-execute::

    nbr_before = xls.nbr(before)
    nbr_after = xls.nbr(after)

    fig, axes = plt.subplots(1, 2, figsize=(10, 8), layout="constrained")
    for ax, nbr in zip(axes, [nbr_before, nbr_after]):
        nbr.plot.imshow(ax=ax, cbar_kwargs=dict(orientation="horizontal"))
        ax.set_title(nbr.attrs["title"])
        ax.set_aspect("equal")
    plt.show()

A useful metric to better visualize the extent of the fires and to even
classify the burn intensity is the dNBR, which can be calculated as:

.. jupyter-execute::

    dnbr = nbr_before - nbr_after

    fig, axes = plt.subplots(1, 2, figsize=(10, 7), layout="constrained")
    rgb.plot.imshow(ax=axes[0])
    dnbr.plot.imshow(ax=axes[1], cbar_kwargs=dict(orientation="horizontal"))
    for ax in axes:
        ax.set_aspect("equal")
    plt.show()

The dNBR values > 0.1 indicate the areas that have been burned. The bright red
parts of the dNBR image above reflect the ongoing fire that was still burning
in the area.


Calculating your own indices
----------------------------

Calculating other indices will is relatively straight forward since most of
them only involve arithmetic operations on different bands.
As an example, let's calculate and plot the
`Modified Soil Adjusted Vegetation Index (MSAVI) <https://doi.org/10.1016/0034-4257(94)90134-1>`__
for our Manaus, Brazil, sample data:

.. jupyter-execute::

    scene = xls.load_scene(xls.datasets.fetch_manaus())

    msavi = 0.5 * (
        2 * scene.nir + 1
        - np.sqrt((2 * scene.nir + 1) * 2 - 8 * (scene.nir - scene.red))
    )
    msavi.name = "msavi"
    msavi.attrs["long_name"] = "modified soil adjusted vegetation index"

    # Plot an RGB as well for comparison
    rgb = xls.composite(scene, rescale_to=[0.02, 0.2])

    fig, axes = plt.subplots(2, 1, figsize=(10, 9.75), layout="constrained")
    rgb.plot.imshow(ax=axes[0])
    msavi.plot(ax=axes[1], vmin=-0.5, vmax=0.5, cmap="RdBu_r")
    axes[0].set_title("Manaus, Brazil")
    for ax in axes:
        ax.set_aspect("equal")
    plt.show()

**With this same logic, you could calculate any other index.**
