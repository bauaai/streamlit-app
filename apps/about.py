"""
About page module
"""

import streamlit as st


def app():
    """
    About page app function
    """
    st.markdown("<h1 style='text-align: center; '>HAKKINDA</h1>", unsafe_allow_html=True)

    st.subheader("")

    st.markdown(
        """
        Katkı verenler bölümünde bulunan öğrenciler tarafından TEMA'nın işbirliğiyle geliştirilen bu uygulama, uzaktan algılama verilerine dayanarak
        orman tahribatının tespit ve analiz edilmesi amacıyla geliştirilmiştir. Uygulamada [Google Earth Engine](https://earthengine.google.com) kataloğunda bulunan
        [Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2) ve [Landsat-8](https://landsat.gsfc.nasa.gov/satellites/landsat-8/)
        uydularından elde edilen veriler kullanılmıştır. Elde edilen veriler [geemap](https://geemap.org) ve [leafmap](https://leafmap.org) gibi açık kaynak
        haritalama kütüphaneleri kullanılarak işlenmiş ve [streamlit](https://streamlit.io) kullanılarak internet sitesi haline getirilmiştir.
""")


    st.info(
        """
        Sentinel-2 verilerinden yararlanarak geliştirilen bu uygulama orman yangınlarının
        analiz edilmesi ve izlenmesi amacıyla [Osman](https://github.com/osbm),
        [Efe](https://github.com/EFCK) ve [Bilal](https://github.com/qimenez) tarafından
        TEMA işbirliğiyle hazırlandı..
"""
    )

    st.subheader("Sorumluluk Reddi Beyanı")
    st.markdown("""
    Bu çalışma ve içerdiği sorgu / analiz sonuçları tahmini değerler içermektedir. Veriler / sonuçlar, herhangi bir arazi gözlemine
    dayanmadan uydu görüntüleri üzerinden görüntü işleme yazılımlarıyla otomatik – yarı otomatik olarak elde edilmiş olduğundan,
    arazi gözlemleri ile uyumsuzluk gösterebilir.
    """)



    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Geliştirenler")
        st.write(
        """[Osman Faruk Bayram](https://github.com/osbm)  \n  [Efe Can Kırbıyık](https://github.com/EFCK)  \n  [Ahmet Bilal Barışman](https://github.com/qimenez)
        """
        )

    with col2:
        st.subheader("Katkı Verenler")
