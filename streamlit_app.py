"""
Streamlit App
"""
import streamlit as st
from streamlit_option_menu import option_menu
from apps import fire_analysis, home

st.set_page_config(page_title="Yangın Analizi", page_icon="🔥", layout="wide")


apps = [
    {"func": home.app, "title": "Ana Sayfa", "icon": "house"},
    {"func": fire_analysis.app, "title": "Yangın Analizi", "icon": "geo-alt"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    DEFAULT_INDEX = titles.index(params["page"][0].lower())
else:
    DEFAULT_INDEX = 0

with st.sidebar:
    selected = option_menu(
        "TEMA",
        options=titles,
        icons=icons,
        menu_icon="list",
        default_index=DEFAULT_INDEX,
    )

    st.sidebar.title("Hakkında")
    st.sidebar.info(
        """
        Bu uygulama [Osman](https://github.com/osbm), [Efe](https://github.com/EFCK) ve
        [Bilal](https://github.com/qimenez) tarafından yazılmıştır.

    [Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/sentinel)
    verilerini kullanarak orman yangınlarının incelenmesini sağlayan web aplikasyonu.
    Bu uygulama [streamlit](https://streamlit.io), [geemap](https://geemap.org) ve
    [Google Earth Engine](https://earthengine.google.com) kullanılarak oluşturuldu.
        """
    )


for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
