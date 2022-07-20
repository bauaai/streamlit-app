"""
Home page
"""

import streamlit as st
from PIL import Image


def app():
    """
    Main app that streamlit will render.
    """
    st.title("Uzaktan Algılama Verilerine Dayalı Orman Tahribatı İzleme Sistemi")

    st.markdown(
        """
Bu web aplikasyonu [streamlit](https://streamlit.io) kullanılarak orman
tarhibatının izlenmesi ve analiz edilebilmesi için TEMA işbirliğiyle,
[google earth engine](https://earthengine.google.com) verilerini esas
alarak yapılmıştır. Çalışmada [leafmap](https://leafmap.org),
[geemap](https://geemap.org) gibi açık kaynak haritalama kütüphaneleri kullanılmıştır.
        """
    )

    st.subheader("Örnek Çalışmalar")
    st.markdown(
        """
        Alt taraftaki çalışmalar Yangın Analizi web sayfası kullanılarak yapıldı.
        Kendi Çalışmalarınızı yaratmak için sol taraftaki menüden `Yangın Analizi`
        sekmesine tıklayınız.
    """
    )

    image1 = Image.open("assets/prefire.png")
    image2 = Image.open("assets/afterfire.png")
    image3 = Image.open("assets/grayscalednbr.png")
    image4 = Image.open("assets/classifieddnbr.png")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.image(image1, "Yangın Öncesi RGB", width=400, use_column_width="always")
        st.image(image3, "Gray Scale dNBR", width=400, use_column_width="always")

    with row1_col2:
        st.image(image2, "Yangın Sonrası RGB", width=400, use_column_width="always")
        st.image(image4, "Classified dNBR", width=400, use_column_width="always")
