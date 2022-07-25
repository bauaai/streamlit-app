"""
Page for utilities
"""

import json
import os
import tempfile
import uuid
import xml.etree.ElementTree as et
import zipfile

import ee
import folium
import geemap.foliumap as geemap
import numpy as np
import pandas as pd
import streamlit as st
from lxml import etree
import plotly.graph_objects as go

delta_nbr_colors = {
    "Veri Yok": "ffffff",
    "Yüksek yeniden büyüme": "7a8737",
    "Düşük yeniden büyüme": "acbe4d",
    "Yanmamış": "0ae042",
    "Düşük Tahribat": "fff70b",
    "Orta-Düşük tahribat": "ffaf38",
    "Orta-yüksek tahribat": "ff641b",
    "Yüksek tahribat": "a41fd6",
}

ndvi_colors = {
    "palette": [
        "#d73027",
        "#f46d43",
        "#fdae61",
        "#fee08b",
        "#d9ef8b",
        "#a6d96a",
        "#66bd63",
        "#1a9850",
    ]
}

NAMES = ['Veri Yok', 'Yüksek tahribat', 'Orta-yüksek tahribat', 'Orta-Düşük tahribat', 'Düşük Tahribat','Yanmamış', 'Düşük yeniden büyüme', 'Yüksek yeniden büyüme']

@st.experimental_memo
def calculate_dnbr_dataframe(number_of_pixels):
    """
    The function to calculate the DNBR dataframe.
    """
    names = NAMES
    values = np.array(number_of_pixels)  # pixel numbers
    hectares = values * 900 / 10000  # convert to hectares
    percenteges = hectares / np.sum(hectares) * 100  # calculate percenteges

    dataframe = pd.DataFrame(
        {"dNBR sınıfları": names, "hektar": hectares, "yüzde": percenteges}
    )
    dataframe = dataframe.style.hide_index().format(precision=2)

    return dataframe.to_html()


@st.experimental_memo
def get_plotly_charts(number_of_pixels):
    """
    The function to generate the plotly charts.
    """
    colors = delta_nbr_colors
    fig = go.Figure(
        data=[
            go.Pie(
                labels= NAMES,
                values=list(number_of_pixels),
                sort=False,
                marker=dict(colors=["ffffff","a41fd6","ff641b","ffaf38","fff70b","0ae042","acbe4d","7a8737"]),
            )
        ],
    )

    return fig


def get_pixel_counts(image, geometry):
    """
    The function to get the pixel counts of classes in an dNBR image.
    """
    # pylint: disable=no-member
    thresholds = ee.Image([-1000, -251, -101, 99, 269, 439, 659, 2000])
    classified = image.lt(thresholds).reduce("sum").toInt()
    allpix = classified.updateMask(classified)
    pixstats = allpix.reduceRegion(
        reducer=ee.Reducer.count(),  # count pixels in a single class
        geometry=geometry,
        scale=30,
    )

    allpixels = ee.Number(pixstats.get("sum"))  # extract pixel count as a number
    allpixels.getInfo()
    results = []

    results = []
    for i in range(8):
        single_mask = classified.updateMask(classified.eq(i))  # mask a single class
        stats = single_mask.reduceRegion(
            reducer=ee.Reducer.count(),  # count pixels in a single class
            geometry=geometry,
            scale=30,
        )
        pix = ee.Number(stats.get("sum"))

        results.append(pix.getInfo())
    return results


def map_search(folium_map: geemap.Map) -> None:  # sourcery skip: use-named-expression
    """
    The function to generate the search box above the map.
    """
    keyword = st.text_input("Bölge arayın:", "")
    if keyword:
        locations = geemap.geocode(keyword)
        if locations is not None and len(locations) > 0:
            str_locations = [str(g)[1:-1] for g in locations]
            location = st.selectbox("Bölge seçin:", str_locations)
            loc_index = str_locations.index(location)
            selected_loc = locations[loc_index]
            lat, lng = selected_loc.lat, selected_loc.lng
            folium.Marker(location=[lat, lng], popup=location).add_to(folium_map)
            folium_map.set_center(lng, lat, 12)
            st.session_state["zoom_level"] = 12


@st.experimental_memo
def kml_geometry_export(file_path):
    """
    The function to export the geometry of a KML file.
    """
    # pylint: disable=c-extension-no-member
    root = etree.parse(file_path)

    for i in root.iter():
        path = root.getelementpath(i).split("}")[0] + "}"

    tree = et.parse(file_path)
    root = tree.getroot()

    name = root.find(f".//*{path}coordinates")
    geolist = name.text.strip().split(" ")

    geometry = []

    for i in geolist:
        current = i.split(",")
        # en az 3 point içermesi lazım yoksa EEException error veriyor.
        geometry.append([float(current[0]), float(current[1])])

    return ee.Geometry.Polygon(geometry)


@st.experimental_memo
def uploaded_file_to_gdf(data):
    """
    The function to convert uploaded file to geodataframe.
    """
    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    # gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

    if file_path.lower().endswith(".kml"):

        return kml_geometry_export(file_path)

    if file_path.lower().endswith(".kmz"):
        # unzip it to get kml file
        in_kmz = os.path.abspath(file_path)
        out_dir = os.path.dirname(in_kmz)
        out_kml = os.path.join(out_dir, "doc.kml")
        with zipfile.ZipFile(in_kmz, "r") as zip_ref:
            zip_ref.extractall(out_dir)

        return kml_geometry_export(out_kml)

    if file_path.lower().endswith(".geojson"):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.loads(file.read())

        return ee.Geometry.Polygon(data["features"][0]["geometry"]["coordinates"][0])
