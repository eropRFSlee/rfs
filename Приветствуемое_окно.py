import streamlit as st

st.set_page_config(
    page_title="Главная страница",
    layout="wide"
)
st.markdown("""
<style>
    .stApp {
        background-color: #204171;
    }
    .main .block-container {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
            header {
        background-color: #204171 !important;
    }
    
    /* Сайдбар */
    section[data-testid="stSidebar"] {
        background-color: #22305f;
    }
</style>
""", unsafe_allow_html=True)
st.title("Титульник")
st.write("Информация для РОИВ")

