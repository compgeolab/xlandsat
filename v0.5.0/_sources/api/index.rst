.. _api:

List of functions and classes (API)
===================================

.. automodule:: xlandsat

.. currentmodule:: xlandsat

Input and output
----------------

.. autosummary::
   :toctree: generated/

    load_scene
    save_scene
    load_panchromatic

Processing
----------

.. autosummary::
   :toctree: generated/

    composite
    pansharpen
    equalize_histogram
    adjust_l1_colors
    interpolate_missing

Sample datasets
---------------

.. automodule:: xlandsat.datasets

.. currentmodule:: xlandsat

.. autosummary::
    :toctree: generated/

    datasets.fetch_brumadinho_after
    datasets.fetch_brumadinho_before
    datasets.fetch_liverpool
    datasets.fetch_liverpool_panchromatic
    datasets.fetch_manaus
    datasets.fetch_momotombo
    datasets.fetch_roraima
