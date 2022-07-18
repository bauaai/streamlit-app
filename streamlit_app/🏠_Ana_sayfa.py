"""
Home page
"""

import streamlit as st
from PIL import Image

#st.set_page_config(page_title="Yangın Analizi", page_icon="🔥", layout="wide")
st.set_page_config(
    layout="wide",
    page_title="Ana Sayfa",
    page_icon="🏠",
)


logo = Image.open("assets/tema-logo.jpg")
st.sidebar.image(logo, use_column_width=True)

st.sidebar.write("""Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium
optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis
obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam
nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,
tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit,
quia. Quo neque error repudiandae fuga?
""")

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
