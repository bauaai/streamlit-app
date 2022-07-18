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

import streamlit as st
from lxml import etree


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


def kml_geometry_export(file_path):
    """
    The function to export the geometry of a KML file.
    """

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
