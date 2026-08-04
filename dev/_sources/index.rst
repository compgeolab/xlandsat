.. title:: Home

.. grid::
    :gutter: 2 3 3 3
    :margin: 5 5 0 0
    :padding: 0 0 0 0

    .. grid-item::
        :columns: 12 8 8 8

        .. raw:: html

            <h1 class="display-1">xlandsat</h1>

        .. div:: sd-fs-3

            Analyze Landsat remote sensing images using xarray

    .. grid-item::
        :columns: 12 4 4 4

        .. image:: ./_static/logo.svg
            :width: 200px
            :class: sd-m-auto dark-light


**xlandsat** is Python library for loading and analyzing Landsat scenes
downloaded from `USGS EarthExplorer <https://earthexplorer.usgs.gov/>`__ with
the power of :mod:`xarray`.
We take care of reading the metadata from the ``*_MTL.txt`` files provided by
EarthExplorer and organizing the bands into a single :class:`xarray.Dataset`
data structure for easier manipulation, processing, and visualization.

Here's a quick example:

.. jupyter-execute::

    import xlandsat as xls

    # Download a sample Landsat 9 scene in EarthExplorer format
    path_to_scene_file = xls.datasets.fetch_manaus()
    # Load the data from the file into an xarray.Dataset
    scene = xls.load_scene(path_to_scene_file)
    # Display the scene and included metadata
    scene

.. jupyter-execute::

    # Make an RGB composite as an xarray.DataArray
    rgb = xls.composite(scene, rescale_to=[0.02, 0.2])
    # Plot the composite on an interactive Leaflet map
    xls.plot_composite_leaflet(rgb, height="400px")


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

        .. button-link:: https://github.com/compgeolab/xlandsat/issues
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

.. admonition:: Looking for large-scale processing or other satellites?
    :class: seealso

    Our goal is **not** to provide a solution for large-scale data processing.
    Our target is smaller scale analysis done on individual computers (which is
    probably the main way EarthExplorer is used).

    * For cloud-based data processing, see the `Pangeo Project <https://pangeo.io/>`__.
    * For other satellites and more powerful features, use `Satpy <https://github.com/pytroll/satpy>`__.


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

    io.rst
    composites.rst
    equalize-histogram.rst
    indices.rst
    missing-values.rst
    pansharpen.rst
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
