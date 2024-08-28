# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Functions for plotting data with ipyleaflet
"""
import base64
import io

import ipyleaflet

# Dependecy of ipyleaflet
import ipywidgets
import matplotlib.pyplot as plt
import pyproj


def _scene_boundaries_geodetic(scene):
    """
    Determine the boundaries of the scene in geodetic longitude and latitude

    Uses pyproj to project the UTM coordinates of the scene and get the
    geographic bounding box.

    Returns
    -------
    [w, e, s, n] : list of floats
        The west, east, south, north boundaries of the scene in degrees.
    """
    projection = pyproj.Proj(
        proj="utm", zone=scene.attrs["utm_zone"], ellps=scene.attrs["ellipsoid"]
    )
    west, south = projection(
        scene.easting.min().values, scene.northing.min().values, inverse=True
    )
    east, north = projection(
        scene.easting.max().values, scene.northing.max().values, inverse=True
    )
    return (west, east, south, north)


def plot_composite_leaflet(composite, dpi=70, leaflet_map=None, height="600px"):
    """
    Display a composite as an image overlay in an interactive HTML map

    Adds the composite to a Leaflet.js map, which can be displayed in a Jupyter
    notebook or HTML page. By default, adds a control widget for the opacity of
    the image overlay.

    Parameters
    ----------
    composite : :class:`xarray.DataArray`
        A composite, as generated by :func:`xlandsat.composite`.
    dpi : int
        The dots-per-inch resolution of the image.
    leaflet_map : :class:`ipyleaflet.Map`
        A Leaflet map instance to which the image overlay will be added. If
        None (default), a new map will be created. Pass an existing map to add
        the overlay to it.
    height : str
        The height of the map which is embedded in the HTML. Should contain the
        proper CSS units (px, em, rem, etc).

    Returns
    -------
    leaflet_map : :class:`ipyleaflet.Map`
        The map with the image overlay and opacity controls added to it.
    """
    west, east, south, north = _scene_boundaries_geodetic(composite)
    center = (0.5 * (north + south), 0.5 * (east + west))
    bounds = ((south, west), (north, east))
    # Create a plot of the composite with no decoration
    fig, ax = plt.subplots(1, 1, layout="constrained")
    composite.plot.imshow(ax=ax, add_labels=False)
    ax.axis("off")
    ax.set_aspect("equal")
    # Save the PNG to an in-memory buffer
    png = io.BytesIO()
    fig.savefig(png, bbox_inches="tight", dpi=dpi, pad_inches=0, transparent=True)
    plt.close(fig)
    # Create the image overlay with the figure as base64 encoded png
    image_overlay = ipyleaflet.ImageOverlay(
        url=f"data:image/png;base64,{base64.b64encode(png.getvalue()).decode()}",
        bounds=bounds,
    )
    image_overlay.name = (
        f"{composite.attrs["long_name"].title()} | {composite.attrs["title"]}"
    )
    # Create a map if one wasn't given
    if leaflet_map is None:
        leaflet_map = ipyleaflet.Map(
            center=center,
            scroll_wheel_zoom=True,
            layout={"height": height},
        )
        leaflet_map.add(ipyleaflet.ScaleControl(position="bottomleft"))
        leaflet_map.add(ipyleaflet.LayersControl(position="bottomright"))
        leaflet_map.add(ipyleaflet.FullScreenControl())
        leaflet_map.fit_bounds(bounds)
    # Add a widget to control the opacity of the image
    opacity_slider = ipywidgets.FloatSlider(
        description="Opacity:",
        min=0,
        max=1,
        step=0.1,
        value=1,
        readout_format=".1f",
        style={"description_width": "initial"},
        layout={"margin": "0 0 0 0.5rem"},
    )
    ipywidgets.jslink((opacity_slider, "value"), (image_overlay, "opacity"))
    leaflet_map.add(
        ipyleaflet.WidgetControl(widget=opacity_slider, position="topright")
    )
    leaflet_map.add(image_overlay)
    return leaflet_map