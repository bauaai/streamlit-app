"""
The page for fire analysis page.
"""

import datetime
from datetime import date

import ee
import folium
import geemap.foliumap as geemap
import streamlit as st

from streamlit_app import utils, satellite_params, rois

st.set_page_config(page_title="Yangın Analizi", page_icon="🔥", layout="wide")

st.sidebar.title("Bu yangın sayfası hakkında ")

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

SENTINEL = satellite_params.satellite["sentinel-2"]["name"]
SENTINEL_LAUNCH = satellite_params.satellite["sentinel-2"]["launch"]
MAP_HEIGHT = 600
CRS = "epsg:4326"  # Coordinate Reference System
DAY_WINDOW = datetime.timedelta(days=6)
rgb_vis_params = satellite_params.satellite["sentinel-2"]["rgb_vis_params"]
false_color_vis_params = satellite_params.satellite["sentinel-2"][
    "false_color_vis_params"
]


col1, col2 = st.columns([2, 1])

if st.session_state.get("zoom_level") is None:
    st.session_state["zoom_level"] = 4

main_map = geemap.Map(
    basemap="ROADMAP",
    plugin_Draw=True,
    Draw_export=True,
    locate_control=True,
    plugin_LatLngPopup=False,
)

pre_fire = date.today() - 2 * DAY_WINDOW
post_fire = date.today() - DAY_WINDOW

with col2:  # right column
    data = st.file_uploader(
        "ROI olarak kullanmak için şekil dosyası ekleyin.",
        type=["geojson", "kml", "zip", "kmz"],
    )

    selected_roi = st.selectbox(
        "Çalışılacak ROI'yi seçin veya eklenilmiş dosyayı yükleyin.",
        ["Yüklenilen dosyayı seç"] + list(rois.fire_cases.keys()),
        index=0,
    )

    if selected_roi != "Yüklenilen dosyayı seç":  # rois coming from fire_cases
        st.session_state["roi"] = rois.fire_cases[selected_roi]["region"]
        pre_fire = date.fromisoformat(rois.fire_cases[selected_roi]["date_range"][0])
        post_fire = date.fromisoformat(rois.fire_cases[selected_roi]["date_range"][1])

    elif data:  # if rois coming from users
        st.session_state["roi"] = utils.uploaded_file_to_gdf(data)

    pre_fire = st.date_input(  # to update dates according to the user selection
        "Yangın başlangıç tarihi",
        pre_fire,
        min_value=SENTINEL_LAUNCH,
        max_value=date.today() - 2 * DAY_WINDOW,
    )

    post_fire = st.date_input(
        "Yangın bitiş tarihi",
        post_fire,
        min_value=SENTINEL_LAUNCH,
        max_value=date.today() - DAY_WINDOW,
    )

    dates = {
        "prefire_start": str(pre_fire - DAY_WINDOW),
        "prefire_end": str(pre_fire),
        "postfire_start": str(post_fire),
        "postfire_end": str(post_fire + DAY_WINDOW),
    }

    with st.expander("Grafikleri görüntüle"):
        empty_graph_text = st.empty()
        empty_graph_text.text("Grafikler yükleniyor ...")

        # empty_chart = st.empty()

    with st.expander("Çıktıları indir"):

        st.write("Çıktılar zip olarak hazırlanıyor...")

with col1:  # left column
    st.info(
        "Adımlar: Harita üzerinde poligon çizin ➡ GeoJSON olarak export edin"
        " ➡ Uygulamaya upload edin"
        " ➡ Tarih aralığı seçin."
    )

    utils.map_search(main_map)

    if st.session_state.get("roi"):
        main_map.center_object(st.session_state["roi"])
        # lets not add the roi as a marker on the map
        # main_map.add_layer(st.session_state["roi"], name="ROI", opacity=0.5)

        imagery = ee.ImageCollection(SENTINEL)

        prefire = imagery.filterDate(
            dates["prefire_start"], dates["prefire_end"]
        ).filterBounds(st.session_state["roi"])

        postfire = imagery.filterDate(
            dates["postfire_start"], dates["postfire_end"]
        ).filterBounds(st.session_state["roi"])

        pre_mos = prefire.median().clip(st.session_state["roi"])
        post_mos = postfire.median().clip(st.session_state["roi"])

        pre_nbr = pre_mos.normalizedDifference(["B8", "B12"])
        post_nbr = post_mos.normalizedDifference(["B8", "B12"])

        delta_nbr = pre_nbr.subtract(post_nbr).multiply(
            1000
        )  # why are we mutliplying by 1000?

        with open("data/sld_intervals.xml", "r", encoding="utf-8") as file:
            sld_intervals = file.read()

        main_map.add_layer(pre_mos, rgb_vis_params, "Yangın öncesi görüntüler")
        main_map.add_layer(post_mos, rgb_vis_params, "Yangın sonrası görüntüler")

        main_map.add_layer(pre_mos, false_color_vis_params, "Yangın öncesi false color")
        main_map.add_layer(
            post_mos, false_color_vis_params, "Yangın sonrası false color"
        )
        delta_nbr_sld = delta_nbr.sldStyle(sld_intervals)
        main_map.add_layer(delta_nbr_sld, name="dNBR")

        folium.map.LayerControl("topright", collapsed=False).add_to(main_map)

        # add legend to the map
        main_map.add_legend(
            title="dNBR Sınıfı",
            legend_dict={
                "Veri Yok": "ffffff",
                "Yüksek yeniden büyüme": "7a8737",
                "Düşük yeniden büyüme": "acbe4d",
                "Yanmamış": "0ae042",
                "Düşük Tahribat": "fff70b",
                "Orta-Düşük tahribat": "ffaf38",
                "Orta-yüksek tahribat": "ff641b",
                "Yüksek tahribat": "a41fd6",
            },
        )

        # after this calculate the charts and add them to the right panel
        empty_graph_text.write(delta_nbr.getInfo())

    main_map.to_streamlit(height=600)
