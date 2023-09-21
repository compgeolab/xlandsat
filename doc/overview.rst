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


Why use xlandsat?
-----------------

One of the main features of xlandsat is the ability to read a scene downloaded
from `USGS EarthExplorer <https://earthexplorer.usgs.gov/>`__ into an
:class:`xarray.Dataset`, which is very useful for processing and plotting
multidimensional array data.
The downloaded scenes can come in 2 main formats:

1. A ``.tar`` file which includes several bands in ``.TIF`` format and metadata in text files.
2. The bands and metadata files downloaded individually.

When reading the TIF files using tools like
`rioxarray <https://corteva.github.io/rioxarray/html/index.html>`__, some of
the rich metadata can be missing since it's not always present in the TIF files
themselves.
Things like UTM zones, conversion factors, units, data provenance, WRS path/row
numbers, etc.
We take care of fetching that information from the ``*_MTL.txt`` files provided
by EarthExplorer so that xarray can use it, for example when annotating plots.


Download a sample scene
-----------------------

The :mod:`xlandsat.datasets` module includes functions for downloading some
sample scenes that we can use. These are cropped to smaller regions of interest
in order to save download time. But everything we do here with these sample
scenes is exactly the same as you would do with a full scene from
EarthExplorer.

As an example, lets download a ``.tar`` archive of a Landsat 9 scene of the
city of Manaus, in the Brazilian Amazon:

.. jupyter-execute::

    path_to_archive = xls.datasets.fetch_manaus()
    print(path_to_archive)

The :func:`~xlandsat.datasets.fetch_manaus` function downloads the data file
and returns the **path** to the archive on your machine as an :class:`str`.
The rest of this tutorial can be executed with your own data by changing the
``path_to_archive`` to point to your data file instead.

.. tip::

    The path can also point to a folder with the ``.TIF`` and the ``*_MTL.txt``
    file instead of a ``.tar`` archive.

.. note::

    Running the code above will only download the data once. We use `Pooch
    <https://www.fatiando.org/pooch>`__ to handle the downloads and it's smart
    enough to check if the file already exists on your computer. See
    :func:`pooch.retrieve` for more information.

.. seealso::

     If you want to use the full scenes instead of the cropped version,
     use :func:`pooch.retrieve` to fetch them from the figshare archive
     https://doi.org/10.6084/m9.figshare.24167235.v1.


Load the scene
--------------

Now that we have the path to the tar archive of the scene, we can use
:func:`xlandsat.load_scene` to read the bands and metadata directly from the
archive:

.. jupyter-execute::

    scene = xls.load_scene(path_to_archive)
    scene


.. tip::

    Placing the ``scene`` variable at the end of a code cell in a Jupyter
    notebook will display a nice preview of the data. This is very useful for
    looking up metadata and seeing which bands were loaded.

The scene is an :class:`xarray.Dataset`. It contains general metadata for the
scene and all of the bands available in the archive as
:class:`xarray.DataArray`.
The bands each have their own set of metadata as well and can be accessed by
name:

.. jupyter-execute::

    scene.nir


Plot some reflectance bands
---------------------------

Now we can use the :meth:`xarray.DataArray.plot` method to make plots of
individual bands with :mod:`matplotlib`. A bonus is that :mod:`xarray` uses the
metadata that :func:`xlandsat.load_scene` inserts into the scene to
automatically add labels and annotations to the plot:

.. jupyter-execute::

    import matplotlib.pyplot as plt

    band_names = list(scene.data_vars.keys())

    fig, axes = plt.subplots(
        len(band_names), 1, figsize=(8, 16), layout="compressed",
    )

    # Set the title using metadata from each scene
    fig.suptitle(scene.attrs["title"])

    for band, ax in zip(band_names, axes.ravel()):
        # Make a pseudocolor plot of the band
        scene[band].plot(ax=ax)
        # Set the aspect to equal so that pixels are squares, not rectangles
        ax.set_aspect("equal")

    plt.show()


What now?
---------

Checkout some of the other things that you can do with xlandsat:

* :ref:`composites`
* :ref:`indices`

Plus, by getting the data into an :class:`xarray.Dataset`, xlandsat opens the
door for a huge range of operations. You now have access to everything that
:mod:`xarray` can do: reduction, slicing, grouping, saving to cloud-optimized
formats, and much more. So go off and do something cool!
