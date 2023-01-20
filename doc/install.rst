.. _install:

Installing
==========

There are different ways to install xlandsat:

.. tab-set::

    .. tab-item:: pip

        Using the `pip package manager <https://pypi.org/project/pip/>`__:

        .. code:: bash

            pip install xlandsat

    .. tab-item:: conda/mamba

        Using the `conda package manager <https://conda.io/>`__ (or ``mamba``)
        that comes with the Anaconda/Miniconda distribution:

        .. code:: bash

            conda install xlandsat --channel conda-forge

    .. tab-item:: Developement version

        You can use ``pip`` to install the latest **unreleased** version from
        GitHub (**not recommended** in most situations):

        .. code:: bash

            python -m pip install --upgrade git+https://github.com/compgeolab/xlandsat

.. note::

   The commands above should be executed in a terminal. On Windows, use the
   ``cmd.exe`` or the "Anaconda Prompt" app if you’re using Anaconda.


Which Python?
-------------

You'll need **Python >= 3.7**.
See :ref:`python-versions` if you require support for older versions.

Dependencies
------------

These required dependencies should be installed automatically when you install
xlandsat with ``pip`` or ``conda``:

* `numpy <http://www.numpy.org/>`__
* `xarray <https://xarray.dev/>`__
* `scikit-image <https://scikit-image.org/>`__
* `imageio <https://github.com/imageio/imageio>`__
* `tifffile <https://pypi.org/project/tifffile/>`__

See :ref:`dependency-versions` for the our policy of oldest supported versions
of each dependency.
