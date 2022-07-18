"""
Streamlit App
"""
# pylint: disable=wrong-import-order

import streamlit as st
from apps import fire_analysis, home, timelapse, about
#from streamlit_option_menu import option_menu
from PIL import Image

from typing import Callable


st.set_page_config(page_title="Yangın Analizi", page_icon="🔥", layout="wide")


page_names_to_funcs = {
    "Home Page": home.app,
    "compute dNBR": fire_analysis.app,
    "generate timelapse": timelapse.app,
    "About": about.app,
}

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]


selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


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
