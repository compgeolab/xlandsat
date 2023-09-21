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

Here's a quick example of loading and plotting this
[Landsat 9 scene from the city of Manaus, Brazil](https://doi.org/10.6084/m9.figshare.24167235.v1),
which is where the Solimões (brown water) and Negro (black water) rivers merge
to form the Amazon river:

```python
import xlandsat as xls
import matplotlib.pyplot as plt

# Download a sample Landsat 9 scene in EarthExplorer format
path_to_scene_file = xls.datasets.fetch_manaus()

# Load the data from the file into an xarray.Dataset
scene = xls.load_scene(path_to_scene_file)

# Make an RGB composite as an xarray.DataArray
rgb = xls.composite(scene, rescale_to=[0.02, 0.2])

# Plot the composite using xarray's plotting machinery
rgb.plot.imshow()

# Annotate the plot with the rich metadata xlandsat adds to the scene
plt.title(f"{rgb.attrs['title']}\n{rgb.attrs['long_name']}")
plt.axis("scaled")
plt.show()
```

<img src="https://raw.githubusercontent.com/compgeolab/xlandsat/main/doc/_static/readme-example.jpg" alt="RGB image showing the city on the left and the black waters of the Negro river merging with the brown waters of the Solimões river" width="100%">

## Project goals

* Loading single scenes in the EarthExplorer format.
* Provide some calculation, like composites, but leave most of the rest to the
  user and xarray.

Our goal is **not** to provide a solution for large-scale data processing.
Instead, our target is smaller scale analysis done on individual computers.

* For cloud-based data processing, see the [Pangeo Project](https://pangeo.io).
* For other satellites and more powerful features, use [Satpy](https://github.com/pytroll/satpy).

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
