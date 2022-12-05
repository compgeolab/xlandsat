<h1 align="center">xlandsat</h1>
<p align="center"><strong>Load Landsat remote sensing images into xarray.</strong></p>
<p align="center">
<a href="https://www.compgeolab.org/xlandsat"><strong>Documentation</strong> (latest)</a> •
<a href="https://www.compgeolab.org/xlandsat/dev"><strong>Documentation</strong> (main branch)</a> •
<a href="https://www.compgeolab.org"><strong>CompGeoLab</strong></a>
</p>

<p align="center">
<a href="https://pypi.python.org/pypi/xlandsat"><img src="http://img.shields.io/pypi/v/xlandsat.svg?style=flat-square" alt="Latest version on PyPI"></a>
<a href="https://github.com/conda-forge/xlandsat-feedstock"><img src="https://img.shields.io/conda/vn/conda-forge/xlandsat.svg?style=flat-square" alt="Latest version on conda-forge"></a>
<a href="https://codecov.io/gh/compgeolab/xlandsat"><img src="https://img.shields.io/codecov/c/github/compgeolab/xlandsat/main.svg?style=flat-square" alt="Test coverage status"></a>
<a href="https://pypi.python.org/pypi/xlandsat"><img src="https://img.shields.io/pypi/pyversions/xlandsat.svg?style=flat-square" alt="Compatible Python versions."></a>
<a href="https://doi.org/10.5281/zenodo.7395473"><img src="https://img.shields.io/badge/doi-10.5281%2Fzenodo.7395473-blue?style=flat-square" alt="DOI used for citations"></a>
</p>

## About

**xlandsat** is Python library for loading Landsat scenes downloaded from
[USGS EarthExplorer](https://earthexplorer.usgs.gov) into `xarray.Dataset`
containers.
We take care of reading the metadata from the `*_MTL.txt` files provided by
EarthExplorer and organizing the bands into a single data structure for easier
manipulation, processing, and visualization.

## Example

Here's a quick example of loading this [Landsat 8 scene from the Brumadinho
tailings dam disaster in Brazil](https://doi.org/10.6084/m9.figshare.21665630.v1):

```python
import xlandsat as xls
import pooch  # for downloading the sample scene

# Download the scene as a tar archive
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
```

![RGB map showing the flooded plain after the dam collapse as light brown.]( https://raw.githubusercontent.com/compgeolab/xlandsat/main/doc/_static/readme-example.jpg)

## Project goals

* Loading single scenes in the EarthExplorer format.
* Provide some calculation, like composites, but leave most of the rest to the
  user and xarray.

Our goal is not to provide a solution for large-scale data processing. Instead,
our target is smaller scale analysis done on individual computers. For
cloud-based data processing, see the [Pangeo Project](https://pangeo.io).

## Project status

**xlandsat is ready for use but still changing.**
This means that we sometimes break backwards compatibility as we try to
improve the software based on user experience, new ideas, better design
decisions, etc. Please keep that in mind before you update xlandsat to a newer
version.

**We welcome feedback and ideas!** This is a great time to bring new ideas on
how we can improve the project.
Submit [issues on GitHub](https://github.com/compgeolab/xlandsat/issues).

## License

This is free software: you can redistribute it and/or modify it under the terms
of the **MIT License**. A copy of this license is provided in
[`LICENSE.txt`](https://github.com/compgeolab/xlandsat/blob/main/LICENSE.txt).
