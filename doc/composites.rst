.. _composites:

Composites
==========

Plotting individual bands is good but we usually want to make some composite
images to visualize information from multiple bands at once.
For that, we have to create **composites**.
We provide the :func:`xlandsat.composite` function to make this process easier.

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


Creating composites
-------------------

Let's make both RGB (true color) and CIR (color infrared) composites for both
of our scenes:

.. jupyter-execute::

    # Make the composite and add it as a variable to the scene
    before = before.assign(rgb=xls.composite(before, rescale_to=[0.03, 0.2]))
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

    after = after.assign(rgb=xls.composite(after, rescale_to=[0.03, 0.2]))
    after = after.assign(
        cir=xls.composite(after, bands=cir_bands, rescale_to=[0, 0.4]),
    )
    after


Plotting composites
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
