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
https://doi.org/10.6084/m9.figshare.21665630.v2 and includes scenes from before
and after the disaster as both the full scene and a cropped version.

We'll use :mod:`pooch` to download the scenes from before and after the
disaster to our computer.
To save space and bandwidth, we'll use the cropped version here.

.. jupyter-execute::

    import pooch

    path_before = pooch.retrieve(
          "doi:10.6084/m9.figshare.21665630.v2/LC08_L2SP_218074_20190114_20200829_02_T1-cropped.tar.gz",
         known_hash="md5:d2a503c944bb7ef3b41294d44b77e98c",
    )
    path_after = pooch.retrieve(
          "doi:10.6084/m9.figshare.21665630.v2/LC08_L2SP_218074_20190130_20200829_02_T1-cropped.tar.gz",
         known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    print(path_before)
    print(path_after)


.. tip::

    Running the code above will only download the data once since Pooch is
    smart enough to check if the file already exists on your computer.
    See :func:`pooch.retrieve` for more information.

.. seealso::

     If you want to use the full scene instead of the cropped version,
     remove the ``-cropped`` from the file names update the MD5 hashes
     accordingly, which you can find on the figshare archive
     https://doi.org/10.6084/m9.figshare.21665630.v2.


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


What now?
---------

Learn more about what you can do with xlandsat and xarray:

* :ref:`composites`
* :ref:`indices`
* :ref:`pansharpen`

By getting the data into an :class:`xarray.Dataset`, xlandsat opens the door
for a huge range of operations. You now have access to everything that
:mod:`xarray` can do: interpolation, reduction, slicing, grouping, saving to
cloud-optimized formats, and much more. So go off and do something cool!
