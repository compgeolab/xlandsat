.. _io:

Loading and cropping scenes
===========================

One of the main features of xlandsat is being able to read scenes downloaded
from `USGS EarthExplorer <https://earthexplorer.usgs.gov/>`__ along with all
of the associated metadata.
EarthExplorer allows you to download scenes in two main formats:

1. As a single ``.tar`` file containing ``.TIF`` files for the bands and a file
   ending in ``MTL.txt`` with the metadata.
2. As individual ``.TIF`` and metadata files.

We support reading from both formats so you don't have really have to do much
after downloading the scene.

In this tutorial, we'll be using some of our sample datasets instead of actual
full scenes from EarthExplorer. This is mostly so we don't have to use the
large (~1Gb) files, which can take a bit of time to download and load. The
scenes we use have been cropped to make them smaller. But everything we do here
is exactly the same when you use it on full scenes from EarthExplorer.

.. admonition:: Downloading scenes from EarthExplorer
    :class: tip

    New to EarthExplorer? Watch this tutorial on how to use the service and
    download scenes that you can use with xlandsat:
    https://www.youtube.com/watch?v=Wn_G4fvitV8

As always, we'll start by importing xlandsat and other libraries we'll use:

.. jupyter-execute::

    import xlandsat as xls
    import matplotlib.pyplot as plt
    import pathlib

.. note::

    All of this works for Collection 2 Level 2 and Level 1 scenes.

Load a scene from a ``.tar`` archive
------------------------------------

If you downloaded a full scene from EarthExplorer in a ``.tar`` archive,
xlandsat can load the data from the archive directly. You don't have to unpack
it yourself and xlandsat reads everything in it by default. **This is usually
the easiest way to work with these data** but the downside is that the archive
can be quite large, particularly if you don't need all of the different bands
(see below for an alternative).

To simulate this use case, let's download the ``.tar`` archive for one of our
sample scenes using :func:`xlandsat.datasets.fetch_liverpool`:

.. jupyter-execute::

   path_to_archive = xls.datasets.fetch_liverpool()
   print(path_to_archive)

This will download the ``.tar`` archive to your computer and return the path
to the file.

