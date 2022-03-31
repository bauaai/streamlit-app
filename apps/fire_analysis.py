"""
The page for fire analysis page.
"""
import random
import streamlit as st
import geemap.foliumap as geemap
import ee
import geopandas as gpd  # to change rois to geojson types

from .rois import fire_cases  # Why i am getting pylint error? code works fine.

IMAGE_COLLECTION = "COPERNICUS/S2"
MAP_WIDTH = 950
MAP_HEIGHT = 600
CRS = "epsg:4326"  # Coordinate Reference System


def app():
    """
    The main app that streamlit will render for fire analysis page.
    """
    st.title("Yangın analizi")

    main_map = geemap.Map()
    name, value = random.choice(list(fire_cases.items()))

    region = value["region"]
    region = gpd.GeoDataFrame(index=[0], crs=CRS, geometry=[region])
    region = geemap.geopandas_to_ee(region, geodesic=False)

    region = ee.Geometry(region)
    st.markdown(name)

    main_map.add_layer(region)
    main_map.to_streamlit(MAP_WIDTH, MAP_HEIGHT)
