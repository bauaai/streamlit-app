"""
The page for create timelapse
"""

from datetime import date

import geemap.foliumap as geemap
import streamlit as st

from streamlit_app import utils, satellite_params, rois

CRS = "epsg:4326"  # Coordinate Reference System
DAY_WINDOW = 6
INITIAL_DATE_WINDOW = 6


st.set_page_config(page_title="Timelapse", page_icon="🕒", layout="wide")

st.sidebar.title("Bu timelapse hakkında ")

st.sidebar.write(
    """Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium
optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis
obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam
nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,
tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit,
quia. Quo neque error repudiandae fuga?
"""
)

st.title("Timelapse")
st.markdown("Belirlenmiş iki tarih arasında gif üreten sistem.")

_, col2 = st.columns([2, 1])

if st.session_state.get("zoom_level") is None:
    st.session_state["zoom_level"] = 4

main_map = geemap.Map(
    basemap="ROADMAP",
    plugin_Draw=True,
    Draw_export=True,
    locate_control=True,
    plugin_LatLngPopup=False,
)

with col2:
    data = st.file_uploader(
        "ROI olarak kullanmak için GeoJSON dosyası ekleyin 😇👇",
        type=["geojson", "kml", "zip"],
    )

    selected_roi = st.selectbox(
        "Çalışılacak roi'yi seçin veya GeoJSON dosyası yükleyin.",
        ["Yüklenilen dosyayı seç"] + list(rois.fire_cases.keys()),
        index=0,
    )

    if selected_roi != "Yüklenilen dosyayı seç":  # rois coming from fire_cases
        st.session_state["roi"] = rois.fire_cases[selected_roi]["region"]

    elif data:  # rois coming from users
        gdf = utils.uploaded_file_to_gdf(data)
        st.session_state["roi"] = geemap.gdf_to_ee(gdf)

    selected_satellite = st.selectbox(
        "Çalışılacak uyduyu seçin", list(satellite_params.satellite.keys())
    )

    if selected_satellite == "sentinel-2":
        st.session_state["satellite"] = satellite_params.satellite["sentinel-2"]

    elif selected_satellite == "landsat-8":
        st.session_state["satellite"] = satellite_params.satellite["landsat-8"]

    selected_rgb = st.selectbox(
        "Görüntülenme rengini seçin", ["True Color", "False Color", "dNBR"]
    )

    if selected_rgb == "True Color":
        st.session_state["vis_params"] = "True Color"

    elif selected_rgb == "False Color":
        st.session_state["vis_params"] = "False Color"

    elif selected_rgb == "dNBR":
        st.session_state["vis_params"] = "dNBR"

    slider_date = st.slider(
        "Tarih Aralığı",
        value=[st.session_state["satellite"]["launch"], date.today()],
    )

    slider_fps = st.slider("FPS", min_value=1, max_value=60)

    print(slider_date, slider_fps)
    with st.expander("Grafikleri görüntüle"):
        st.write("Grafikler yükleniyor...")
