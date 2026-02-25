import streamlit as st
st.markdown("""
<style>
    .stApp {
        background-color: #204171;
    }
    
    /* Сайдбар - белый фон, черный текст */
    section[data-testid="stSidebar"] {
        background-color: white !important;
    }
    
    /* ВСЕ элементы в сайдбаре - черный текст */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: black !important;
    }
    
    /* Переопределяем белый цвет для сайдбара */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown div,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4,
    section[data-testid="stSidebar"] .stMarkdown h5,
    section[data-testid="stSidebar"] .stMarkdown h6,
    section[data-testid="stSidebar"] .stWrite,
    section[data-testid="stSidebar"] .stWrite p,
    section[data-testid="stSidebar"] .stWrite span,
    section[data-testid="stSidebar"] .stWrite div,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
    section[data-testid="stSidebar"] .element-container,
    section[data-testid="stSidebar"] .sidebar-content,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: black !important;
    }
    
    /* Статистика с эмодзи в сайдбаре */
    section[data-testid="stSidebar"] .stMarkdown p:contains("🔵"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("🟡"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("🟢"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("🟣"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("🔴"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("⚪"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("⚫"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Всего объектов"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Типы точек"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Дополнительно"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Натуральных полей"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Искусственная трава"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Спортивное"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Доска"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Иное"),
    section[data-testid="stSidebar"] .stMarkdown p:contains("Нет информации") {
        color: black !important;
    }
    
    /* Селектбоксы в сайдбаре */
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: black !important;
    }
    
    /* Кнопки в сайдбаре */
    section[data-testid="stSidebar"] .stButton button {
        color: white !important;
        border-color: white !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Кнопки режима просмотра в сайдбаре */
    section[data-testid="stSidebar"] .stButton button[key="map_btn"],
    section[data-testid="stSidebar"] .stButton button[key="list_btn"] {
        color: black !important;
        border-color: #ccc !important;
    }
    
    section[data-testid="stSidebar"] .stButton button[key="map_btn"]:hover,
    section[data-testid="stSidebar"] .stButton button[key="list_btn"]:hover {
        background-color: #f0f0f0 !important;
    }
    
    header {
        background-color: #204171 !important;
    }
    
    /* ГЛАВНОЕ ОКНО - БЕЛЫЙ ТЕКСТ */
    .main .block-container {
        background-color: #2a4a80;
        color: white !important;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    /* ВСЕ элементы в основном окне - белый цвет */
    .main .block-container *:not([data-baseweb="select"] *):not([role="listbox"] *):not([role="option"] *):not(section[data-testid="stSidebar"] *) {
        color: white !important;
    }
    
    /* Исключения для некоторых элементов */
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4,
    .main .block-container h5,
    .main .block-container h6,
    .main .block-container p,
    .main .block-container span,
    .main .block-container div:not([data-baseweb="select"]):not([role="listbox"]):not([role="option"]):not(section[data-testid="stSidebar"]),
    .main .block-container label {
        color: white !important;
    }
    
    /* ===== УСИЛЕННЫЕ СТИЛИ ДЛЯ КОМБОБОКСОВ ===== */
    /* ★★★ ВСЕ КОМБОБОКСЫ - БЕЛЫЙ фон, черный текст, ellipsis, защита от темной темы ★★★ */
    [data-baseweb="select"] {
        background-color: white !important;
        color-scheme: light !important; /* Принудительно светлая схема */
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: white !important;
        color-scheme: light !important;
    }
    
    [data-baseweb="select"] [role="button"] {
        background-color: white !important;
        color-scheme: light !important;
        min-height: 38px !important;
    }
    
    /* Убираем скроллы и добавляем ellipsis для текста внутри кнопки */
    [data-baseweb="select"] [role="button"] span {
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        max-width: 100% !important;
        display: block !important;
        color: black !important;
        padding-right: 24px !important; /* Место для стрелки */
    }
    
    /* Все текстовые элементы внутри комбобокса */
    [data-baseweb="select"] * {
        color: black !important;
        background-color: white !important;
        color-scheme: light !important;
    }
    
    /* Контейнер с текстом - принудительно убираем скроллы */
    [data-baseweb="select"] [role="button"] div {
        overflow: hidden !important;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        color: black !important;
        scrollbar-width: none !important; /* Firefox */
        -ms-overflow-style: none !important; /* IE/Edge */
        max-width: 100% !important;
        width: 100% !important;
        display: inline-block !important;
    }
    
    /* Дополнительная защита для всех внутренних элементов */
    [data-baseweb="select"] [role="button"] div *,
    [data-baseweb="select"] [role="button"] span,
    [data-baseweb="select"] [role="button"] span * {
        overflow: hidden !important;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        max-width: 100% !important;
    }
    
    /* Скрываем скроллы у всех возможных контейнеров */
    [data-baseweb="select"] *::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    [data-baseweb="select"] * {
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    
    /* Выбранный элемент */
    [data-baseweb="select"] [aria-selected="true"] {
        color: black !important;
        background-color: #f0f0f0 !important;
    }
    
    /* Выпадающий список */
    [role="listbox"] {
        background-color: white !important;
        color-scheme: light !important;
        border: 1px solid #ccc !important;
        max-height: 300px !important;
        overflow-y: auto !important; /* Вертикальный скролл для списка */
        overflow-x: hidden !important; /* Убираем горизонтальный */
    }
    
    /* Элементы выпадающего списка */
    [role="option"] {
        color: black !important;
        background-color: white !important;
        white-space: normal !important; /* В списке текст может переноситься */
        word-wrap: break-word !important;
        padding: 8px 12px !important;
        border-bottom: 1px solid #f0f0f0 !important;
    }
    
    [role="option"]:hover {
        background-color: #f0f0f0 !important;
        color: black !important;
    }
    
    [role="option"][aria-selected="true"] {
        background-color: #e0e0e0 !important;
        color: black !important;
    }
    
    /* Фикс для темной темы браузера - максимальный приоритет */
    .main .block-container [data-baseweb="select"] *,
    .stSelectbox *,
    div[data-testid="stSelectbox"] * {
        color: black !important;
        background-color: white !important;
    }
    
    /* Дополнительная защита для сайдбара */
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: black !important;
        background-color: white !important;
    }
    
    /* Стрелка выпадающего списка */
    [data-baseweb="select"] [role="button"] svg {
        fill: #666 !important;
        color: #666 !important;
    }
    
    /* ФИНАЛЬНЫЙ ФИКС - перебиваем все возможные скроллы */
    .stSelectbox div[data-baseweb="select"] *,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
    div[role="combobox"] * {
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    
    .stSelectbox div[data-baseweb="select"] *::-webkit-scrollbar,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] *::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    /* Фикс для сайдбара */
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        scrollbar-width: none !important;
    }
    /* ===== КОНЕЦ ИСПРАВЛЕННЫХ СТИЛЕЙ ===== */
    
    .stTextInput input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    .stTextInput label {
        color: white !important;
    }
    
    .stButton button {
        color: white !important;
        border-color: white !important;
    }
    
    .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSpinner + div,
    .stSpinner > div > div,
    .stAlert,
    .stInfo,
    .stWarning,
    .stSuccess,
    .stError,
    .element-container .stMarkdown p,
    .element-container .stMarkdown span,
    .element-container .stMarkdown div {
        color: white !important;
    }
    
    div[data-testid="stToast"],
    div[data-testid="stNotification"],
    .st-emotion-cache-1q7spjk {
        color: white !important;
    }
    
    .stAlert *,
    .stInfo *,
    .stWarning *,
    .stSuccess *,
    .stError * {
        color: white !important;
    }
    
    .stInfo,
    .stWarning,
    .stSuccess,
    .stError {
        border-color: white !important;
    }
    
    .card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    
    .card * {
        color: #000000 !important;
    }
    
    .color-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }
    
    .color-label {
        display: inline-flex;
        align-items: center;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: #000000 !important;
    }
    
    .color-blue {
        background-color: #3B82F6;
    }
    
    .color-yellow {
        background-color: #FFA500;
    }
    
    .color-green {
        background-color: #10B981;
    }
    
    .color-purple {
        background-color: #9444EF;
    }
    
    .color-red {
        background-color: #EF4444;
    }
    
    .stSpinner > div {
        border-color: white transparent transparent transparent !important;
    }
    
    .stSpinner + div {
        color: white !important;
    }
    
    .main .block-container {
        overflow-y: auto !important;
    }
    
    .stMarkdown, .stHtml {
        overflow-y: auto !important;
    }
    
    iframe {
        max-height: none !important;
    }
    
    /* Скролл только у всего сайдбара, убираем скроллы у внутренних элементов */
    section[data-testid="stSidebar"] > div:first-child {
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }
    
    /* Убираем скроллы у всех внутренних элементов */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .element-container,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stWrite,
    section[data-testid="stSidebar"] .st-br,
    section[data-testid="stSidebar"] .st-c0,
    section[data-testid="stSidebar"] .st-d5 {
        overflow-y: visible !important;
        overflow-x: visible !important;
    }
    
    /* Разрешаем скролл только для выпадающих списков */
    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    section[data-testid="stSidebar"] [role="listbox"] * {
        overflow-y: auto !important;
    }
    
    /* Нормальный скролл только у сайдбара */
    section[data-testid="stSidebar"] > div:first-child {
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }
    
    /* Убираем скроллы у всех внутренних элементов, КРОМЕ selectbox */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .element-container,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stWrite {
        overflow-y: visible !important;
        overflow-x: visible !important;
    }
    
    /* НЕ ТРОГАЕМ selectbox - оставляем как есть */
    /* Убираем только если есть лишние скроллы у самих контейнеров selectbox */
    section[data-testid="stSidebar"] [data-baseweb="select"] {
        overflow-y: visible !important;
    }
</style>
""", unsafe_allow_html=True)
st.header("Обратная связь")

st.write("""
Если у Вас возникли вопросы по работе приложения, Вы обнаружили ошибку в функционале или у Вас есть предложения по улучшению, обращайтесь удобным для Вас способом.""")

st.subheader("Контактная информация:")

# Используем markdown для более структурированного отображения
st.markdown(
    """
- **Почта:** [li_ea@rfs.ru](mailto:li_ea@rfs.ru)
- **Телефон:** +7(950) 284-84-83 / +7(993) 264-84-63
- **Telegram:** [https://t.me/eropliya](https://t.me/eropliya)
"""
)   

st.markdown("---")
# QR-код
st.image("инструкция/qr код.png")


