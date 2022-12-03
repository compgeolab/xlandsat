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

.. jupyter-execute::

    import pooch


    path = pooch.retrieve(
          "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
         known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    print(path)


Load the scene
--------------

.. jupyter-execute::

    scene = xls.load_scene(path)
    scene


Plot some bands
---------------

.. jupyter-execute::

    import matplotlib.pyplot as plt


    scene.nir.plot()
    plt.axis("scaled")
    plt.show()


Make a composite
----------------

.. jupyter-execute::

    composite = xls.composite(scene, rescale_to=[0, 0.2])
    scene = scene.assign(rgb=composite)
    scene


Plot the composite
------------------

.. jupyter-execute::

    scene.rgb.plot.imshow()
    plt.axis("scaled")
    plt.title(f"{scene.attrs['title']}\n{scene.rgb.attrs['long_name']}")
    plt.show()
