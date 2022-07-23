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
        Bağçeşehir öğrencileri tarafından tema'nın isteği doğrultusunda tema işbirliğiyle geliştirildi.
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
