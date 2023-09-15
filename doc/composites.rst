.. _composites:

Composites
==========

Plotting individual bands is good but we usually want to make some composite
images to visualize information from multiple bands at once.
For that, we have to create **composites**.
We provide the :func:`xlandsat.composite` function to make this process easier.

As an example, let's load an example scene from the
`Brumadinho tailings dam disaster <https://en.wikipedia.org/wiki/Brumadinho_dam_disaster>`__:

.. jupyter-execute::

    import xlandsat as xls
    import matplotlib.pyplot as plt

    path = xls.datasets.fetch_brumadinho_after()

    scene = xls.load_scene(path)


RGB composites
--------------

Let's make an RGB (true color) composite since that is the most fundamental
type and it allows us to get a good handle on what we're seeing in the scene.
The RGB composite is also the default made by :func:`xlandsat.composite` if the
bands aren't specified.

.. jupyter-execute::

    rgb = xls.composite(scene)
    rgb

The composite has a similar layout as the bands of a scene but with an extra
``"channel"`` dimension corresponding to red, green, blue, and
alpha/transparency. The values are scaled to the [0, 255] range and the
composite is an array of unsigned 8-bit integers.

.. admonition:: Transparency
    :class: note

    If any of the bands used for the composite have NaNs, those pixels will
    have their transparency set to the maximum value of 255. If there are no
    NaNs in any band, then the composite will only have 3 channels (red, green,
    blue).


Plotting a composite
--------------------

Composites can be plotted using :meth:`xarray.DataArray.plot.imshow` (using
:meth:`~xarray.DataArray.plot` won't work and will display histograms instead).

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    rgb.plot.imshow(ax=ax)

    # The "long_name" of the composite is the band combination
    ax.set_title(f"Composite: {rgb.attrs['long_name']}")

    # Make sure pixels are square and don't have any distortions from plotting
    ax.set_aspect("equal")

    plt.show()

Well, this looks bad because that bright cloud is making it so the ground
pixels have only a small share of the full range of available values. This can
be mitigated by rescaling the intensity of the image to a smaller range of
reflectance values.


Rescaling intensity (AKA contrast stretching)
---------------------------------------------

We rescale the intensities of a composite to a given reflectance range by
setting the ``rescale_to`` parameter when creating a composite. It takes a list
of the min and max reflectance values allowed. For this image, we can arrive at
the following values by trial and error until it looks nice:

.. jupyter-execute::

    rgb = xls.composite(scene, rescale_to=[0.03, 0.2])

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    rgb.plot.imshow(ax=ax)
    ax.set_title(f"Rescaled composite: {rgb.attrs['long_name']}")
    ax.set_aspect("equal")
    plt.show()

Notice that we can more clearly see the colors of the ground but we lose a lot
of detail in the clouds.

.. note::

   The rescaling has to be done when creating the composite so that we can use
   min/max values in reflectance units. After a composite is created, the
   original range of values is lost and we'd have to specify the min/max
   between 0 and 255 instead.


Color infrared composites
-------------------------

Another common type of composite is the color infrared (CIR) composites. These
change the bands used to NIR, red, and green and serve primarily to distinguish
healthy vegetation from other objects in the scene. Let's make one by specifying
this band combination to :func:`xlandsat.composite` to see if we can more clearly spot the dam flood.

.. jupyter-execute::

    cir = xls.composite(scene, bands=("nir", "red", "green"), rescale_to=[0, 0.4])

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    cir.plot.imshow(ax=ax)
    ax.set_title(f"Composite: {rgb.attrs['long_name']}")
    ax.set_aspect("equal")
    plt.show()

The flood region can be clearly spotted in the image above as the brown/gray
blog in the center.

**With this, you can now make composites using any other band combination you
may want!**
