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

    # Download a cropped Landsat 8 scene from the Brumadinho dam disaster
    # (Brazil). The function downloads it and returns the path to the .tar file
    # containing the scene.
    path = xls.datasets.fetch_brumadinho_after()

    # Load the scene directly from the archive (no need to unpack it)
    scene = xls.load_scene(path)

    # Make an RGB composite and stretch the contrast
    rgb = xls.composite(scene, rescale_to=[0.03, 0.2])

    # Plot the composite
    rgb.plot.imshow()


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

    Only **Landsat 8 and 9 Level 1 & 2 data products** have been tested at the
    moment.

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
    :caption: User Guide

    composites.rst
    indices.rst
    pansharpen.rst
    missing-values.rst
    plot-overlay.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Reference Documentation

    api/index.rst
    citing.rst
    references.rst
    changes.rst
    compatibility.rst
    versions.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Community

    How to contribute <https://github.com/compgeolab/xlandsat/blob/main/CONTRIBUTING.md>
    Code of Conduct <https://github.com/compgeolab/xlandsat/blob/main/CODE_OF_CONDUCT.md>
    Source code on GitHub <https://github.com/compgeolab/xlandsat>
    Computer-Oriented Geoscience Lab <https://www.compgeolab.org>