.. note::

   Our sample data come in ``.tar.gz`` archives, which have been compressed
   (hence the ``.gz`` to save space and bandwidth. But all our functions work
   the same with ``.tar`` or ``.tar.gz`` archives.

To load a scene directly from the archive, use :func:`xlandsat.load_scene` with
the path to the archive file, which can be a string or a :class:`pathlib.Path`:

.. jupyter-execute::

   scene = xls.load_scene(path_to_archive)
   scene

The ``scene`` contains all of the bands available in the archive and has
metadata populated from the ``MTL.txt`` file. Notice also that the values for
each band have been converted to **surface reflectance** and **surface
temperature** automatically.

Load a scene from a folder
--------------------------

If you don't need all of the bands, you can save space by downloading only the
``.TIF`` files that you need from EarthExplorer. Once you do that, place the
``.TIF`` files and the associated ``MTL.txt`` file (**don't forget it**) in
the same folder. It's important that a **folder can only contain a single
scene**, so if you're working with multiple scenes you'll have to place them in
different folders.

Let's simulate this use case by telling
:func:`~xlandsat.datasets.fetch_liverpool` to unpack the archive and give us
the path to the folder instead of the archive:

.. jupyter-execute::

   path_to_folder = xls.datasets.fetch_liverpool(untar=True)
   print(path_to_folder)

Notice that there is now a ``.untar`` at the end of the name, indicating that
this is the folder where the archive has been unpacked.
We can use the :mod:`pathlib` module from the Python standard library to list
all of the files that are in this folder:

.. jupyter-execute::

    path_to_folder = pathlib.Path(path_to_folder)
    print(f"This is indeed a folder: {path_to_folder.is_dir()}")
    print("Folder contents:")
    for file in path_to_folder.iterdir():
        print(f"  {file.name}")

As you can see, the band ``.TIF`` files are there as well as the ``MTL.txt``
file. Now that we have the path to a folder that has these files, we can pass
it to :func:`xlandsat.load_scene` and it will do its job:

.. jupyter-execute::

   scene = xls.load_scene(path_to_folder)
   scene


Notice that this is the same result we had before.

.. hint::

    Only the ``.TIF`` files present will be loaded by
    :func:`xlandsat.load_scene`. So you don't need some of them, don't include
    them in the folder.


The scene, bands, and metadata
------------------------------

The ``scene`` itself is a :class:`xarray.Dataset` that contains:

1. ``easting`` and ``northing`` dimensions which are the UTM coordinates of
   the pixels (in meters).
2. Several data variables that each represent a band. The bands are referenced
   by name, not by number. Each band is a :class:`xarray.DataArray` that has
   the same dimensions as the scene.
3. Missing values in the scene (either from the padding or out-of-bounds
   pixels) are represented by :class:`numpy.nan`.
4. Metadata for the scene, each dimension, and each band.

Placing a :class:`xarray.Dataset` or :class:`xarray.DataArray` at the end of a
Jupyter notebook cell will display a nice preview of the contents:

.. jupyter-execute::

   scene

In the preview above, click on the icons to the right to access the metadata
for each dimension and band and a preview of their data values. The metadata
for the scene itself can be accessed by clicking in "Attributes". Go ahead and
explore what's available!

The metadata is available programmatically through the ``attrs`` attribute of
the scene. It behaves like a dictionary:

.. jupyter-execute::

    print(scene.attrs["landsat_product_id"])
    print(scene.attrs["date_acquired"])

The metadata for the bands and the dimensions can be accessed the same way:

.. jupyter-execute::

    print(scene.blue.attrs["filename"])
    print(scene.easting.attrs["long_name"])

Selecting which bands to load
-----------------------------

If you have more bands downloaded than you actually want to use, then we can
save time and memory by only loading the desired bands.
For example, if our only goal is to make an RGB composite, then we only really
need the red, green, and blue bands.
Instead of having to edit the ``.tar`` archive or move files out of our data
folder, we can tell :func:`xlandsat.load_scene` which bands we want by passing
it a list of band names like so:

.. jupyter-execute::

    scene = xls.load_scene(path_to_archive, bands=["red", "green", "blue"])
    scene

This works the same if reading from an archive or from a folder that contains
more band files than we want:

.. jupyter-execute::

    scene = xls.load_scene(path_to_folder, bands=["red", "green", "blue"])
    scene


Loading only a segment of the scene
-----------------------------------

Since Landsat scenes are large, it's not uncommon to need only a smaller
section of a scene. Limiting the spatial extent loaded can also help reduce the
memory requirement, particularly when loading a time series of scenes.
We could crop an existing scene after loading by using :meth:`xarray.Dataset.sel`
with the UTM bounding box of the desired region:

.. jupyter-execute::

    scene = xls.load_scene(path_to_archive)
    cropped = scene.sel(
        easting=slice(4.88e5, 4.90e5),
        northing=slice(5.925e6, 5.927e6),
    )
    cropped

But this will still load the full scene, which **takes up time and memory**. A
**better way** to do this is to crop the scene directly when loading it:

.. jupyter-execute::

    cropped = xls.load_scene(
        path_to_archive,
        region=(4.88e5, 4.90e5, 5.925e6, 5.927e6),
    )
    cropped

Notice that in both examples we were able to use the natural UTM coordinates
of the scene instead of pixel numbers. This is particularly important when
cropping scenes with the same WRS path/row at different times, since their
boundaries won't coincide exactly and cropping by pixels would result in
misaligned images.

Load the panchromatic band
--------------------------

The panchromatic band from Level 1 scenes will be ignored by
:func:`xlandsat.load_scene` if it's present in an archive or folder.
This is because of it's higher spatial resolution, which means that it can't
share dimension coordinates with the other bands. For this reason, we have
the separate function :func:`xarray.load_panchromatic` for loading it.
Just like with regular scenes, we can provide either a ``.tar`` archive or a
folder that contains the band and the ``MTL.txt`` file:

.. jupyter-execute::

    path_to_pan = xls.datasets.fetch_liverpool_panchromatic()
    pan = xls.load_panchromatic(path_to_pan)
    pan

And we can also crop the panchromatic band upon loading to the same extent as
our regular scene:

.. jupyter-execute::

    cropped_pan = xls.load_panchromatic(
        path_to_pan,
        region=(4.88e5, 4.90e5, 5.925e6, 5.927e6),
    )
    cropped_pan

This is particularly useful for :ref:`pansharpening <pansharpen>` to make
higher resolution RGB composites.
