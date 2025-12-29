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
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    /* ★★★ ОЧЕНЬ СПЕЦИФИЧНЫЕ ПРАВИЛА ДЛЯ ЗОЛОТИСТОГО ТЕКСТА ★★★ */
    /* Для всех текстовых элементов в основном окне */
    .main .block-container,
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4,
    .main .block-container h5,
    .main .block-container h6,
    .main .block-container p,
    .main .block-container div,
    .main .block-container span,
    .main .block-container label,
    .main [data-testid="stMarkdownContainer"],
    .main [data-testid="stMarkdownContainer"] *,
    .st-emotion-cache-16idsys p,
    .st-emotion-cache-16idsys h1,
    .st-emotion-cache-16idsys h2,
    .st-emotion-cache-16idsys h3,
    .st-emotion-cache-16idsys h4,
    .st-emotion-cache-16idsys h5,
    .st-emotion-cache-16idsys h6,
    .st-emotion-cache-16idsys div,
    .st-emotion-cache-16idsys span {
        color: #d3b37d !important;
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
            video {
        max-width: 700px !important;
        height: auto !important;
        border-radius: 10px !important;  /* Закругленные углы */
    }
</style>
""", unsafe_allow_html=True)

st.title("Боковая панель")
st.write("Для удобства можно увеличить или уменьшить размеры боковй панели")
st.video('боковая панель.mp4')
st.write("На панеле слева необходимо выбрать пункт 'Карта футбольных объектов'")
st.image('Сайдбар.png')

st.write("В выпадающем списке слева выберите свой регион")
st.image('Выбор региона.png')

st.write("После выбора региона происходит загрузка карты (в правом углу будет виден значок прогрузки), если карта долго не прогружается, необходимо обновить страницу")
st.image('Загрузка карты.png')

st.write("После правильных действий отобразится карта футбольных объектов Вашего региона")
st.image('После прогрузки карты.png')


st.title("Фукнционал карты")
st.write('На карте видны точки - футбольные объекты Вашего региона')
st.image('Карта общая.png')
st.write('Если навести курсор на точку и нажать на нее, отобразится информация об объекте')
st.write('Также доступен следующий функционал')
st.write('Изменить данные')
st.write('Не поле')
st.write('Дубликат')
st.write('Каждая из кнопок откроет соответствующую форму для заполнения анкеты')
st.video('Функционал точек.mp4')

st.write('Для отметки футбольного поля необходимо выбрать точку на карте, нажать на нее, после в окне нажать на кнопку "Здесь футбольное поле". Откроится форма для заполнения. Для удобства можно скопировать адрес и координаты.')
st.video('Функционал простановки нового поля.mp4')

st.title("Фильтры для карты")
st.write('На боковой панеле также доступны фильтры для отображения точек на карте')
st.image('Фильтры - все.png')


st.title("Выбор дисцпилины")
st.image('Выбор дисциплины.png')
st.write('В выпадающем списке отображаются все имеющиеся дисциплины по размеру футбольного поля')
st.title("Наличие в реестрах")

st.image('Наличие в реестрах.png')
st.write('В выпадающем списке отображаются источники информации по футбольным объектам')

st.title("Особенности")
st.image('Особенности.png')
st.write('В выпадающем списке доступна возможность выбрать наличие особеннсотей футбольного поля')

st.title("Сводная информация")
st.write('На боковой панеле приведена сводная информация по общему количеству футбольных объектов')
st.image("Сводная инфа.png")

