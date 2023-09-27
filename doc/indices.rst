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
As an example, we'll use two example scenes from before and after the
`Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__
to try to image and quantify the total area flooded by the damn collapse.

.. admonition:: Trigger warning
    :class: warning

    This tutorial uses data from the tragic
    `Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__,
    in which over 250 people lost their lives. We use this dataset to
    illustrate the usefulness of remote sensing data for monitoring such
    disasters but we want to acknowledge its tragic human consequences.
    **Some readers may find this topic disturbing and may not wish to read
    futher.**

First, we must import the required packages, download our two sample scenes,
and load them with :func:`xlandsat.load_scene`:

.. jupyter-execute::

    import xlandsat as xls
    import matplotlib.pyplot as plt


    path_before = xls.datasets.fetch_brumadinho_before()
    path_after = xls.datasets.fetch_brumadinho_after()

    before = xls.load_scene(path_before)
    after = xls.load_scene(path_after)
    after

Let's make RGB composites to get a sense of what these
two scenes contain:

.. jupyter-execute::

    rgb_before = xls.composite(before, rescale_to=(0.03, 0.2))
    rgb_after = xls.composite(after, rescale_to=(0.03, 0.2))

    fig, axes = plt.subplots(2, 1, figsize=(10, 12), layout="tight")
    for ax, rgb in zip(axes, [rgb_before, rgb_after]):
        rgb.plot.imshow(ax=ax)
        ax.set_title(rgb.attrs["title"])
        ax.set_aspect("equal")
    plt.show()


.. tip::

     See :ref:`composites` for more information on what we did above.

NDVI
----

We can calculate the
`NDVI <https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index>`__
for these scenes to see if we can isolate the effect of the flood following the
dam collapse.
NDVI highlights vegetation, which we assume will have decreased in the after
scene due to the flood.
NDVI is defined as:

.. math::

    NDVI = \dfrac{NIR - Red}{NIR + Red}

which we can calculate with xarray as:

.. jupyter-execute::

    ndvi_before = (before.nir - before.red) / (before.nir + before.red)
    ndvi_before

Now we can do the same for the after scene:

.. jupyter-execute::

    ndvi_after = (after.nir - after.red) / (after.nir + after.red)
    ndvi_after

And add some metadata for xarray to find when making plots:

.. jupyter-execute::

    for ndvi in [ndvi_before, ndvi_after]:
        ndvi.attrs["long_name"] = "normalized difference vegetation index"
        ndvi.attrs["units"] = "dimensionless"
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
--------------------

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
---------------

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

   These are very rough estimates! Do not use them as official numbers or for
   any purpose other than educational.
