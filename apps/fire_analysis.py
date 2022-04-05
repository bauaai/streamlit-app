"""
The page for fire analysis page.
"""

# Standard libraries
from io import StringIO
import datetime
from datetime import date
import tempfile
import os
import uuid

# Third party libraries
import streamlit as st
import geemap.foliumap as geemap
import ee
import folium
import geopandas as gpd

# Local libraries
from . import rois  # Why i am getting pylint error? code works fine.

IMAGE_COLLECTION = "COPERNICUS/S2"
MAP_WIDTH = 950
MAP_HEIGHT = 600
CRS = "epsg:4326"  # Coordinate Reference System


def map_search(folium_map):  # sourcery skip: use-named-expression
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


@st.cache
def uploaded_file_to_gdf(data):
    """
    The function to convert uploaded file to geodataframe.
    """
    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if not file_path.lower().endswith(".kml"):
        return gpd.read_file(file_path)

    gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"
    return gpd.read_file(file_path, driver="KML")


def app():
    # sourcery skip: remove-redundant-if, remove-redundant-pass, use-named-expression

    """
    The main app that streamlit will render for fire analysis page.
    """

    st.title("Yangın analizi")

    st.markdown(
        """
[Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/sentinel)
verilerini kullanarak orman yangınlarının incelenmesini sağlayan web aplikasyonu.
Bu uygulama [streamlit](https://streamlit.io), [geemap](https://geemap.org) ve
[Google Earth Engine](https://earthengine.google.com) kullanılarak oluşturuldu.
Daha fazla bilgi için, streamlit
[blog post](https://blog.streamlit.io/creating-satellite-timelapse-with-streamlit-and-earth-engine)
sayfasını ziyaret edebilirsiniz.
        """
    )

    row1_col1, row1_col2 = st.columns([2, 1])

    if st.session_state.get("zoom_level") is None:
        st.session_state["zoom_level"] = 4

    main_map = geemap.Map(
        basemap="ROADMAP",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
        plugin_LatLngPopup=False,
    )

    with row1_col1:
        st.info(
            "Adımlar: Harita üzerinde poligon çizin -> GeoJSON olarak export edin"
            "-> Uygulumaya upload edin"
            "-> Submit tuşuna tıklayın."
        )

        keyword = st.text_input("Bölge arayın:", "")
        if keyword:
            locations = geemap.geocode(keyword)
            if locations is not None and len(locations) > 0:
                str_locations = [str(g)[1:-1] for g in locations]
                location = st.selectbox("Bölge seçin:", str_locations)
                loc_index = str_locations.index(location)
                selected_loc = locations[loc_index]
                lat, lng = selected_loc.lat, selected_loc.lng
                folium.Marker(location=[lat, lng], popup=location).add_to(main_map)
                main_map.set_center(lng, lat, 12)
                st.session_state["zoom_level"] = 12

        main_map.to_streamlit(height=400)

    with row1_col2:
        data = st.file_uploader(
            "ROI olarak kullanmak için GeoJSON dosyası ekleyin 😇👇",
            type=["geojson", "kml", "zip"],
        )

        selected_roi = st.selectbox(
            "Çalışılacak roi'yi seçin veya GeoJSON dosyası yükleyin.",
            ["Yüklenilen GeoJSON"] + list(rois.fire_cases.keys()),
            index=0,
        )

        geometry = None
        if selected_roi == "Yüklenilen GeoJSON":  # rois coming from the user
            pre_fire_date = st.date_input(
                "Yangın başlangıç tarihi", date.today() - datetime.timedelta(days=1)
            )

            post_fire_date = st.date_input("Yangın bitiş tarihi", date.today())
            if data:
                geojson = StringIO(data.getvalue().decode("utf-8"))
                geometry = ee.Geometry(geojson)

        else:  # rois coming from fire_cases
            geometry = rois.fire_cases[selected_roi]["region"]
            pre_fire_date = rois.fire_cases[selected_roi]["date_range"][0]
            post_fire_date = rois.fire_cases[selected_roi]["date_range"][1]

    # now we have geometry and dates
    # also we need the geometry as ee.Geometry

    print(geometry, pre_fire_date, post_fire_date)
    image_collection = ee.ImageCollection(IMAGE_COLLECTION)
    print(image_collection)
