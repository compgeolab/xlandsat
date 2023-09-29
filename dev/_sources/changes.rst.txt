.. _changes:

Changelog
=========

Version 0.4.0
-------------

Released on: 2023/09/28

doi: https://doi.org/10.5281/zenodo.8348805

Bug fixes:

* Bug fix: Use np.abs in pansharpen to avoid sign issues (`#34 <https://github.com/compgeolab/xlandsat/pull/34>`__)

New features and improvements:

* Add function for histogram equalization (`#40 <https://github.com/compgeolab/xlandsat/pull/40>`__ `#54 <https://github.com/compgeolab/xlandsat/pull/54>`__)
* Add function to fill missing values by interpolation (`#36 <https://github.com/compgeolab/xlandsat/pull/36>`__)
* Faster version of cropped loading using less RAM (`#28 <https://github.com/compgeolab/xlandsat/pull/28>`__)
* Add sample data for Manaus, Brazil (`#49 <https://github.com/compgeolab/xlandsat/pull/49>`__)
* Add sample data from Mount Roraima (`#39 <https://github.com/compgeolab/xlandsat/pull/39>`__)
* Add sample data for the Momotombo eruption (`#32 <https://github.com/compgeolab/xlandsat/pull/32>`__)

Documentation:

* Tutorial about the many ways to read data (`#57 <https://github.com/compgeolab/xlandsat/pull/57>`__)
* Add section on Indices tutorial about other indices (`#55 <https://github.com/compgeolab/xlandsat/pull/55>`__)
* Add a trigger warning and update the indices tutorial (`#53 <https://github.com/compgeolab/xlandsat/pull/53>`__)
* Use the Manaus data in the Composites tutorial (`#52 <https://github.com/compgeolab/xlandsat/pull/52>`__)
* Expand the Overview page and use the Manaus data (`#51 <https://github.com/compgeolab/xlandsat/pull/51>`__)
* Fill missing and equalization in overlay tutorial (`#45 <https://github.com/compgeolab/xlandsat/pull/45>`__)
* Fix wrong mention of color in indices tutorial (`#44 <https://github.com/compgeolab/xlandsat/pull/44>`__)
* Rework and expand the composites tutorial (`#37 <https://github.com/compgeolab/xlandsat/pull/37>`__)
* Add a tutorial on how to overlay bands on RGB (`#33 <https://github.com/compgeolab/xlandsat/pull/33>`__)
* Make README preview image full width (`#26 <https://github.com/compgeolab/xlandsat/pull/26>`__)
* Add a logo for the project (`#43 <https://github.com/compgeolab/xlandsat/pull/43>`__)
* Add Community guides (`#27 <https://github.com/compgeolab/xlandsat/pull/27>`__)

Maintenance:

* Add Issue templates with a release checklist (`#58 <https://github.com/compgeolab/xlandsat/pull/58>`__)
* Add missing Scipy dependency (`#56 <https://github.com/compgeolab/xlandsat/pull/56>`__)
* Update Leo's affiliation to USP (`#50 <https://github.com/compgeolab/xlandsat/pull/50>`__)
* Fix version number for uploading to TestPyPI (`#48 <https://github.com/compgeolab/xlandsat/pull/48>`__)
* Fetch data files from GitHub instead of figshare (`#47 <https://github.com/compgeolab/xlandsat/pull/47>`__)
* Host sample data files on GitHub (`#46 <https://github.com/compgeolab/xlandsat/pull/46>`__)
* Add testing and support for Python 3.11 (`#35 <https://github.com/compgeolab/xlandsat/pull/35>`__)
* Use the tifffile plugin for IO instead of PIL (`#31 <https://github.com/compgeolab/xlandsat/pull/31>`__)
* Update jupyter-sphinx and add ipykernel (`#30 <https://github.com/compgeolab/xlandsat/pull/30>`__)
* Move the Authorship Guidelines to the lab manual (`#29 <https://github.com/compgeolab/xlandsat/pull/29>`__)

This release contains contributions from:

* Leonardo Uieda

Version 0.3.0
-------------

Released on: 2023/02/08

doi: https://doi.org/10.5281/zenodo.7619773

New features:

* Create a datasets module to automate downloading: https://github.com/compgeolab/xlandsat/pull/24
* Add pansharpening (Weighted Brovey Transform): https://github.com/compgeolab/xlandsat/pull/23

Documentation:

* Add a favicon image to the docs: https://github.com/compgeolab/xlandsat/pull/22

This release contains contributions from:

* Leonardo Uieda

Version 0.2.0
-------------

Released on: 2023/01/20

doi: https://doi.org/10.5281/zenodo.7553891

New features:

* Add the ``save_scene`` function to save a scene back to a tar file: https://github.com/compgeolab/xlandsat/pull/19

This release contains contributions from:

* Leonardo Uieda

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
