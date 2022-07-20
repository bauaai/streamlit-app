"""
Streamlit App
"""
# pylint: disable=wrong-import-order

import streamlit as st
from apps import fire_analysis, home, timelapse
from streamlit_option_menu import option_menu
from PIL import Image

from typing import Callable


st.set_page_config(page_title="Yangın Analizi", page_icon="🔥", layout="wide")


apps = [
    {"func": home.app, "title": "Ana Sayfa", "icon": "house"},
    {"func": fire_analysis.app, "title": "Yangın Analizi", "icon": "geo-alt"},
    {"func": timelapse.app, "title": "Timelapse", "icon": "hourglass-split"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    DEFAULT_INDEX = titles.index(params["page"][0].lower())
else:
    DEFAULT_INDEX = 0

with st.sidebar:
    logo = Image.open("assets/tema-logo.jpg")
    st.image(logo, use_column_width=True)

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
        Sentinel-2 verilerinden yararlanarak geliştirilen bu uygulama orman yangınlarının
        analiz edilmesi ve izlenmesi amacıyla [Osman](https://github.com/osbm),
        [Efe](https://github.com/EFCK) ve [Bilal](https://github.com/qimenez) tarafından
        TEMA işbirliğiyle hazırlandı..
        """
    )


for app in apps:
    if app["title"] == selected:
        page_func: Callable = app["func"]
        page_func()
        break
