.. _composites:

Making composites
=================

Plotting individual bands is nice but we usually want to make some composite
images, both RGB and false-color, to visualize information from multiple bands
at once.
We provide the :func:`xlandsat.composite` function to make this process easier
and produce composites that are compatible with both :mod:`xarray` and
:mod:`matplotlib`.

As an example, let's load our example scene from Manaus, Brazil, which is where
the Solimões (brown water) and Negro (black water) rivers merge to form the
Amazon river:

.. jupyter-execute::

    import xlandsat as xls
    import matplotlib.pyplot as plt


    path = xls.datasets.fetch_manaus()
    scene = xls.load_scene(path)
    scene


RGB composites
--------------

Let's make an RGB (true color) composite since that is the most fundamental
type and it allows us to get a good handle on what we're seeing in the scene.
The RGB composite is also the default made by :func:`xlandsat.composite` if the
bands aren't specified.

.. jupyter-execute::

    rgb = xls.composite(scene)
    rgb

The composite is also an :class:`xarray.DataArray` and is similar to the bands.
It has the same easting and northing dimensions but also an extra ``"channel"``
dimension, which corresponds to red, green, blue, and alpha/transparency. This
extra dimension is what combines the three bands into a single color image. The
values are scaled to the [0, 255] range and the composite is an array of
unsigned 8-bit integers.

.. admonition:: Transparency
    :class: note

    If any of the bands used for the composite have NaNs, those pixels will
    have their transparency set to the maximum value of 255. If there are no
    NaNs in any band, then the composite will only have 3 channels (red, green,
    blue).


Plotting composites
-------------------

Composites can be plotted using the :meth:`xarray.DataArray.plot.imshow` method:

.. jupyter-execute::

    rgb.plot.imshow()


With no arguments, xarray takes care of creating the new figure and adding a
lot of the different plot elements, like axis labels and units.
If we want more control over the plot, we must create a matplotlib figure and
axes separately and tell :meth:`~xarray.DataArray.plot.imshow` to plot on those
instead:

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    rgb.plot.imshow(ax=ax)

    # The "long_name" of the composite is the band combination
    ax.set_title(rgb.attrs["long_name"].title())

    # Make sure pixels are square when plotting to avoid distortions
    ax.set_aspect("equal")

    plt.show()

Well, this looks bad because some very bright pixels in the city are making the
majority of the other pixels have only a small share of the full range of
available values. This can be mitigated by rescaling the intensity of the image
to a smaller range of reflectance values.

.. note::

    Using :meth:`xarray.DataArray.plot` instead of
    :meth:`xarray.DataArray.plot.imshow` won't work and will display histograms
    instead.


Rescaling intensity (AKA contrast stretching)
---------------------------------------------

We rescale the intensities of a composite to a given reflectance range by
setting the ``rescale_to`` parameter when creating a composite. It takes a list
of the min and max reflectance values allowed. For this image, we can arrive at
the following values by trial and error until it looks nice:

.. jupyter-execute::

    rgb = xls.composite(scene, rescale_to=[0.01, 0.2])

    # Pretty much the same plotting code
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    rgb.plot.imshow(ax=ax)
    ax.set_title(f"Rescaled {rgb.attrs['long_name'].title()}")
    ax.set_aspect("equal")
    plt.show()

Notice that we can more clearly see the different colors of the forest and the
rivers.
However, it can still be a bit hard to distinguish between some of the water
bodies and the forest in the right side of the scene.
Other band combinations can generate composites that better highlight these
features.

.. note::

   The rescaling has to be done when creating the composite so that we can use
   min/max values in reflectance units. After a composite is created, the
   original range of values is lost and we'd have to specify the min/max
   between 0 and 255 instead.


Color infrared composites
-------------------------

Another common type of composite is the color infrared (CIR) composites,
which uses the NIR, red, and green bands as the red, green, blue channels.
The added information of the NIR band helps highlight vegetation, which can
help us distinguish between the water and forest on the right.
Let's make one by specifying
this band combination to :func:`xlandsat.composite` to see what happens:

.. jupyter-execute::

    cir = xls.composite(
        scene, rescale_to=[0, 0.4], bands=("nir", "red", "green"),
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    cir.plot.imshow(ax=ax)
    ax.set_title(cir.attrs["long_name"].title())
    ax.set_aspect("equal")
    plt.show()

In this composite, the contrast between the forest and water bodies on the
right are much clearer!

Composites highlighting fires
-----------------------------

When a fire is currently burning and producing smoke, it can be difficult to
visualize the fire front in a regular RGB composite. For this, the SWIR and NIR
bands can be very useful. A composite of SWIR, NIR, and blue can be useful to
highlight the burned areas, ongoing fire, and vegetation.
Let's see what this looks like in our Corumbá, Brazil, sample data:

.. jupyter-execute::

    corumba = xls.load_scene(xls.datasets.fetch_corumba_after())
    corumba_rgb = xls.adjust_l1_colors(
        xls.composite(corumba, rescale_to=(0, 0.2)),
        percentile=0,
    )
    corumba_fire = xls.composite(
        corumba, rescale_to=(0, 0.4), bands=["swir1", "nir", "blue"],
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 8), layout="constrained")
    for ax, composite in zip(axes, [corumba_rgb, corumba_fire]):
        composite.plot.imshow(ax=ax)
        ax.set_title(rgb.attrs["long_name"])
        ax.set_aspect("equal")
    plt.show()

The burn scar can be seen in the RGB but there is smoke in the South and it's
not clear whether there are any active fires still burning.
The SWIR/NIR/green composite highlights the active fires in bright red and can
even show then through the smoke (which doesn't reflect in the SWIR bands).
This composite also highlights the difference between burned areas and
preserved vegetation.

Other composites
----------------

You can make pretty much any composite you'd like by passing the correct band
combination to :func:`xlandsat.composite`.
For example, let's make one with NIR as red, SWIR1 as green, and red as blue:

.. jupyter-execute::

    custom = xls.composite(
        scene, rescale_to=[0, 0.4], bands=("nir", "swir1", "red"),
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    custom.plot.imshow(ax=ax)
    ax.set_title(custom.attrs["long_name"].title())
    ax.set_aspect("equal")
    plt.show()

This particular composite is great at distinguishing between built structures
in the city and along the canals (light green), the water ways (dark blue and
purple), and the forest (orange).
