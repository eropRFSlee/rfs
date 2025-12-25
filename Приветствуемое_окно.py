import streamlit as st

st.set_page_config(
    page_title="Главная страница",
    layout="wide"
)
st.markdown("""
<style>
    /* Основной фон приложения */
    .stApp {
        background-color: #204171;
    }
    
    /* Сайдбар */
    section[data-testid="stSidebar"] {
        background-color: #22305f;
    }
    
    /* Текст в сайдбаре */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Шапка */
    header {
        background-color: #204171 !important;
    }
    
    /* Основной контент - блок */
    .main .block-container {
        background-color: #2a4a80;  /* Светлее основного фона, но темнее белого */
        color: white !important;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    /* Белый текст во всех элементах основного контейнера */
    .main .block-container * {
        color: white !important;
    }
    
    /* Текст по умолчанию */
    p, span, div {
        color: white !important;
    }
    
    /* Заголовки */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    /* Элементы ввода и метки */
    label, input, select, textarea {
        color: white !important;
    }
    
    /* Кнопки в сайдбаре */
    section[data-testid="stSidebar"] button {
        color: white !important;
        border-color: white !important;
    }
    
    /* Подсветка активного элемента в сайдбаре */
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("Титульник")
st.write("Информация для РОИВ")
