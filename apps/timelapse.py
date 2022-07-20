"""
The page for create timelapse
"""

import datetime
from datetime import date
import os

import geemap.foliumap as geemap
import streamlit as st

from . import rois, satellite_params, utils

CRS = "epsg:4326"  # Coordinate Reference System
DAY_WINDOW = datetime.timedelta(days=6)
INITIAL_DATE_WINDOW = 6


def app():
    """
    The main app that streamlit will render for create timelapse page.
    """

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

    st.session_state["vis_params"] = None
    st.session_state["satellite"] = "sentinel-2"
    pre_fire = date.today() - 2 * DAY_WINDOW
    post_fire = date.today() - DAY_WINDOW

    with col2:  # right column
        data = st.file_uploader(
            "ROI olarak kullanmak için şekil dosyası ekleyin 😇👇",
            type=["geojson", "kml", "kmz"],
        )

        selected_roi = st.selectbox(
            "Çalışılacak ROI'yi seçin veya şekil dosyası yükleyin.",
            ["Yüklenilen dosyayı seç"] + list(rois.fire_cases.keys()),
            index=0,
        )

        if selected_roi != "Yüklenilen dosyayı seç":  # rois coming from fire_cases
            st.session_state["roi"] = rois.fire_cases[selected_roi]["region"]
            pre_fire = date.fromisoformat(
                rois.fire_cases[selected_roi]["date_range"][0]
            )
            post_fire = date.fromisoformat(
                rois.fire_cases[selected_roi]["date_range"][1]
            )

        elif data:  # if rois coming from users
            st.session_state["roi"] = utils.uploaded_file_to_gdf(data)

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
            st.session_state["vis_params"] = satellite_params.satellite[
                selected_satellite
            ]["rgb_vis_params"]

        elif selected_rgb == "False Color":
            st.session_state["vis_params"] = satellite_params.satellite[
                selected_satellite
            ]["false_color_vis_params"]

        elif selected_rgb == "dNBR":
            st.session_state["vis_params"] = "dNBR"

        pre_fire = st.date_input(  # to update dates according to the user selection
            "Yangın başlangıç tarihi",
            pre_fire,
            min_value=st.session_state["satellite"]["launch"],
            max_value=date.today() - 2 * DAY_WINDOW,
        )

        post_fire = st.date_input(
            "Yangın bitiş tarihi",
            post_fire,
            min_value=st.session_state["satellite"]["launch"],
            max_value=date.today() - DAY_WINDOW,
        )

        dates = {
            "prefire_start": str(pre_fire - DAY_WINDOW),
            "prefire_end": str(pre_fire),
            "postfire_start": str(post_fire),
            "postfire_end": str(post_fire + DAY_WINDOW),
        }

        timelapse_title = ""
        if st.session_state["satellite"] == "landsat-8":
            timelapse_title = "Landsat-8 Timelapse"
        elif st.session_state["satellite"] == "sentinel-2":
            timelapse_title = "Sentinel-2 Timelapse"

        with st.form("submit_form"):

            roi = None
            if st.session_state.get("roi") is not None:
                roi = st.session_state.get("roi")
            out_gif = geemap.temp_file_path(".gif")

            title = st.text_input("Timelapse'in başlığı: ", timelapse_title)

            with st.expander("Timelaps'i özelleştirme:"):

                speed = st.slider("Fps:", 1, 30, 5)

                progress_bar_color = st.color_picker("Bar rengi:", "#0000ff")

                font_size = st.slider("Font büyüklüğü:", 10, 50, 30)

                font_color = st.color_picker("Font rengi:", "#ffffff")

                apply_fmask = st.checkbox("Bulut maskeleme uygulansın mı?", True)

                font_type = st.selectbox(
                    "Başlık için font tipini seçin:",
                    ["arial.ttf", "alibaba.otf"],
                    index=0,
                )

                mp4 = st.checkbox("MP4 olarak kaydedilsin mi?", True)

            empty_text = st.empty()
            empty_image = st.empty()
            empty_video = st.container()
            submitted = st.form_submit_button("Submit")
            if submitted:

                if selected_roi == "Uploaded GeoJSON" and data is None:
                    empty_text.warning("Öncelikle roi yükleyiniz.")

                else:

                    empty_text.text("Computing... Please wait...")
                    try:
                        if st.session_state["satellite"] == "landsat-8":
                            out_gif = geemap.landsat_timelapse(
                                roi=selected_roi,
                                out_gif=out_gif,
                                start_date=dates["prefire_start"],
                                end_date=dates["postfire_end"],
                                vis_params=st.session_state["vis_params"],
                                apply_fmask=apply_fmask,
                                frames_per_second=speed,
                                date_format=None,
                                title=title,
                                title_xy=("2%", "90%"),
                                add_text=True,
                                text_xy=("2%", "2%"),
                                text_sequence=None,
                                font_type=font_type,
                                font_size=font_size,
                                font_color=font_color,
                                add_progress_bar=True,
                                progress_bar_color=progress_bar_color,
                                progress_bar_height=5,
                                loop=0,
                                mp4=mp4,
                            )

                        elif st.session_state["satellite"] == "sentinel-2":
                            out_gif = geemap.sentinel2_timelapse(
                                roi=selected_roi,
                                out_gif=out_gif,
                                start_date=dates["prefire_start"],
                                end_date=dates["postfire_end"],
                                vis_params=st.session_state["vis_params"],
                                apply_fmask=apply_fmask,
                                frames_per_second=speed,
                                date_format=None,
                                title=title,
                                title_xy=("2%", "90%"),
                                add_text=True,
                                text_xy=("2%", "2%"),
                                text_sequence=None,
                                font_type=font_type,
                                font_size=font_size,
                                font_color=font_color,
                                add_progress_bar=True,
                                progress_bar_color=progress_bar_color,
                                progress_bar_height=5,
                                loop=0,
                                mp4=mp4,
                            )

                        geemap.sentinel2_timelapse()

                    except:
                        empty_text.error("Bir hata meydana geldi.")
                        st.stop()

                    if out_gif is not None and os.path.exists(out_gif):

                        empty_text.text(
                            "Right click the GIF to save it to your computer👇"
                        )
                        empty_image.image(out_gif)

                        out_mp4 = out_gif.replace(".gif", ".mp4")
                        if mp4 and os.path.exists(out_mp4):
                            with empty_video:
                                st.text(
                                    "Right click the MP4 to save it to your computer👇"
                                )
                                st.video(out_gif.replace(".gif", ".mp4"))

                    else:
                        empty_text.error(
                            "Something went wrong. You probably requested too much data. Try reducing the ROI or timespan."
                        )

    with col1:  # left column
        st.info(
            "Adımlar: Harita üzerinde poligon çizin ➡ GeoJSON olarak export edin"
            " ➡ Uygulamaya upload edin"
            " ➡ Tarih aralığı seçin."
        )

        utils.map_search(main_map)

        if st.session_state.get("roi"):
            main_map.center_object(st.session_state["roi"])

        main_map.to_streamlit(height=600)
