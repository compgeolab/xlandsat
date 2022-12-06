.. _changes:

Changelog
=========

Version 0.1.0
-------------

Released on: 2022/12/06

doi: https://doi.org/10.5281/zenodo.7402498

New features:

* Add option to load only selected bands: https://github.com/compgeolab/xlandsat/pull/13
* Add option to crop a scene as its being loaded: https://github.com/compgeolab/xlandsat/pull/14

Documentation:

* Add full docstrings to the 2 API functions: https://github.com/compgeolab/xlandsat/pull/3
* Use a p instead of h2 for the README tagline: https://github.com/compgeolab/xlandsat/pull/4
* Add full docstrings to the 2 API functions: https://github.com/compgeolab/xlandsat/pull/5
* Use the "all versions" Zenodo DOI in citation: https://github.com/compgeolab/xlandsat/pull/7
* Expand and populate the Overview tutorial: https://github.com/compgeolab/xlandsat/pull/8

Maintenance:

* Default to float16 for loading scenes: https://github.com/compgeolab/xlandsat/pull/15
* Add codecov configuration file to control reports: https://github.com/compgeolab/xlandsat/pull/6
* Add tests for folder reading and > 1 MTL files: https://github.com/compgeolab/xlandsat/pull/11
* Add test for missing metadata files: https://github.com/compgeolab/xlandsat/pull/12

This release contains contributions from:

* Leonardo Uieda

Version 0.0.1
-------------

Released on: 2022/12/04

doi: https://doi.org/10.5281/zenodo.7395474

**First release of xlandsat!** This first release provides:

* A function to get Landsat 8 and 9 Collection 2 Level 2 scenes downloaded from
  `USGS EarthExplorer <https://earthexplorer.usgs.gov/>`__ into an
  :class:`xarray.Dataset`.
* A function to generate a composite as an :class:`xarray.DataArray` that can
  be easily plotted with xarray's machinery.

This release contains contributions from:

* Leonardo Uieda
