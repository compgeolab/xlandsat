.. title:: Home

.. grid::
    :gutter: 2 3 3 3
    :margin: 5 5 0 0
    :padding: 0 0 0 0

    .. grid-item::
        :columns: 12 12 12 12

        .. raw:: html

            <h1 class="display-1">xlandsat</h1>

        .. div:: sd-fs-3

            Load Landsat remote sensing images into xarray


**xlandsat** is Python library for
loading Landsat scenes downloaded from
`USGS EarthExplorer <https://earthexplorer.usgs.gov/>`__ into
:class:`xarray.Dataset` containers.
We take care of reading the metadata from the ``*_MTL.txt`` files provided by
EarthExplorer and organizing the bands into a single data structure for easier
manipulation, processing, and visualization.

Here's a quick example:

.. jupyter-execute::

    import xlandsat as xls
    import pooch  # for downloading sample data

    # Download a cropped scene from the Brumadinho dam (Brazil)
    path = pooch.retrieve(
          "doi:10.6084/m9.figshare.21665630.v1/cropped-after.tar.gz",
         known_hash="md5:4ae61a2d7a8b853c727c0c433680cece",
    )
    # Load the scene directly from the archive (no need to unpack it)
    scene = xls.load_scene(path)
    # Make an RGB composite and add it to the scene Dataset
    scene = scene.assign(rgb=xls.composite(scene, rescale_to=[0, 0.2]))
    # Plot the composite
    scene.rgb.plot.imshow()


----

.. grid:: 1 2 1 2
    :margin: 5 5 0 0
    :padding: 0 0 0 0
    :gutter: 4

    .. grid-item-card:: :octicon:`info` Getting started
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        New to xlandsat? Start here!

        .. button-ref:: overview
            :ref-type: ref
            :click-parent:
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`comment-discussion` Need help?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Open an Issue on GitHub.

        .. button-link:: https://github.com/compgeolab/xlandsat
            :click-parent:
            :color: primary
            :outline:
            :expand:

            Join the conversation :octicon:`link-external`

    .. grid-item-card:: :octicon:`file-badge` Reference documentation
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        A list of available functions.

        .. button-ref:: api
            :ref-type: ref
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`bookmark` Using for research?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Citations help support our work!

        .. button-ref:: citing
            :ref-type: ref
            :color: primary
            :outline:
            :expand:

----

.. note::

    Only **Landsat 8 and 9 Collection 2 Level 2 data products** are supported at
    the moment.

.. admonition:: xlandsat is ready for use but still changing
    :class: important

    This means that we sometimes break backwards compatibility as we try to
    improve the software based on user experience, new ideas, better design
    decisions, etc. Please keep that in mind before you update xlandsat to a
    newer version.

    :octicon:`code-review` **We welcome feedback and ideas!** This is a great
    time to bring new ideas on how we can improve the project. Submit
    `issues on GitHub <https://github.com/compgeolab/xlandsat/issues>`__.

.. admonition:: Looking for large-scale cloud-based processing?
    :class: seealso

    Our goal is not to provide a solution for large-scale data processing. The
    target is smaller scale analysis done on individual computers (which is
    probably the main way EarthExplorer is used). For cloud-based data
    processing, see the `Pangeo Project <https://pangeo.io/>`__.


.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Getting Started

    overview.rst
    install.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Reference Documentation

    api/index.rst
    citing.rst
    changes.rst
    compatibility.rst
    versions.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Links

    Source code on GitHub <https://github.com/compgeolab/xlandsat>
    Computer-Oriented Geoscience Lab <https://www.compgeolab.org>
