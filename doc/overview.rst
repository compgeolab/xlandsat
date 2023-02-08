.. _overview:

Overview
========

The library
-----------

All functionality in xlandsat is available from the base namespace of the
:mod:`xlandsat` package. This means that you can access all of them with a
single import:

.. jupyter-execute::

    # xlandsat is usually imported as xls
    import xlandsat as xls


Download a sample scene
-----------------------

As an example, lets download a tar archive of a Landsat 8 scene of the
`Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__
that happened in 2019 in Brazil.
The archive is available on figshare at
https://doi.org/10.6084/m9.figshare.21665630 and includes scenes from before
and after the disaster as both the full scene and a cropped version.

We'll use the functions in :mod:`xlandsat.datasets` to download the scenes from
before and after the disaster to our computer. To save space and bandwidth,
these are cropped versions of the full Landsat scenes.

.. jupyter-execute::

    path_before = xls.datasets.fetch_brumadinho_before()
    path_after = xls.datasets.fetch_brumadinho_after()
    print(path_before)
    print(path_after)


.. tip::

    Running the code above will only download the data once. We use `Pooch
    <https://www.fatiando.org/pooch>`__ to handle the downloads and it's smart
    enough to check if the file already exists on your computer. See
    :func:`pooch.retrieve` for more information.

.. seealso::

     If you want to use the full scenes instead of the cropped version,
     use :func:`pooch.retrieve` to fetch them from the figshare archive
     https://doi.org/10.6084/m9.figshare.21665630.


Load the scenes
---------------

Now that we have paths to the tar archives of the scenes, we can use
:func:`xlandsat.load_scene` to read the bands and metadata directly from the
archives (without unpacking):

.. jupyter-execute::

    before = xls.load_scene(path_before)
    before

And the after scene:

.. jupyter-execute::

    after = xls.load_scene(path_after)
    after

.. admonition:: Did you notice?
    :class: note

    If you look carefully at the coordinates for each scene, you may notice
    that they don't exactly coincide in area. That's OK since :mod:`xarray`
    knows how to take the pixel coordinates into account when doing
    mathematical operations like calculating indices and differences between
    scenes.


Plot some reflectance bands
---------------------------

Now we can use the :meth:`xarray.DataArray.plot` method to make plots of
individual bands with :mod:`matplotlib`. A bonus is that :mod:`xarray` uses the
metadata that :func:`xlandsat.load_scene` inserts into the scene to
automatically add labels and annotations to the plot.

.. jupyter-execute::

    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Make the pseudocolor plots of the near infrared band
    before.nir.plot(ax=ax1)
    after.nir.plot(ax=ax2)

    # Set the title using metadata from each scene
    ax1.set_title(f"Before: {before.attrs['title']}")
    ax2.set_title(f"After: {after.attrs['title']}")

    # Set the aspect to equal so that pixels are squares, not rectangles
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")

    plt.show()


Make composites
---------------

Plotting individual bands is good but we usually want to make some composite
images to visualize information from multiple bands at once.
Let's make both RGB (true color) and CIR (color infrared) composites for both
of our scenes using :func:`xlandsat.composite`:

.. jupyter-execute::

    # Make the composite and add it as a variable to the scene
    before = before.assign(rgb=xls.composite(before, rescale_to=[0, 0.2]))
    cir_bands = ("nir", "red", "green")
    before = before.assign(
        cir=xls.composite(before, bands=cir_bands, rescale_to=[0, 0.4]),
    )
    before

The composites have a similar layout as the bands but with an extra
``"channel"`` dimension corresponding to red, green, blue, and
alpha/transparency. The values are scaled to the [0, 255] range and the
composite is an array of unsigned 8-bit integers.

.. admonition:: Transparency
    :class: note

    If any of the bands used for the composite have NaNs, those pixels will
    have their transparency set to the maximum value of 255. If there are no
    NaNs in any band, then the composite will only have 3 channels (red, green,
    blue).


Now do the same for the after scene:

.. jupyter-execute::

    after = after.assign(rgb=xls.composite(after, rescale_to=[0, 0.2]))
    after = after.assign(
        cir=xls.composite(after, bands=cir_bands, rescale_to=[0, 0.4]),
    )
    after


Plot the composites
-------------------

Composites can be plotted using :meth:`xarray.DataArray.plot.imshow` (using
:meth:`~xarray.DataArray.plot` won't work and will display histograms instead).
Let's make the before and after figures again for each of the composites we
generated.

.. jupyter-execute::

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Plot the composites
    before.rgb.plot.imshow(ax=ax1)
    after.rgb.plot.imshow(ax=ax2)

    # The "long_name" of the composite is the band combination
    ax1.set_title(f"Before: {before.rgb.attrs['long_name']}")
    ax2.set_title(f"After: {after.rgb.attrs['long_name']}")

    ax1.set_aspect("equal")
    ax2.set_aspect("equal")

    plt.show()

And now the CIR composites:

.. jupyter-execute::

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    before.cir.plot.imshow(ax=ax1)
    after.cir.plot.imshow(ax=ax2)

    ax1.set_title(f"Before: {before.cir.attrs['long_name']}")
    ax2.set_title(f"After: {after.cir.attrs['long_name']}")

    ax1.set_aspect("equal")
    ax2.set_aspect("equal")

    plt.show()

Calculating indices
-------------------

Producing indices from these scenes is straightforward thanks to
:mod:`xarray`'s excelled support for coordinate-aware operations.
As an example, let's calculate the
`NDVI <https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index>`__:

.. jupyter-execute::

    before = before.assign(
        ndvi=(before.nir - before.red) / (before.nir + before.red),
    )
    after = after.assign(
        ndvi=(after.nir - after.red) / (after.nir + after.red),
    )

    # Set some metadata for xarray to find
    before.ndvi.attrs["long_name"] = "normalized difference vegetation index"
    before.ndvi.attrs["units"] = "dimensionless"
    after.ndvi.attrs["long_name"] = "normalized difference vegetation index"
    after.ndvi.attrs["units"] = "dimensionless"

    after

And now we can make pseudocolor plots of the NDVI:

.. jupyter-execute::

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Limit the scale to [-1, +1] so the plots are easier to compare
    before.ndvi.plot(ax=ax1, vmin=-1, vmax=1, cmap="RdBu_r")
    after.ndvi.plot(ax=ax2, vmin=-1, vmax=1, cmap="RdBu_r")

    ax1.set_title(f"Before: {before.attrs['title']}")
    ax2.set_title(f"After: {after.attrs['title']}")

    ax1.set_aspect("equal")
    ax2.set_aspect("equal")

    plt.show()

Finally, we can calculate the change in NDVI from one scene to the other by
taking the difference:

.. jupyter-execute::

    ndvi_change = before.ndvi - after.ndvi
    ndvi_change.name = "ndvi_change"
    ndvi_change.attrs["long_name"] = (
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

Now lets plot it:

.. jupyter-execute::


    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ndvi_change.plot(ax=ax, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_aspect("equal")
    plt.show()

There's some noise in the cloudy areas of both scenes in the northeast but
otherwise this plots highlights the area affected by flooding from the dam
collapse in bright red at the center.

What now?
---------

By getting the data into an :class:`xarray.Dataset`, xlandsat opens the door
for a huge range of operations. You now have access to everything that
:mod:`xarray` can do: interpolation, reduction, slicing, grouping, saving to
cloud-optimized formats, and much more. So go off and do something cool!
