.. _indices:

Calculating indices
-------------------

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

    ndvi_before.attrs["long_name"] = "normalized difference vegetation index"
    ndvi_before.attrs["units"] = "dimensionless"
    ndvi_after.attrs["long_name"] = "normalized difference vegetation index"
    ndvi_after.attrs["units"] = "dimensionless"

Now we can make pseudo-color plots of the NDVI from before and after the
disaster:

.. jupyter-execute::

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Limit the scale to [-1, +1] so the plots are easier to compare
    ndvi_before.plot(ax=ax1, vmin=-1, vmax=1, cmap="RdBu_r")
    ndvi_after.plot(ax=ax2, vmin=-1, vmax=1, cmap="RdBu_r")

    ax1.set_title(f"NDVI before: {before.attrs['title']}")
    ax2.set_title(f"NDVI after: {after.attrs['title']}")

    ax1.set_aspect("equal")
    ax2.set_aspect("equal")

    plt.show()

Finally, we can calculate the change in NDVI from one scene to the other by
taking the difference:

.. jupyter-execute::

    ndvi_change = ndvi_before - ndvi_after
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
    ndvi_change.plot(ax=ax, vmin=-1, vmax=1, cmap="PuOr")
    ax.set_aspect("equal")
    plt.show()

There's some noise in the cloudy areas of both scenes in the northeast but
otherwise this plots highlights the area affected by flooding from the dam
collapse in purple at the center.
