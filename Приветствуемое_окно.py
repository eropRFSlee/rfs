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
    
    /* Сайдбар - белый фон, черный текст */
    section[data-testid="stSidebar"] {
        background-color: white !important;
    }
    
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: black !important;
    }
    
    header {
        background-color: #204171 !important;
    }
    
    /* Главное окно */
    .main .block-container {
        background-color: #2a4a80;
        color: white !important;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    .main .block-container,
    .main .block-container * {
        color: white !important;
    }
    
    /* ★★★ ВСЕ КОМБОБОКСЫ - БЕЛЫЙ фон ★★★ */
    /* Фон самого комбобокса */
    [data-baseweb="select"] {
        background-color: white !important;
    }
    
    /* Внутренняя часть комбобокса */
    [data-baseweb="select"] > div {
        background-color: white !important;
    }
    
    /* Кнопка комбобокса */
    [data-baseweb="select"] [role="button"] {
        background-color: white !important;
    }
    
    /* ★★★ Текст в комбобоксах - ЧЁРНЫЙ ★★★ */
    [data-baseweb="select"] * {
        color: black !important;
    }
    
    /* Выбранное значение */
    [data-baseweb="select"] [aria-selected="true"] {
        color: black !important;
    }
    
    /* Выпадающий список */
    [role="listbox"] {
        background-color: white !important;
    }
    
    [role="option"] {
        color: black !important;
        background-color: white !important;
    }
    
    [role="option"]:hover {
        background-color: #f0f0f0 !important;
        color: black !important;
    }
    
    /* Убираем белый текст из комбобоксов в основном блоке */
    .main .block-container [data-baseweb="select"] * {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("Титульник")
st.write("Информация для РОИВ")
