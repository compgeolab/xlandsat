.. _indices:

Indices
-------

Indices calculated from multispectral satellite imagery are powerful ways to
quantitatively analyze these data.
They take advantage of different spectral properties of materials to
differentiate between them.
Many of these indices can be calculated with simple arithmetic operations.
So now that our data are in :class:`xarray.Dataset`'s it's fairly easy to
calculate them.

NDVI
----

As an example, let's load two example scenes from the
`Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__:

.. jupyter-execute::

    import xlandsat as xls
    import matplotlib.pyplot as plt
    import pooch

    path_before = pooch.retrieve(
          "doi:10.6084/m9.figshare.21665630.v2/LC08_L2SP_218074_20190114_20200829_02_T1-cropped.tar.gz",
         known_hash="md5:d2a503c944bb7ef3b41294d44b77e98c",
    )
    path_after = pooch.retrieve(
          "doi:10.6084/m9.figshare.21665630.v2/LC08_L2SP_218074_20190130_20200829_02_T1-cropped.tar.gz",
         known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )

    before = xls.load_scene(path_before)
    after = xls.load_scene(path_after)


We can calculate the
`NDVI <https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index>`__
for these scenes to see if we can isolate the effect of the flood following the
dam collapse:


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

And now we can make pseudo-color plots of the NDVI:

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
    ndvi_change.plot(ax=ax, vmin=-1, vmax=1, cmap="PuOr")
    ax.set_aspect("equal")
    plt.show()

There's some noise in the cloudy areas of both scenes in the northeast but
otherwise this plots highlights the area affected by flooding from the dam
collapse in bright red at the center.