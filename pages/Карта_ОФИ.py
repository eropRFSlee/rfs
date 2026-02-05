import streamlit as st
import pandas as pd
import json
import requests
import time
import uuid
from io import BytesIO
import base64

WEBHOOK = 'https://drlk.rfs.ru/rest/205/b8fz7f8gjkxwstkm/'
ENTITY_TYPE_ID = 142

# Константы для повторных попыток
MAX_RETRIES = 3
RETRY_DELAY = 2  # секунды
CONNECTION_TIMEOUT = 30
READ_TIMEOUT = 60

# ---------------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Реестр ОФИ", 
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
    
    /* ГЛАВНОЕ ОКНО - ЗОЛОТОЙ ТЕКСТ */
    .main .block-container {
        background-color: #2a4a80;
        color: #FFD700 !important; /* Золотой цвет */
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    /* ВСЕ элементы в основном окне - золотой цвет */
    .main .block-container *:not([data-baseweb="select"] *):not([role="listbox"] *):not([role="option"] *) {
        color: #FFD700 !important;
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
    .main .block-container div:not([data-baseweb="select"]):not([role="listbox"]):not([role="option"]),
    .main .block-container label {
        color: #FFD700 !important;
    }
    
    /* ★★★ ВСЕ КОМБОБОКСЫ - БЕЛЫЙ фон, черный текст ★★★ */
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
    
    /* Текст в комбобоксах в основном блоке - черный */
    .main .block-container [data-baseweb="select"] * {
        color: black !important;
    }
    
    /* Текст в input полях поиска */
    .stTextInput input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    .stTextInput label {
        color: #FFD700 !important;
    }
    
    /* Кнопки в основном окне */
    .stButton button {
        color: #FFD700 !important;
        border-color: #FFD700 !important;
    }
    
    .stButton button:hover {
        background-color: rgba(255, 215, 0, 0.1) !important;
    }
    
    /* ★★★ ВСЕ ИНФОРМАЦИОННЫЕ СООБЩЕНИЯ В ОСНОВНОМ ОКНЕ - ЗОЛОТОЙ ★★★ */
    /* Сообщение "Загрузка данных..." и другие текстовые элементы */
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
        color: #FFD700 !important;
    }
    
    /* Специально для информационных сообщений */
    div[data-testid="stToast"],
    div[data-testid="stNotification"],
    .st-emotion-cache-1q7spjk {
        color: #FFD700 !important;
    }
    
    /* Текст внутри информационных блоков */
    .stAlert *,
    .stInfo *,
    .stWarning *,
    .stSuccess *,
    .stError * {
        color: #FFD700 !important;
    }
    
    /* Границы информационных сообщений */
    .stInfo,
    .stWarning,
    .stSuccess,
    .stError {
        border-color: #FFD700 !important;
    }
    
    /* Стили для карточек объектов */
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
    
    /* Стили для цветового индикатора */
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
    
    /* Стили для спиннера */
    .stSpinner > div {
        border-color: #FFD700 transparent transparent transparent !important;
    }
    
    /* Текст статуса загрузки */
    .stSpinner + div {
        color: #FFD700 !important;
    }
    
    /* Заголовки в сайдбаре */
    .sidebar-content h1,
    .sidebar-content h2,
    .sidebar-content h3,
    .sidebar-content h4,
    .sidebar-content h5,
    .sidebar-content h6 {
        color: black !important;
    }
    
    /* Параграфы и текст в сайдбаре */
    .sidebar-content p,
    .sidebar-content span,
    .sidebar-content div {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

FULL_BALLOONS_DATA = []

# Функция для отправки запроса с повторными попытками
def send_request_with_retry(url, params, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url, 
                params=params, 
                timeout=(CONNECTION_TIMEOUT, READ_TIMEOUT)
            )
            return response, attempt + 1
        except requests.exceptions.ConnectTimeout:
            print(f"  ⏳ Таймаут соединения (попытка {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.ReadTimeout:
            print(f"  ⏳ Таймаут чтения (попытка {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.ConnectionError as e:
            print(f"  🔌 Ошибка соединения (попытка {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  ⚠️ Другая ошибка (попытка {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
    
    return None, max_retries

# Функция для загрузки данных из Битрикса (ТОЛЬКО РЕГИОН 24)
def load_bitrix_data(REGION_NUMBER):
    all_items = []
    start = 0  # Начинаем с первого элемента

    while True:
        # Если REGION_NUMBER = 0, загружаем все данные без фильтра
        if REGION_NUMBER == 0:
            params = {
                'entityTypeId': ENTITY_TYPE_ID,
                'start': start
                # НЕТ ФИЛЬТРА ПО РЕГИОНУ
            }
        else:
            # Иначе добавляем фильтр по региону
            params = {
                'entityTypeId': ENTITY_TYPE_ID,
                'start': start,
                f'filter[ufCrm6_1767014564]': REGION_NUMBER  # Фильтр по номеру региона
            }
        
        # Используем функцию с повторными попытками
        response, attempt_used = send_request_with_retry(
            f'{WEBHOOK}crm.item.list', 
            params
        )
        
        # Если все попытки неудачны
        if response is None:
            print(f"  ❌ Не удалось получить данные после {MAX_RETRIES} попыток")
            break
        
        try:
            data = response.json()
        except Exception as e:
            print(f"  ❌ Ошибка при разборе JSON: {e}")
            # Если это была последняя страница, выходим
            if attempt_used < MAX_RETRIES:
                # Пробуем еще раз с теми же параметрами
                continue
            else:
                break
        
        # Проверяем, есть ли результат в ответе
        if 'result' in data and 'items' in data['result']:
            batch = data['result']['items']
            all_items.extend(batch)  # Добавляем пачку в общий список
            
            # Условие выхода: если в пачке меньше 50, это последняя страница
            if len(batch) < 50:
                break
            
            # Увеличиваем start на количество полученных элементов для следующей страницы
            start += len(batch)
        else:
            # Если нет результатов или ошибка в ответе
            print(f"  ⚠️ Некорректный ответ от API: {data.get('error', 'No error message')}")
            break
    
    return all_items

# Функция для обработки данных
def process_data(all_items):
    clear_data = []
    for i in range(len(all_items)):
        under_lst = []
        under_lst.append(all_items[i]['ufCrm6_1767015754'] if all_items[i]['ufCrm6_1767015754'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6FullName'] if all_items[i]['ufCrm6FullName'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6ShortName'] if all_items[i]['ufCrm6ShortName'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014546'] if all_items[i]['ufCrm6_1767014546'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014564'] if all_items[i]['ufCrm6_1767014564'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767018331'] if all_items[i]['ufCrm6_1767018331'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768300125944'] if all_items[i]['ufCrm6_1768300125944'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014622'] if all_items[i]['ufCrm6_1767014622'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768300173280'] if all_items[i]['ufCrm6_1768300173280'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768300553359'] if all_items[i]['ufCrm6_1768300553359'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768300847565'] if all_items[i]['ufCrm6_1768300847565'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301117660'] if all_items[i]['ufCrm6_1768301117660'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014657585'] if all_items[i]['ufCrm6_1767014657585'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014665209'] if all_items[i]['ufCrm6_1767014665209'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301185476'] if all_items[i]['ufCrm6_1768301185476'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014674'] if all_items[i]['ufCrm6_1767014674'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301287324'] if all_items[i]['ufCrm6_1768301287324'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301403770'] if all_items[i]['ufCrm6_1768301403770'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301417514'] if all_items[i]['ufCrm6_1768301417514'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301428170'] if all_items[i]['ufCrm6_1768301428170'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768468056'] if all_items[i]['ufCrm6_1768468056'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768301567690'] if all_items[i]['ufCrm6_1768301567690'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767014692'] if all_items[i]['ufCrm6_1767014692'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768303689332'] if all_items[i]['ufCrm6_1768303689332'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1767018403'].replace(',', ''))
        under_lst.append(all_items[i]['ufCrm6_1768304361743'] if all_items[i]['ufCrm6_1768304361743'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768312479608'] if all_items[i]['ufCrm6_1768312479608'] not in ('','N') else '-')
        under_lst.append(all_items[i]['ufCrm6_1768564635'] if all_items[i]['ufCrm6_1768564635'] not in ('','N') else '-')

        clear_data.append(under_lst)
    
    return clear_data

# Функция для определения цвета точки
def get_point_color(status_of_work, in_reestr):
    if str(status_of_work) == '1':
        return '#EF4444', '🔴 Внесли изменения, в стадии рассмотрения'
    elif str(status_of_work) == '2':
        return '#9444EF', '🟣 Добавили новое поле, в стадии рассмотрения'
    elif in_reestr == 1:
        return '#3B82F6', '🔵 Есть в РОИВ, но нет в ЦП'
    elif in_reestr == 2:
        return '#FFA500', '🟡 Есть только в ЦП'
    else:
        return '#10B981', '🟢 Есть в РОИВ и в ЦП'

# Функция для получения CSS класса цвета
def get_color_class(status_of_work, in_reestr):
    if str(status_of_work) == '1':
        return 'color-red', '🔴 Внесли изменения, в стадии рассмотрения'
    elif str(status_of_work) == '2':
        return 'color-purple', '🟣 Добавили новое поле, в стадии рассмотрения'
    elif in_reestr == 1:
        return 'color-blue', '🔵 Есть в РОИВ, но нет в ЦП'
    elif in_reestr == 2:
        return 'color-yellow', '🟡 Есть только в ЦП'
    else:
        return 'color-green', '🟢 Есть в РОИВ и в ЦП'

# Инициализация session_state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.all_items = None
    st.session_state.clear_data = None
    st.session_state.current_region = None
    st.session_state.last_region = None
    st.session_state.force_reload = False
    st.session_state.widget_reset_key = 0  # Ключ для сброса виджетов
    st.session_state.map_refresh_key = str(uuid.uuid4())  # Уникальный ключ для карты
    st.session_state.map_refresh_counter = 0  # Счетчик обновлений карты
    st.session_state.last_data_update = None  # Время последнего обновления данных
    st.session_state.view_mode = 'map'  # Режим просмотра: 'map' или 'list'
    st.session_state.copied_id = None  # Для отслеживания скопированного ID
    st.session_state.search_query = ''  # Поисковый запрос
    st.session_state.search_triggered = False  # Флаг для отслеживания нажатия Enter

# Создаем одну кнопку обновления в сайдбаре ДО выбора региона

st_select_region = st.sidebar.selectbox("Выберите свой регион", ['Регионы',\
    '01 Республика Адыгея',
    '02 Республика Башкортостан',
    '03 Республика Бурятия',
    '04 Республика Алтай',
    '05 Республика Дагестан',
    '06 Республика Ингушетия',
    '07 Кабардино-Балкарская Республика',
    '08 Республика Калмыкия',
    '09 Карачаево-Черкесская Республика',
    '10 Республика Корелия',
    '11 Республика Коми',
    '12 Республика Марий Эл',
    '13 Республика Мордовия',
    '14 Республика Саха (Якутия)',
    '15 Республика Северная Осетия — Алания',
    '16 Республика Татарстан',
    '17 Республика Тыва',
    '18 Удмуртская Республика',
    '19 Республика Хакасия',
    '20 Чеченская Республика',
    '21 Чувашская Республика',
    '22 Алтайский край',
    '23 Краснодарский край',
    '24 Красноярский край',
    '25 Приморский край',
    '26 Ставропольский край',
    '27 Хабаровский край',
    '28 Амурская область',
    '29 Архангельская область',
    '30 Астраханская область',
    '31 Белгородская область',
    '32 Брянская область',
    '33 Владимирская область',
    '34 Волгоградская область',
    '35 Вологодская область',
    '36 Воронежская область',
    '37 Ивановская область',
    '38 Иркутская область',
    '39 Калининградская область',
    '40 Калужская область',
    '41 Камчатский край',
    '42 Кемеровская область',
    '43 Кировская область',
    '44 Костромская область',
    '45 Курганская область',
    '46 Курская область',
    '47 Ленинградская область',
    '48 Липецкая область',
    '49 Магаданская область',
    '50 Московская область',
    '51 Мурманская область',
    '52 Нижегородская область',
    '53 Новгородская область',
    '54 Новосибирская область',
    '55 Омская область',
    '56 Оренбургская область',
    '57 Орловская область',
    '58 Пензенская область',
    '59 Пермский край',
    '60 Псковская область',
    '61 Ростовская область',
    '62 Рязанская область',
    '63 Самарская область',
    '64 Саратовская область',
    '65 Сахалинская область',
    '66 Свердловская область',
    '67 Смоленская область',
    '68 Тамбовская область',
    '69 Тверская область',
    '70 Томская область',
    '71 Тульская область',
    '72 Тюменская область',
    '73 Ульяновская область',
    '74 Челябинская область',
    '75 Забайкальский край',
    '76 Ярославская область',
    '77 Москва',
    '78 Санкт-Петербург',
    '79 Еврейская автономная область',
    '83 Ненецкий автономный округ',
    '86 Ханты-Мансийский автономный округ — Югра',
    '87 Чукотский автономный округ',
    '89 Ямало-Ненецкий автономный округ'
])

# Кнопка в сайдбаре для перезагрузки данных
if st_select_region != 'Регионы':
    if st_select_region == 'Сибирь':
        current_region_number = 0
        st_select_region = '000'
    else:
        current_region_number = int(st_select_region[0:2])
    
    # Переносим кнопку "Обновить карту и данные" в сайдбар

    if st.sidebar.button("🔄 Обновить данные", key="refresh_all_btn"):
        # 1. Загружаем новые данные из Битрикса
        st.session_state.force_reload = True
        # 2. Обновляем карту (черные/серые точки исчезнут)
        st.session_state.map_refresh_key = str(uuid.uuid4())
        st.session_state.map_refresh_counter += 1
        st.session_state.last_data_update = time.time()  # Запоминаем время обновления
        # 3. Используем JavaScript для обновления страницы
        st.markdown("""
        <script>
            window.location.reload();
        </script>
        """, unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------------------------------------------
    # ПЕРЕМЕЩАЕМ КНОПКИ ВЫБОРА РЕЖИМА В САЙДБАР ПОСЛЕ ВЫБОРА РЕГИОНА
    st.sidebar.markdown("---")
    st.sidebar.write("**Режим просмотра:**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Карта", key="map_btn" if st.session_state.view_mode == 'map' else "secondary", 
                     help="Переключить на карту", use_container_width=True):
            st.session_state.view_mode = 'map'
            st.rerun()
    with col2:
        if st.button("Список", key="list_btn" if st.session_state.view_mode == 'list' else "secondary",
                     help="Переключить на список", use_container_width=True):
            st.session_state.view_mode = 'list'
            st.rerun()  
    
    # Загружаем данные если они еще не загружены, изменился регион или принудительное обновление
    if (not st.session_state.data_loaded or 
        st.session_state.current_region != current_region_number or 
        st.session_state.clear_data is None or
        st.session_state.force_reload):
        
        with st.spinner("Загрузка данных..."):
            st.session_state.all_items = load_bitrix_data(current_region_number)
            st.session_state.clear_data = process_data(st.session_state.all_items)
            st.session_state.data_loaded = True
            st.session_state.current_region = current_region_number
            st.session_state.last_region = current_region_number
            st.session_state.force_reload = False
    

    
    # Используем данные из session_state
    clear_data = st.session_state.clear_data
    
    #----------------------------------------------------------------
    data = pd.DataFrame(data=clear_data, columns = ['РФС_ID', 'Полное (официальное) название объекта', 
    'Короткое (спортивное) название объекта', 'Регион', 'Номер региона', 'Адрес', 'Контактное лицо', 'Собственник (ОГРН)',
    'Управляющая компания (ОГРН)', 'Пользователь (ОГРН)', 'Тип Объекта ', 'Дисциплина ','Длина футбольного поля',
    'Ширина футбольного поля', 'Конструктивная особенность', 'Тип покрытия', 'Количество мест для зрителей', 'Наличие дренажа',
    'Наличие подогрева', 'Наличие табло', 'Наличие раздевалок', 'Год ввода в эксплуатацию/год капитального ремонта', 'Наличие в реестрах',
      'Статус работы', 'Широта и долгота','Дисциплина_2', 'id_egora','То, что заполнили РОИВ'])
    
    data[['Широта', 'Долгота']] = data['Широта и долгота'].str.split(r'\s+', expand=True)

    data['Широта'] = pd.to_numeric(data['Широта'], errors='coerce')
    data['Долгота'] = pd.to_numeric(data['Долгота'], errors='coerce')

    all_object = data.shape[0]

    one_object = data[data['Наличие в реестрах'] == 1].shape[0]
    two_object = data[data['Наличие в реестрах'] == 2].shape[0]
    three_object = data[data['Наличие в реестрах'] == 3].shape[0]
    cnt_tablo = data[data['Наличие табло'] == 'Y'].shape[0]
    cnt_drinage = data[data['Наличие дренажа'] == 'Y'].shape[0]
    cnt_dress_room = data[data['Наличие раздевалок'] =='Y'].shape[0]
    cnt_heat = data[data['Наличие подогрева'] =='Y'].shape[0]

    condition_reestr = []
    condition_reestr.append('Все')
    condition_reestr.append('🔵 Есть в РОИВ, но нет в ЦП')  # Синий
    condition_reestr.append('🟡 Есть только в ЦП')          # Желтый
    condition_reestr.append('🟢 Есть в РОИВ и в ЦП')       # Зеленый
    condition_reestr.append('🟣 Добавили новое поле, в стадии рассмотрения')  # Фиолетовый
    condition_reestr.append('🔴 Внесли изменения, в стадии рассмотрения')       # Красный
    
    conditional_size = []

    for x in sorted(data['Дисциплина_2'].unique()):
        if x != '-':  # Убираем '-'
            conditional_size.append(x)
    under_list_size = ['Все']

    if '11x11' in conditional_size:
        under_list_size.append([conditional_size[conditional_size.index('11x11')]])
        conditional_size.remove('11x11')
    if ('6x6' in conditional_size) or ('7x7' in conditional_size)  or ('8x8' in conditional_size)  or ('Спортивная площадка' in conditional_size):
        under_list_size.append(conditional_size[:])

    if len(under_list_size) > 2:
        lst_to_combo = [under_list_size[0],str(under_list_size[1])[1:-2].replace("'",""), str(under_list_size[2])[1:-2].replace("'","")]
        lst_to_combo.append('Зал')
    else:
        lst_to_combo = [under_list_size[0],str(under_list_size[1])[1:-2].replace("'","")]
        lst_to_combo.append('Зал')

    # -------------------------------------------------------------------------------------------------------------

    # Добавляем список для фильтра по типу покрытия (в раздел с другими фильтрами)
    conditional_dop = ['Все']
    conditional_dop.append('Наличие табло')
    conditional_dop.append('Наличие дренажа')
    conditional_dop.append('Наличие раздевалок')
    conditional_dop.append('Наличие подогрева')
    conditional_dop.append('Натуральное')
    conditional_dop.append('Искусственная трава')
    conditional_dop.append('Спортивное (резина, крошка и тп)') 
    conditional_dop.append('Доска (паркет)') 
    conditional_dop.append('Иное') 
    conditional_dop.append('Нет информации') 

    # -------------------------------------------------------------------------------------------------------------

    # Создаем ключи для виджетов, зависящие от региона и ключа сброса
    st_select_desciplyne = st.sidebar.selectbox(
        "Выбор дисциплины", 
        lst_to_combo,
        key=f"discipline_{current_region_number}_{st.session_state.widget_reset_key}"
    )
    st.sidebar.markdown("---")

    # ДОБАВЛЯЕМ НОВЫЙ ФИЛЬТР ПО ТИПУ ПОКРЫТИЯ
    st_select_covering = st.sidebar.selectbox(
        "Фильтр по типу покрытия/особенностям",
        conditional_dop,
        key=f"covering_{current_region_number}_{st.session_state.widget_reset_key}"
    )
    st.sidebar.markdown("---")
    st_select_reestr = st.sidebar.selectbox(
        "Фильтр по цветам точек", 
        condition_reestr,
        key=f"reestr_{current_region_number}_{st.session_state.widget_reset_key}"
    )

    # -------------------------------------------------------------------------------------------------------------

    # Применяем фильтры
    original_data = data.copy()  # Сохраняем исходные данные для статистики

    if st_select_reestr == '🔴 Внесли изменения, в стадии рассмотрения':
        data = data[data['Статус работы'] == '1']
    elif st_select_reestr == '🟣 Добавили новое поле, в стадии рассмотрения':
        data = data[data['Статус работы'] == '2']
    elif st_select_reestr == '🔵 Есть в РОИВ, но нет в ЦП':
        data = data[(data['Наличие в реестрах'] == 1) & (data['Статус работы'] != '1') & (data['Статус работы'] != '2')]
    elif st_select_reestr == '🟡 Есть только в ЦП':
        data = data[(data['Наличие в реестрах'] == 2) & (data['Статус работы'] != '1') & (data['Статус работы'] != '2')]
    elif st_select_reestr == '🟢 Есть в РОИВ и в ЦП':
        data = data[(data['Наличие в реестрах'] == 3) & (data['Статус работы'] != '1') & (data['Статус работы'] != '2')]

    if st_select_desciplyne != 'Все':
        if st_select_desciplyne == '11x11':
            data = data[data['Дисциплина_2'].isin([lst_to_combo[1]])]
        elif st_select_desciplyne =='Зал':
            data = data[data['Дисциплина_2'].isin(['Зал'])]
        else:
            data = data[data['Дисциплина_2'].isin(lst_to_combo[2].split(', '))]

    # ДОБАВЛЯЕМ ПРИМЕНЕНИЕ ФИЛЬТРА ПО ТИПУ ПОКРЫТИЯ
    if st_select_covering == 'Натуральное':
        data = data[data['Тип покрытия'] == 'Натуральное']
    elif st_select_covering == 'Искусственная трава':
        data = data[data['Тип покрытия'] == 'Искусственная трава']
    elif st_select_covering == 'Спортивное (резина, крошка и тп)':
        data = data[data['Тип покрытия'] == 'Спортивное (резина, крошка и тп)']
    elif st_select_covering == 'Доска (паркет)':
        data = data[data['Тип покрытия'] == 'Доска (паркет)']
    elif st_select_covering == 'Иное':
        data = data[data['Тип покрытия'] == 'Иное']
    elif st_select_covering == 'Нет информации':
        data = data[data['Тип покрытия'] == 'Нет информации']
    elif st_select_covering == 'Наличие табло':
        data = data[data['Наличие табло'] == 'Y']
    elif st_select_covering == 'Наличие дренажа':
        data = data[data['Наличие дренажа'] == 'Y']
    elif st_select_covering == 'Наличие раздевалок':
        data = data[data['Наличие раздевалок'] == 'Y']
    elif st_select_covering == 'Наличие подогрева':
        data = data[data['Наличие подогрева'] == 'Y']

    # -------------------------------------------------------------------------------------------------------------
    
    # ДОБАВЛЕН ПОИСК ПО КЛЮЧЕВЫМ СЛОВАМ С ИСПРАВЛЕННОЙ ЛОГИКОЙ
    # Создаем контейнер для поиска
    search_container = st.container()
    
    with search_container:
        # Используем key для управления состояния поля поиска
        search_query = st.text_input(
            "Поиск",
            value=st.session_state.get('search_query', ''),
            placeholder="Введите название, адрес, контакт и т.д. (нажмите Enter для поиска)",
            label_visibility="collapsed",
            key="search_input_field"
        )
    
    # Обработка нажатия Enter и очистки поля
    # Если поле поиска пустое, очищаем session_state.search_query
    if search_query == "" and st.session_state.search_query != "":
        st.session_state.search_query = ""
        # Используем rerun для немедленного обновления
        st.rerun()
    
    # Если в поле есть текст, сохраняем его в session_state
    elif search_query != "" and search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
    
    # Применяем поисковый фильтр ко всем данным (и для карты, и для списка)
    filtered_data_for_display = data.copy()
    if st.session_state.search_query:
        search_lower = st.session_state.search_query.lower()
        search_mask = (
            filtered_data_for_display['Полное (официальное) название объекта'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Короткое (спортивное) название объекта'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Адрес'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Контактное лицо'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Собственник (ОГРН)'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Управляющая компания (ОГРН)'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Пользователь (ОГРН)'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Тип Объекта '].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Тип покрытия'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Год ввода в эксплуатацию/год капитального ремонта'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered_data_for_display['Дисциплина_2'].astype(str).str.lower().str.contains(search_lower, na=False)
        )
        filtered_data_for_display = filtered_data_for_display[search_mask]
        
        # Показываем количество найденных объектов
        st.markdown(f'<p style="color: #FFD700;">Найдено объектов по запросу "{st.session_state.search_query}": {len(filtered_data_for_display)}</p>', unsafe_allow_html=True)
    
    # Проверяем режим просмотра
    if st.session_state.view_mode == 'list':
        
        # Сохраняем все данные для поиска
        st.session_state.all_filtered_data = filtered_data_for_display.copy()
        
        # Пагинация
        items_per_page = 50
        total_items = len(filtered_data_for_display)
        
        # Если данных больше, чем на одну страницу, показываем пагинацию
        if total_items > items_per_page:
            # Определяем количество страниц
            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            # Создаем селектор для выбора страницы
            page_options = [f"Страница {i+1}" for i in range(total_pages)]
            st.write('Выбор страницы')
            selected_page = st.selectbox(
                "",
                page_options,
                key=f"page_selector_{current_region_number}"
            )
            
            # Определяем выбранный номер страницы
            page_number = page_options.index(selected_page)
            
            # Вычисляем индексы для текущей страницы
            start_idx = page_number * items_per_page
            end_idx = min((page_number + 1) * items_per_page, total_items)
            
            # Получаем данные для текущей страницы
            page_data = filtered_data_for_display.iloc[start_idx:end_idx]
            
        else:
            # Если все помещается на одну страницу
            page_data = filtered_data_for_display
            total_pages = 1
            page_number = 0
        
        # Подготавливаем данные для JavaScript из page_data
        objects_data = []
        for index, row in page_data.iterrows():
            # Подготавливаем id_egora
            id_egora_value = '-'
            if pd.notna(row['id_egora']):
                try:
                    # Пробуем преобразовать в int
                    if isinstance(row['id_egora'], (int, float)):
                        id_egora_int = int(float(str(row['id_egora'])))
                        id_egora_value = str(id_egora_int)
                    else:
                        id_egora_value = str(row['id_egora']).strip()
                except:
                    id_egora_value = str(row['id_egora']).strip()
            
            # Определяем цвет точки
            status_of_work = row['Статус работы'] if pd.notna(row['Статус работы']) else '0'
            in_reestr = row['Наличие в реестрах'] if pd.notna(row['Наличие в реестрах']) else 0
            color_class, color_description = get_color_class(status_of_work, in_reestr)
            
            # Обработка информации для объектов со статусом работы '1' или '2'
            provided_data = ""
            info = row['То, что заполнили РОИВ'] if pd.notna(row['То, что заполнили РОИВ']) else ""
            
            if status_of_work in ('1', '2') and info:
                to_slovar = str(info).replace('<br>', '|').split('|')
                
                if status_of_work == '1' and len(to_slovar) >= 11:
                    slovar = {
                        'Полное(официальное) название объекта': to_slovar[0],
                        'Короткое (спортивное) название объекта': to_slovar[1],
                        'Адрес': to_slovar[2],
                        'Широта и долгота': to_slovar[3],
                        'Длина': to_slovar[4],
                        'Ширина': to_slovar[5],
                        'Тип покрытия': to_slovar[6],
                        'Отправитель': to_slovar[7],
                        'Подтвердить': to_slovar[8] if to_slovar[8] == 'Y' else '',
                        'Удалить': to_slovar[9] if to_slovar[9] == 'Y' else '',
                        'Зал/не зал': to_slovar[10] if to_slovar[10] == 'Y' else '',
                        'Комментарий': to_slovar[11],
                        'Номер региона': to_slovar[12]
                    }
                elif status_of_work == '2' and len(to_slovar) >= 9:
                    slovar = {
                        'Полное(официальное) название объекта': to_slovar[0],
                        'Короткое (спортивное) название объекта': to_slovar[1],
                        'Адрес': to_slovar[2],
                        'Широта и долгота': to_slovar[3],
                        'Длина': to_slovar[4],
                        'Ширина': to_slovar[5],
                        'Тип покрытия': to_slovar[6],
                        'Отправитель': to_slovar[7],
                        'Зал/не зал': to_slovar[8] if to_slovar[8] == 'Y' else '',
                        'Комментарий':  to_slovar[9],
                        'Номер региона': to_slovar[-1]
                    }
                
                if 'slovar' in locals():
                    result_parts = []
                    for key, value in slovar.items():
                        if value != '' and value is not None:
                            result_parts.append(f'{key}: <strong>{value}</strong>')

                    if result_parts:
                        provided_data = '<br>'.join(result_parts)
            
            # Подготавливаем все данные с целочисленными значениями размеров
            length_val = str(row['Длина футбольного поля']) if pd.notna(row['Длина футбольного поля']) else '-'
            width_val = str(row['Ширина футбольного поля']) if pd.notna(row['Ширина футбольного поля']) else '-'
            
            # Пытаемся преобразовать к целым числам
            try:
                if length_val != '-' and float(length_val).is_integer():
                    length_val = str(int(float(length_val)))
                if width_val != '-' and float(width_val).is_integer():
                    width_val = str(int(float(width_val)))
            except:
                pass
            
            full_info = {
                'fn': str(row['Полное (официальное) название объекта']) if pd.notna(row['Полное (официальное) название объекта']) else '-',
                'sn': str(row['Короткое (спортивное) название объекта']) if pd.notna(row['Короткое (спортивное) название объекта']) else '-',
                'ad': str(row['Адрес']) if pd.notna(row['Адрес']) else '-',
                'ct': str(row['Контактное лицо']) if pd.notna(row['Контактное лицо']) else '-',
                'ow': str(row['Собственник (ОГРН)']) if pd.notna(row['Собственник (ОГРН)']) else '-',
                'mg': str(row['Управляющая компания (ОГРН)']) if pd.notna(row['Управляющая компания (ОГРН)']) else '-',
                'us': str(row['Пользователь (ОГРН)']) if pd.notna(row['Пользователь (ОГРН)']) else '-',
                'tp': str(row['Тип Объекта ']) if pd.notna(row['Тип Объекта ']) else '-',
                'd2': str(row['Дисциплина_2']) if pd.notna(row['Дисциплина_2']) else '-',
                'ln': length_val,
                'wd': width_val,
                'cv': str(row['Тип покрытия']) if pd.notna(row['Тип покрытия']) else '-',
                'cp': str(row['Количество мест для зрителей']) if pd.notna(row['Количество мест для зрителей']) else '-',
                'dr': '+' if pd.notna(row['Наличие дренажа']) and row['Наличие дренажа'] == 'Y' else '-',
                'ht': '+' if pd.notna(row['Наличие подогрева']) and row['Наличие подогрева'] == 'Y' else '-',
                'sc': '+' if pd.notna(row['Наличие табло']) and row['Наличие табло'] == 'Y' else '-',
                'ds': '+' if pd.notna(row['Наличие раздевалок']) and row['Наличие раздевалок'] == 'Y' else '-',
                'yr': str(row['Год ввода в эксплуатацию/год капитального ремонта']) if pd.notna(row['Год ввода в эксплуатацию/год капитального ремонта']) else '-',
                'sz': f"{length_val}×{width_val}" if length_val != '-' and width_val != '-' else '-',
                'id': id_egora_value,
                'cl': color_class,
                'cd': color_description,
                'sw': status_of_work,
                'pd': provided_data
            }
            
            objects_data.append(full_info)
        
        # HTML для компактных плашек с правильным расположением элементов
        objects_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: transparent;
                    width: 100%;
                    overflow-x: hidden;
                }}
                
                .objects-container {{
                    width: 100%;
                    margin: 0 auto;
                    padding: 3px;
                    max-height: 850px;
                    overflow-y: auto;
                    scroll-behavior: smooth;
                }}
                
                .card {{
                    background-color: white;
                    border-radius: 6px;
                    padding: 8px;
                    margin-bottom: 6px;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
                    border-left: 2px solid #3b82f6;
                }}
                
                /* Стиль для карточек со статусом 2 */
                .card-status-2 {{
                    border-left: 2px solid #9444EF;
                }}
                
                /* Строка 1: Полное название + Кнопка (кнопка сразу после названия) */
                .row-1 {{
                    display: flex;
                    align-items: flex-start;
                    margin-bottom: 6px;
                    gap: 5px;
                }}
                
                .full-name {{
                    color: #2a4a80;
                    font-weight: bold;
                    font-size: 13px;
                    line-height: 1.3;
                    margin-top: 0;
                    margin-bottom: 0;
                }}
                
                /* Кнопка "Внести изменения" - сразу после названия */
                .form-btn-compact {{
                    cursor: pointer;
                    background: #10b981;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    color: white;
                    font-weight: bold;
                    font-size: 10px;
                    white-space: nowrap;
                    height: 24px;
                }}
                
                .form-btn-compact:hover {{
                    background: #059669;
                }}
                
                .form-btn-opened {{
                    background: #6b7280;
                    cursor: default !important;
                }}
                
                .form-btn-disabled {{
                    background: #9ca3af;
                    opacity: 0.7;
                    cursor: not-allowed !important;
                }}
                
                /* Строка 2: ID + Краткое + Адрес + Размер + Статус (все подряд) */
                .row-2 {{
                    display: flex;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-bottom: 6px;
                    font-size: 11px;
                    color: #333;
                }}
                
                /* ID с кнопкой копирования */
                .id-container {{
                    display: flex;
                    align-items: center;
                    gap: 3px;
                    background: #f3f4f6;
                    padding: 2px 6px;
                    border-radius: 3px;
                    white-space: nowrap;
                }}
                
                .copy-icon-small {{
                    cursor: pointer;
                    color: #3b82f6;
                    font-size: 10px;
                    transition: color 0.2s;
                    margin-left: 2px;
                }}
                
                .copy-icon-small:hover {{
                    color: #2563eb;
                }}
                
                /* Элементы второй строки - все подряд */
                .info-item {{
                    display: flex;
                    align-items: center;
                    gap: 2px;
                    white-space: nowrap;
                }}
                
                /* Цветовая метка статуса - просто элемент в строке */
                .color-label-compact {{
                    display: inline-flex;
                    align-items: center;
                    gap: 3px;
                    padding: 1px 5px;
                    border-radius: 3px;
                    font-size: 9px;
                    font-weight: bold;
                    background: #f3f4f6;
                    white-space: nowrap;
                }}
                
                .color-indicator-small {{
                    display: inline-block;
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                }}
                
                .color-blue {{ background-color: #3B82F6; }}
                .color-yellow {{ background-color: #FFA500; }}
                .color-green {{ background-color: #10B981; }}
                .color-purple {{ background-color: #9444EF; }}
                .color-red {{ background-color: #EF4444; }}
                
                /* Строка 3: Кнопка показа деталей */
                .toggle-details-btn {{
                    background: none;
                    border: none;
                    color: #3b82f6;
                    cursor: pointer;
                    font-size: 10px;
                    padding: 2px 0;
                    text-align: left;
                    margin: 0;
                }}
                
                .toggle-details-btn:hover {{
                    text-decoration: underline;
                }}
                
                /* Уведомление о копировании */
                .notification {{
                    position: fixed;
                    top: 15px;
                    right: 15px;
                    background-color: #10b981;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 4px;
                    z-index: 10000;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    opacity: 0;
                    transition: opacity 0.3s;
                    font-size: 11px;
                }}
                
                .notification.show {{
                    opacity: 1;
                }}
                
                hr {{
                    border: none;
                    height: 0.5px;
                    background-color: #e5e7eb;
                    margin: 6px 0;
                }}
                
                /* Секция деталей */
                .details-section {{
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    padding: 6px;
                    margin: 5px 0;
                }}
                
                .details-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 5px;
                }}
                
                .details-item {{
                    display: flex;
                    flex-direction: column;
                }}
                
                .details-label {{
                    font-weight: bold;
                    color: #495057;
                    font-size: 9px;
                    margin-bottom: 1px;
                }}
                
                .details-value {{
                    color: #212529;
                    font-size: 9px;
                    word-break: break-word;
                }}
                
                /* Предоставленные данные */
                .provided-data-section {{
                    background-color: #F0F9FF;
                    border: 1px solid #93C5FD;
                    border-radius: 4px;
                    padding: 6px;
                    margin: 5px 0;
                }}
                
                .provided-data-section-red {{
                    background-color: #FEF2F2;
                    border: 1px solid #FCA5A5;
                    border-radius: 4px;
                    padding: 6px;
                    margin: 5px 0;
                }}
                
                .provided-data-section-purple {{
                    background-color: #F3E8FF;
                    border: 1px solid #9444EF;
                    border-radius: 4px;
                    padding: 6px;
                    margin: 5px 0;
                }}
                
                .provided-data-title {{
                    color: #1D4ED8;
                    font-weight: bold;
                    font-size: 9px;
                    margin-bottom: 4px;
                }}
                
                .provided-data-title-red {{
                    color: #DC2626;
                    font-weight: bold;
                    font-size: 9px;
                    margin-bottom: 4px;
                }}
                
                .provided-data-title-purple {{
                    color: #9444EF;
                    font-weight: bold;
                    font-size: 9px;
                    margin-bottom: 4px;
                }}
                
                .provided-data-content {{
                    color: #000000;
                    font-size: 9px;
                    white-space: pre-line;
                    line-height: 1.2;
                }}
                
                .provided-data-content strong {{
                    font-weight: bold;
                    color: #000000;
                }}
                
                /* Пагинация информация */
                .pagination-info {{
                    background-color: #f0f9ff;
                    border: 1px solid #bae6fd;
                    border-radius: 4px;
                    padding: 8px;
                    margin: 10px 0;
                    font-size: 10px;
                    color: #0369a1;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="pagination-info">
                Показано объектов: {len(objects_data)} из {len(filtered_data_for_display)}
                {f' (Страница {page_number + 1} из {total_pages})' if total_pages > 1 else ''}
            </div>
            
            <div class="objects-container" id="objects-container">
                <!-- Объекты будут добавлены через JavaScript -->
            </div>
            
            <div id="notification" class="notification" style="display: none;">
                <span class="notification-icon">✓</span>
                <span id="notification-text"></span>
            </div>
            
            <script>
                const objectsData = {json.dumps(objects_data, ensure_ascii=False)};
                
                let buttonStates = {{}};
                let detailsStates = {{}};
                let scrollPosition = 0;
                
                // Сохраняем позицию скролла
                function saveScrollPosition() {{
                    const container = document.getElementById('objects-container');
                    if (container) {{
                        scrollPosition = container.scrollTop;
                    }}
                }}
                
                // Восстанавливаем позицию скролла
                function restoreScrollPosition() {{
                    const container = document.getElementById('objects-container');
                    if (container && scrollPosition > 0) {{
                        setTimeout(() => {{
                            container.scrollTop = scrollPosition;
                        }}, 50);
                    }}
                }}
                
                function showNotification(message, duration = 1500) {{
                    const notification = document.getElementById('notification');
                    const notificationText = document.getElementById('notification-text');
                    
                    notificationText.textContent = message;
                    notification.style.display = 'flex';
                    
                    setTimeout(() => {{
                        notification.classList.add('show');
                    }}, 10);
                    
                    setTimeout(() => {{
                        notification.classList.remove('show');
                        setTimeout(() => {{
                            notification.style.display = 'none';
                        }}, 300);
                    }}, duration);
                }}
                
                // Функция для копирования ID
                function copyId(id, index) {{
                    saveScrollPosition(); // Сохраняем позицию перед копированием
                    
                    if (navigator.clipboard && navigator.clipboard.writeText) {{
                        navigator.clipboard.writeText(id)
                            .then(() => {{
                                showNotification('ID скопирован: ' + id);
                            }})
                            .catch(err => {{
                                console.error('Clipboard API error:', err);
                                fallbackCopy(id);
                            }});
                    }} else {{
                        fallbackCopy(id);
                    }}
                    
                    function fallbackCopy(textToCopy) {{
                        const textArea = document.createElement('textarea');
                        textArea.value = textToCopy;
                        textArea.style.position = 'fixed';
                        textArea.style.left = '-999999px';
                        document.body.appendChild(textArea);
                        textArea.select();
                        
                        try {{
                            const successful = document.execCommand('copy');
                            if (successful) {{
                                showNotification('✓ ID скопирован: ' + textToCopy);
                            }} else {{
                                showNotification('❌ Не удалось скопировать');
                            }}
                        }} catch (err) {{
                            console.error('execCommand error:', err);
                            showNotification('❌ Ошибка при копировании');
                        }} finally {{
                            document.body.removeChild(textArea);
                        }}
                    }}
                }}
                
                function openForm(index, statusOfWork) {{
                    saveScrollPosition(); // Сохраняем позицию перед открытием формы
                    
                    if (statusOfWork === '1' || statusOfWork === '2') {{
                        return false;
                    }}
                    
                    const url = "https://school-eev.bitrix24site.ru/crm_form_drmcv/";
                    
                    buttonStates[index] = true;
                    
                    const button = document.getElementById('form-btn-' + index);
                    if (button) {{
                        button.textContent = '📋 Форма была открыта';
                        button.className = 'form-btn-compact form-btn-opened';
                        
                        button.onclick = function() {{
                            window.open(url, '_blank');
                        }};
                    }}
                    
                    window.open(url, '_blank');
                    return true;
                }}
                
                function createObjectCard(obj, index) {{
                    const statusOfWork = obj.sw || '0';
                    
                    // Для статуса 2 создаем упрощенную карточку
                    if (statusOfWork === '2') {{
                        const card = document.createElement('div');
                        card.className = 'card card-status-2';
                        
                        let providedDataHTML = '';
                        if (obj.pd) {{
                            providedDataHTML = `
                                <div class="provided-data-section-purple" style="margin-top: 8px;">
                                    <div class="provided-data-title-purple">🟣 Добавили новое поле, в стадии рассмотрения</div>
                                    <div class="provided-data-content">${{obj.pd}}</div>
                                </div>
                            `;
                        }}
                        
                        // Для статуса 2: только адрес и цветовая метка
                        card.innerHTML = `
                            <!-- Строка 1: Только цветовая метка статуса -->
                            <div class="row-2">
                                <div class="color-label-compact">
                                    <span>${{obj.cd}}</span>
                                </div>
                            </div>
                            
                            <!-- Строка 2: Адрес -->
                            <div class="row-2" style="margin-top: 4px;">
                                <div class="info-item">
                                    <span>📍</span>
                                    <span>${{obj.ad}}</span>
                                </div>
                            </div>
                            
                            <!-- Строка 3: Кнопка показа деталей (только предоставленные данные) -->
                            <button onclick="toggleStatus2Details(${{index}})" class="toggle-details-btn">
                                ${{detailsStates[index] ? '▲ Скрыть предоставленные данные' : '▼ Показать предоставленные данные'}}
                            </button>
                            
                            <!-- Детали (только предоставленные данные) -->
                            <div id="details-${{index}}" style="display: ${{detailsStates[index] ? 'block' : 'none'}};">
                                ${{providedDataHTML}}
                            </div>
                        `;
                        
                        return card;
                    }}
                    
                    // Для остальных статусов - обычная карточка
                    const card = document.createElement('div');
                    card.className = 'card';
                    
                    if (buttonStates[index] === undefined) {{
                        buttonStates[index] = false;
                    }}
                    
                    // Восстанавливаем состояние из sessionStorage или инициализируем как false
                    if (detailsStates[index] === undefined) {{
                        const savedState = sessionStorage.getItem(`card_${{index}}_expanded`);
                        detailsStates[index] = savedState === 'true';
                    }}
                    
                    let providedDataHTML = '';
                    if (obj.pd) {{
                        if (statusOfWork === '1') {{
                            providedDataHTML = `
                                <div class="provided-data-section-red">
                                    <div class="provided-data-title-red">🔴 Внесли изменения, в стадии рассмотрения</div>
                                    <div class="provided-data-content">${{obj.pd}}</div>
                                </div>
                            `;
                        }}
                    }}
                    
                    let formButtonHTML = '';
                    // Для статуса 1 и 2 не показываем кнопку
                    if (statusOfWork !== '1' && statusOfWork !== '2') {{
                        let formBtnClass = 'form-btn-compact';
                        let formBtnText = '✅ Внести изменения';
                        let formBtnOnclick = `openForm(${{index}}, '${{statusOfWork}}')`;
                        
                        if (buttonStates[index]) {{
                            formBtnClass = 'form-btn-compact form-btn-opened';
                            formBtnText = '📋 Форма была открыта';
                            formBtnOnclick = `window.open('https://school-eev.bitrix24site.ru/crm_form_drmcv/', '_blank')`;
                        }}
                        
                        formButtonHTML = `
                            <button id="form-btn-${{index}}" 
                                    onclick="${{formBtnOnclick}}" 
                                    class="${{formBtnClass}}" 
                                    title="Открыть форму для внесения изменений">
                                ${{formBtnText}}
                            </button>
                        `;
                    }}
                    
                    const detailsHTML = `
                        <div class="details-section">
                            <div class="details-grid">
                                <div class="details-item">
                                    <span class="details-label">📞 Контакт:</span>
                                    <span class="details-value">${{obj.ct}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">👤 Собственник:</span>
                                    <span class="details-value">${{obj.ow}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">🏢 Управляющая:</span>
                                    <span class="details-value">${{obj.mg}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">👥 Пользователь:</span>
                                    <span class="details-value">${{obj.us}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Тип:</span>
                                    <span class="details-value">${{obj.tp}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Дисциплина:</span>
                                    <span class="details-value">${{obj.d2}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Покрытие:</span>
                                    <span class="details-value">${{obj.cv}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Мест:</span>
                                    <span class="details-value">${{obj.cp}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Дренаж:</span>
                                    <span class="details-value">${{obj.dr}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Подогрев:</span>
                                    <span class="details-value">${{obj.ht}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Табло:</span>
                                    <span class="details-value">${{obj.sc}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Раздевалки:</span>
                                    <span class="details-value">${{obj.ds}}</span>
                                </div>
                                <div class="details-item">
                                    <span class="details-label">Год:</span>
                                    <span class="details-value">${{obj.yr}}</span>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    // КОМПАКТНЫЙ ФОРМАТ: 3 строки, все элементы подряд
                    card.innerHTML = `
                        <!-- Строка 1: Полное название + Кнопка (сразу после названия) -->
                        <div class="row-1">
                            <div class="full-name">${{obj.fn}}</div>
                            ${{formButtonHTML}}
                        </div>
                        
                        <!-- Строка 2: ID + Краткое + Адрес + Размер + Статус (все подряд) -->
                        <div class="row-2">
                            <div class="id-container">
                                <span>ID: ${{obj.id}}</span>
                                <span onclick="copyId('${{obj.id}}', ${{index}})" class="copy-icon-small" title="Скопировать ID">📄</span>
                            </div>
                            <div class="info-item">
                                <span>⚽</span>
                                <span>${{obj.sn}}</span>
                            </div>
                            <div class="info-item">
                                <span>📍</span>
                                <span>${{obj.ad}}</span>
                            </div>
                            <div class="info-item">
                                <span>📏</span>
                                <span>${{obj.sz}}</span>
                            </div>
                            <div class="color-label-compact">
                                <span>${{obj.cd}}</span>
                            </div>
                        </div>
                        
                        <!-- Строка 3: Кнопка показа деталей -->
                        <button onclick="toggleDetails(${{index}})" class="toggle-details-btn">
                            ${{detailsStates[index] ? '▲ Скрыть детали' : '▼ Показать все детали'}}
                        </button>
                        
                        <!-- Детали и предоставленные данные -->
                        <div id="details-${{index}}" style="display: ${{detailsStates[index] ? 'block' : 'none'}};">
                            ${{detailsHTML}}
                            ${{providedDataHTML}}
                        </div>
                    `;
                    
                    return card;
                }}
                
                function toggleDetails(index) {{
                    // Сохраняем текущую позицию скролла
                    saveScrollPosition();
                    
                    // Меняем состояние
                    detailsStates[index] = !detailsStates[index];
                    
                    // Сохраняем в sessionStorage
                    sessionStorage.setItem(`card_${{index}}_expanded`, detailsStates[index]);
                    
                    // Обновляем только конкретную карточку (чтобы не терять скролл)
                    const toggleButton = document.querySelector(`[onclick="toggleDetails(${{index}})"]`);
                    const detailsElement = document.getElementById('details-' + index);
                    
                    if (toggleButton && detailsElement) {{
                        // Обновляем текст кнопки
                        toggleButton.textContent = detailsStates[index] ? '▲ Скрыть детали' : '▼ Показать все детали';
                        
                        // Показываем/скрываем детали
                        detailsElement.style.display = detailsStates[index] ? 'block' : 'none';
                        
                        // Плавно прокручиваем к карточке, если она раскрывается
                        if (detailsStates[index]) {{
                            setTimeout(() => {{
                                toggleButton.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                            }}, 10);
                        }}
                        
                        // Восстанавливаем позицию скролла
                        setTimeout(() => {{
                            restoreScrollPosition();
                        }}, 20);
                    }}
                }}
                
                function toggleStatus2Details(index) {{
                    // Сохраняем текущую позицию скролла
                    saveScrollPosition();
                    
                    // Меняем состояние
                    detailsStates[index] = !detailsStates[index];
                    
                    // Сохраняем в sessionStorage
                    sessionStorage.setItem(`card_${{index}}_expanded`, detailsStates[index]);
                    
                    // Обновляем только конкретную карточку (чтобы не терять скролл)
                    const toggleButton = document.querySelector(`[onclick="toggleStatus2Details(${{index}})"]`);
                    const detailsElement = document.getElementById('details-' + index);
                    
                    if (toggleButton && detailsElement) {{
                        // Обновляем текст кнопки
                        toggleButton.textContent = detailsStates[index] ? '▲ Скрыть предоставленные данные' : '▼ Показать предоставленные данные';
                        
                        // Показываем/скрываем детали
                        detailsElement.style.display = detailsStates[index] ? 'block' : 'none';
                        
                        // Плавно прокручиваем к карточке, если она раскрывается
                        if (detailsStates[index]) {{
                            setTimeout(() => {{
                                toggleButton.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                            }}, 10);
                        }}
                        
                        // Восстанавливаем позицию скролла
                        setTimeout(() => {{
                            restoreScrollPosition();
                        }}, 20);
                    }}
                }}
                
                function renderObjects() {{
                    const container = document.getElementById('objects-container');
                    container.innerHTML = '';
                    
                    if (objectsData.length === 0) {{
                        container.innerHTML = '<div class="card"><p style="text-align: center; color: #666;">Объекты не найдены</p></div>';
                        return;
                    }}
                    
                    // Рендерим все карточки
                    for (let i = 0; i < objectsData.length; i++) {{
                        const obj = objectsData[i];
                        const card = createObjectCard(obj, i);
                        container.appendChild(card);
                        
                        if (i < objectsData.length - 1) {{
                            const hr = document.createElement('hr');
                            container.appendChild(hr);
                        }}
                    }}
                    
                    // Восстанавливаем позицию скролла
                    restoreScrollPosition();
                }}
                
                document.addEventListener('DOMContentLoaded', function() {{
                    // Сохраняем скролл при прокрутке
                    const container = document.getElementById('objects-container');
                    if (container) {{
                        container.addEventListener('scroll', saveScrollPosition);
                    }}
                    
                    // Загружаем сохраненные состояния кнопок
                    try {{
                        const savedButtonStates = sessionStorage.getItem('buttonStates');
                        if (savedButtonStates) {{
                            buttonStates = JSON.parse(savedButtonStates);
                        }}
                    }} catch (e) {{
                        console.error('Error loading button states:', e);
                    }}
                    
                    renderObjects();
                    
                    // Сохраняем состояния при закрытии
                    window.addEventListener('beforeunload', function() {{
                        try {{
                            sessionStorage.setItem('buttonStates', JSON.stringify(buttonStates));
                        }} catch (e) {{
                            console.error('Error saving button states:', e);
                        }}
                    }});
                }});
                
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', renderObjects);
                }} else {{
                    setTimeout(renderObjects, 100);
                }}
            </script>
        </body>
        </html>
        """
        
        # Увеличиваем высоту для показа большего количества объектов
        st.components.v1.html(objects_html, height=9000, scrolling=True)
    
    else:
        # Карта (режим карты) - используем filtered_data_for_display вместо data
        sirota = filtered_data_for_display['Широта']
        dolgota = filtered_data_for_display['Долгота']
        
        full_name = filtered_data_for_display['Полное (официальное) название объекта'] # 0
        short_name = filtered_data_for_display['Короткое (спортивное) название объекта'] # 1
        adres = filtered_data_for_display['Адрес'] # 2
        contact_name = filtered_data_for_display['Контактное лицо'] # 3
        owner = filtered_data_for_display['Собственник (ОГРН)'] # 4
        manager = filtered_data_for_display['Управляющая компания (ОГРН)'] #5
        user = filtered_data_for_display['Пользователь (ОГРН)'] #6
        rfs_id= filtered_data_for_display['РФС_ID'] #7
        type_objectt = filtered_data_for_display['Тип Объекта '] #8
        disciplyne = filtered_data_for_display['Дисциплина '] #9
        length = filtered_data_for_display['Длина футбольного поля'] # 10
        width = filtered_data_for_display['Ширина футбольного поля'] # 11
        design_feature = filtered_data_for_display['Конструктивная особенность'] # 12
        type_of_coverage = filtered_data_for_display['Тип покрытия'] # 13
        capacity = filtered_data_for_display['Количество мест для зрителей'] # 14
        capacity = capacity.astype(str)
        drainage = filtered_data_for_display['Наличие дренажа'] # 15
        heating = filtered_data_for_display['Наличие подогрева'] # 16
        scoreboard = filtered_data_for_display['Наличие табло'] # 17
        dress_room = filtered_data_for_display['Наличие раздевалок'] # 18
        year = filtered_data_for_display['Год ввода в эксплуатацию/год капитального ремонта'] # 19
        year = year.astype(str)
        in_reestr = filtered_data_for_display['Наличие в реестрах'].to_list()
        disp_2 = filtered_data_for_display['Дисциплина_2']
        id_egora = filtered_data_for_display['id_egora']
        status_of_work = filtered_data_for_display['Статус работы']
        info = filtered_data_for_display['То, что заполнили РОИВ']

        YANDEX_API_KEY = "7fe74d5b-be45-47d1-9fc0-a0765598a4d7"

        # Подготовка данных для карты
        points_data = []
        for i in range(len(sirota)):
            # Обработка информации для объектов со статусом работы '1' или '2'
            result_string = ""
            if status_of_work.iloc[i] in ('1', '2'):
                to_slovar = filtered_data_for_display['То, что заполнили РОИВ'].iloc[i].replace('<br>', '|').split('|')
                
                if status_of_work.iloc[i] == '1' and len(to_slovar) >= 11:
                    slovar = {
                        'Полное(официальное) название объекта': to_slovar[0],
                        'Короткое (спортивное) название объекта': to_slovar[1],
                        'Адрес': to_slovar[2],
                        'Широта и долгота': to_slovar[3],
                        'Длина': to_slovar[4],
                        'Ширина': to_slovar[5],
                        'Тип покрытия': to_slovar[6],
                        'Отправитель': to_slovar[7],
                        'Подтвердить': to_slovar[8] if to_slovar[8] == 'Y' else '',
                        'Удалить': to_slovar[9] if to_slovar[9] == 'Y' else '',
                        'Зал/не зал': to_slovar[10] if to_slovar[10] == 'Y' else '',
                        'Комментарий': to_slovar[11],
                        'Номер региона': to_slovar[12]
                    }
                elif status_of_work.iloc[i] == '2' and len(to_slovar) >= 9:
                    slovar = {
                        'Полное(официальное) название объекта': to_slovar[0],
                        'Короткое (спортивное) название объекта': to_slovar[1],
                        'Адрес': to_slovar[2],
                        'Широта и долгота': to_slovar[3],
                        'Длина': to_slovar[4],
                        'Ширина': to_slovar[5],
                        'Тип покрытия': to_slovar[6],
                        'Отправитель': to_slovar[7],
                        'Зал/не зал': to_slovar[8] if to_slovar[8] == 'Y' else '',
                        'Комментарий':  to_slovar[9],
                        'Номер региона': to_slovar[-1]
                    }
                if slovar:
                    result_parts = []
                    for key, value in slovar.items():
                        if value != '' and value is not None:
                            result_parts.append(f'{key}: <strong>{value}</strong>')

                    if result_parts:
                        result_string = '<br>'.join(result_parts)
            
            # Определяем цвет точки
            icon_color, _ = get_point_color(str(status_of_work.iloc[i]), in_reestr[i])
            
            current_id_egora = str(int(float(id_egora.iloc[i]))) if pd.notna(id_egora.iloc[i]) and str(id_egora.iloc[i]).replace('.0', '') != 'nan' else ""
            
            # Преобразуем размеры в целые числа
            length_val = str(length.iloc[i]) if pd.notna(length.iloc[i]) else '-'
            width_val = str(width.iloc[i]) if pd.notna(width.iloc[i]) else '-'
            
            try:
                if length_val != '-' and float(length_val).is_integer():
                    length_val = str(int(float(length_val)))
                if width_val != '-' and float(width_val).is_integer():
                    width_val = str(int(float(width_val)))
            except:
                pass
            
            points_data.append({
                'lat': float(sirota.iloc[i]) if pd.notna(sirota.iloc[i]) else 0,
                'lon': float(dolgota.iloc[i]) if pd.notna(dolgota.iloc[i]) else 0,
                'color': icon_color,
                'index': i,
                'id_egora': current_id_egora,
                'status_of_work': str(status_of_work.iloc[i]) if pd.notna(status_of_work.iloc[i]) else "0",
                'address': str(adres.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(adres.iloc[i]) else '-',
                'full_name': str(full_name.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(full_name.iloc[i]) else '-',
                'short_name': str(short_name.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(short_name.iloc[i]) else '-',
                'contact': str(contact_name.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(contact_name.iloc[i]) else '-',
                'owner': str(owner.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(owner.iloc[i]) else '-',
                'manager': str(manager.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(manager.iloc[i]) else '-',
                'user': str(user.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(user.iloc[i]) else '-',
                'type': str(type_objectt.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(type_objectt.iloc[i]) else '-',
                'discipline': str(disp_2.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(disp_2.iloc[i]) else '-',
                'size': f"{length_val}×{width_val}",
                'coverage': str(type_of_coverage.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(type_of_coverage.iloc[i]) else '-',
                'capacity': str(capacity.iloc[i]).replace('nan','-') if pd.notna(capacity.iloc[i]) else '-',
                'drainage': '+' if pd.notna(drainage.iloc[i]) and drainage.iloc[i] == 'Y' else '-',
                'heating': '+' if pd.notna(heating.iloc[i]) and heating.iloc[i] == 'Y' else '-',
                'scoreboard': '+' if pd.notna(scoreboard.iloc[i]) and scoreboard.iloc[i] == 'Y' else '-',
                'dressing': '+' if pd.notna(dress_room.iloc[i]) and dress_room.iloc[i] == 'Y' else '-',
                'year': str(year.iloc[i]).replace('nan','-') if pd.notna(year.iloc[i]) else '-',
                'provided_data': result_string
            })

        # Центр карты - средние координаты
        if len(sirota) > 0 and not sirota.isna().all():
            if st_select_region == '87 Чукотский автономный округ':
                center_lat, center_lon = 67.131709, 172.286661
            else:
                center_lat = sirota.mean()
                center_lon = dolgota.mean()
        else:
            center_lat, center_lon = 44.6, 40.1  

        # HTML карты
        zoom = 5
        
        
        map_unique_id = st.session_state.map_refresh_key
        map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://api-maps.yandex.ru/2.1/?apikey={YANDEX_API_KEY}&lang=ru_RU"></script>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }}
        #map-{map_unique_id} {{
            width: 100%;
            height: 100vh;
        }}
        .address-info {{
            position: absolute;
            background: white;
            padding: 12px;
            border-radius: 6px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.2);
            max-width: 320px;
            z-index: 1000;
            border: 2px solid #3b82f6;
            font-family: Arial, sans-serif;
            left: 15px;
            bottom: 15px;
        }}
        .close-btn {{
            position: absolute;
            top: -8px;
            right: -8px;
            background: #3b82f6;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            text-align: center;
            line-height: 20px;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        .close-btn:hover {{
            background: #2563eb;
        }}
        .address-title {{
            color: #3b82f6;
            margin-bottom: 6px;
            font-size: 14px;
        }}
        .coords {{
            color: #666;
            font-size: 12px;
            margin-top: 6px;
            font-family: monospace;
        }}
        .field-btn {{
            margin-top: 8px;
            text-align: center;
        }}
        .field-btn button {{
            cursor: pointer;
            background: #3b82f6;
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            color: white;
            font-weight: bold;
            font-size: 11px;
            width: 100%;
        }}
        .field-btn button:hover {{
            background: #2563eb;
        }}
        .copy-btn {{
            margin-top: 8px;
            text-align: center;
        }}
        .copy-btn button {{
            cursor: pointer;
            background: #8b5cf6;
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            color: white;
            font-weight: bold;
            font-size: 11px;
            width: 100%;
        }}
        .copy-btn button:hover {{
            background: #7c3aed;
        }}
        .copy-success {{
            position: fixed;
            top: 15px;
            right: 15px;
            background: #10b981;
            color: white;
            padding: 8px 15px;
            border-radius: 4px;
            z-index: 9999;
            box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
            display: none;
        }}
        .address-item {{
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .address-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .item-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3px;
        }}
        .item-label {{
            font-weight: bold;
            color: #3b82f6;
            font-size: 12px;
        }}
        .item-content {{
            color: #333;
            font-size: 12px;
            word-break: break-word;
        }}
        .copy-icon-btn {{
            cursor: pointer;
            background: none;
            border: none;
            padding: 2px;
            font-size: 16px;
            color: #666;
            transition: color 0.2s;
        }}
        .copy-icon-btn:hover {{
            color: #8b5cf6;
        }}
        .status-warning {{
            background-color: #F3E8FF;
            border: 2px solid #9444EF;
            border-radius: 6px;
            padding: 12px;
            margin: 8px 0;
        }}
        .status-warning-title {{
            color: #9444EF;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 8px;
            text-align: center;
        }}
        .status-warning-text {{
            color: #6B21A8;
            font-size: 12px;
        }}
        .provided-data-content strong {{
            font-weight: bold;
            color: #000000;
        }}
        .provided-data-section {{
            background-color: #F0F9FF;
            border: 1px solid #93C5FD;
            border-radius: 5px;
            padding: 10px;
            margin: 8px 0;
        }}
        .provided-data-title {{
            color: #1D4ED8;
            font-weight: bold;
            font-size: 12px;
            margin-bottom: 6px;
        }}
        .provided-data-content {{
            color: #000000;
            font-size: 11px;
            white-space: pre-line;
            line-height: 1.3;
        }}
        .form-button-disabled {{
            cursor: not-allowed !important;
            background-color: #9ca3af !important;
            opacity: 0.7;
        }}
        .form-button-disabled:hover {{
            background-color: #9ca3af !important;
        }}
    </style>
</head>
<body>
    <div id="map-{map_unique_id}"></div>
    <div id="copy-success" class="copy-success">✓ Скопировано в буфер обмена!</div>

    <script>
        // Передаём данные точек
        const POINTS_DATA = {json.dumps(points_data, ensure_ascii=False)};
        
        // Глобальные переменные
        let map;
        let lastClickCoords = null;
        let lastClickAddress = null;
        let placemarks = [];
        let blackPlacemarks = [];
        
        function handleConfirmClick(index) {{
            const pointData = POINTS_DATA[index];
            const statusOfWork = pointData.status_of_work || '0';
            
            if (statusOfWork === '1' || statusOfWork === '2') {{
                alert('Внесли изменения, в стадии рассмотрения. Внести изменения нельзя.');
                return false;
            }}
            
            window.open("https://school-eev.bitrix24site.ru/crm_form_drmcv/", "_blank");
            
            if (placemarks[index]) {{
                const placemark = placemarks[index];
                placemark.options.set('iconColor', '#808080');
                const updatedBalloon = getBalloonContent(pointData, true);
                placemark.properties.set('balloonContent', updatedBalloon);
            }}
            
            return true;
        }}
        
        function getBalloonContent(pointData, isChanged = false) {{
            const statusOfWork = pointData.status_of_work || '0';
            const providedData = pointData.provided_data || '';
            
            if (statusOfWork === '2') {{
                let providedDataHTML = '';
                if (providedData) {{
                    providedDataHTML = `
                        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                            <div style="color: #9444EF; font-weight: bold; font-size: 11px; margin-bottom: 4px;">
                                📋 Предоставленные данные:
                            </div>
                            <div style="color: #000000; font-size: 10px;">${{providedData}}</div>
                        </div>
                    `;
                }}
                
                return `
                    <div style="font-size: 9px; max-width: 450px; padding: 6px; line-height: 1.3;">
                        <div style="margin-bottom: 5px; padding-top: 5px;">
                            <strong>📍 Адрес:</strong><br>
                            <span>${{pointData.address}}</span>
                        </div>
                        
                        <div class="status-warning">
                            <div class="status-warning-title">🟣 Добавили новое поле, в стадии рассмотрения</div>
                            ${{providedDataHTML}}
                        </div>
                    </div>
                `;
            }}
            
            let statusHTML = '';
            if (isChanged || statusOfWork === '1') {{
                let providedDataHTML = '';
                if (providedData && !isChanged) {{
                    if (statusOfWork === '1') {{
                        providedDataHTML = `
                            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                                <div style="color: #DC2626; font-weight: bold; font-size: 11px; margin-bottom: 4px;">
                                    📋 Предоставленные данные:
                                </div>
                                <div style="color: #000000; font-size: 10px;">${{providedData}}</div>
                            </div>
                        `;
                    }}
                }}
                
                statusHTML = `
                    <div style="background-color: ${{isChanged ? '#F3F4F6' : '#FEF2F2'}}; 
                         border: 1px solid ${{isChanged ? '#D1D5DB' : '#FCA5A5'}}; 
                         padding: 8px; border-radius: 3px; margin-bottom: 8px;">
                        <div style="color: ${{isChanged ? '#6B7280' : '#DC2626'}}; font-weight: bold; display: flex; align-items: center; gap: 4px;">
                            <span>${{isChanged ? '⚪' : '🔴'}}</span>
                            <span>${{isChanged ? 'Нажали "Внести изменения", но не отправили анкету' : 'Внесли изменения, в стадии рассмотрения'}}</span>
                        </div>
                        ${{providedDataHTML}}
                    </div>
                `;
            }}
            
            const showConfirmButton = (statusOfWork !== '1' && statusOfWork !== '2');
            const confirmButtonSection = showConfirmButton ? `
                <div style="margin-top: 10px; padding-top: 10px; border-top: 2px solid #e5e7eb;">
                    <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
                        <button onclick="handleConfirmClick(${{pointData.index}})" 
                                style="cursor: pointer; background: ${{statusOfWork === '1' || statusOfWork === '2' ? '#9ca3af' : '#10b981'}}; 
                                       border: none; padding: 6px 12px; border-radius: 3px; 
                                       color: white; font-weight: bold; font-size: 11px;
                                       ${{statusOfWork === '1' || statusOfWork === '2' ? 'cursor: not-allowed;' : ''}}"
                                ${{statusOfWork === '1' || statusOfWork === '2' ? 'disabled' : ''}}
                                title="${{statusOfWork === '1' || statusOfWork === '2' ? 'Объект на рассмотрении, изменения внести нельзя' : 'Внести изменения'}}">
                            ${{statusOfWork === '1' || statusOfWork === '2' ? '⏳ На рассмотрении' : '✅ Внести изменения'}}
                        </button>
                    </div>
                </div>
            ` : '';
            
            return `
                <div style="font-size: 9px; max-width: 450px; padding: 6px; line-height: 1.3;">
                    ${{statusHTML}}
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                        <div><strong>📋 Полное название:</strong><br><span>${{pointData.full_name}}</span></div>
                        <div><strong>⚽ Короткое название:</strong><br><span>${{pointData.short_name}}</span></div>
                    </div>
                    <div style="margin-bottom: 5px; padding-top: 5px; border-top: 1px solid #e5e7eb;">
                        <strong>📍 Адрес:</strong><br>
                        <span>${{pointData.address}}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                        <div><strong>📞 Контакт:</strong><br><span>${{pointData.contact}}</span></div>
                        <div><strong>👤 Собственник:</strong><br><span>${{pointData.owner}}</span></div>
                        <div><strong>🏢 Управляющая:</strong><br><span>${{pointData.manager}}</span></div>
                        <div><strong>👥 Пользователь:</strong><br><span>${{pointData.user}}</span></div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div><strong>🌐 РФС ID:</strong><br><span>${{pointData.id_egora}}</span></div>
                            <button onclick="copyRfsId('${{pointData.id_egora}}')" class="copy-icon-btn" title="Скопировать РФС ID">
                                📄
                            </button>
                        </div>
                        <div><strong>Тип:</strong><br><span>${{pointData.type}}</span></div>
                        <div><strong>Дисциплина:</strong><br><span>${{pointData.discipline}}</span></div>
                        <div><strong>Размер:</strong><br><span>${{pointData.size}} м</span></div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                        <div><strong>Покрытие:</strong><br><span>${{pointData.coverage}}</span></div>
                        <div><strong>Мест:</strong><br><span>${{pointData.capacity}}</span></div>
                        <div><strong>Дренаж:</strong><br><span>${{pointData.drainage}}</span></div>
                        <div><strong>Подогрев:</strong><br><span>${{pointData.heating}}</span></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                        <div><strong>Табло:</strong><br><span>${{pointData.scoreboard}}</span></div>
                        <div><strong>Раздевалки:</strong><br><span>${{pointData.dressing}}</span></div>
                        <div><strong>Год:</strong><br><span>${{pointData.year}}</span></div>
                    </div>
                    ${{confirmButtonSection}}
                </div>
            `;
        }}
        
        function handleFieldHereClick(coords) {{
            window.open("https://school-eev.bitrix24site.ru/crm_form_saeda/", "_blank");
            
            const blackPlacemark = new ymaps.Placemark(coords, {{
                balloonContent: '',
                hasBalloon: false,
                isBlack: true,
                coords: coords
            }}, {{
                preset: 'islands#circleDotIcon',
                iconColor: "#000000",
                draggable: false
            }});
            
            // Добавляем обработчик клика на черную точку
            blackPlacemark.events.add('click', function(e) {{
                createAddressInfo(coords);
            }});
            
            map.geoObjects.add(blackPlacemark);
            blackPlacemarks.push(blackPlacemark);
        }}
        
        function copyToClipboard(text) {{
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(text).then(function() {{
                    showSuccessNotification();
                }});
            }} else {{
                const textArea = document.createElement("textarea");
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
                showSuccessNotification();
            }}
            
            function showSuccessNotification() {{
                const successDiv = document.getElementById('copy-success');
                successDiv.style.display = 'block';
                setTimeout(function() {{
                    successDiv.style.display = 'none';
                }}, 1500);
            }}
        }}
        
        function copyAddress() {{
            if (lastClickAddress) {{
                copyToClipboard(lastClickAddress);
            }}
        }}
        
        function copyCoords() {{
            if (lastClickCoords) {{
                const coordsText = `${{lastClickCoords[0].toFixed(6)}}, ${{lastClickCoords[1].toFixed(6)}}`;
                copyToClipboard(coordsText);
            }}
        }}
        
        function copyRegionNumber() {{
            copyToClipboard("{int(st_select_region[0:2])}");
        }}
        
        function copyRfsId(rfsId) {{
            if (rfsId) {{
                copyToClipboard(rfsId);
            }}
        }}
        
        function createAddressInfo(coords, address) {{
            const oldInfo = document.querySelector('.address-info');
            if (oldInfo) {{
                oldInfo.remove();
            }}
            
            // Если адрес не предоставлен, геокодируем координаты
            if (!address) {{
                ymaps.geocode(coords).then(function(res) {{
                    const firstGeoObject = res.geoObjects.get(0);
                    let fetchedAddress = 'Адрес не определен';
                    
                    if (firstGeoObject) {{
                        fetchedAddress = firstGeoObject.getAddressLine();
                    }}
                    
                    lastClickAddress = fetchedAddress;
                    lastClickCoords = coords;
                    
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'address-info';
                    infoDiv.innerHTML = `
                        <div class="close-btn" onclick="this.parentElement.remove()">×</div>
                        <div class="address-title">📍 Информация о местоположении</div>
                        
                        <div class="address-item">
                            <div class="item-header">
                                <div class="item-label">Адрес:</div>
                                <button onclick="copyAddress()" class="copy-icon-btn" title="Скопировать адрес">
                                    📄
                                </button>
                            </div>
                            <div class="item-content">${{fetchedAddress}}</div>
                        </div>
                        
                        <div class="address-item">
                            <div class="item-header">
                                <div class="item-label">Координаты:</div>
                                <button onclick="copyCoords()" class="copy-icon-btn" title="Скопировать координаты">
                                    📄
                                </button>
                            </div>
                            <div class="item-content">
                                ${{coords[0].toFixed(6)}}, ${{coords[1].toFixed(6)}}
                            </div>
                        </div>
                        
                        <div class="address-item">
                            <div class="item-header">
                                <div class="item-label">Номер региона:</div>
                                <button onclick="copyRegionNumber()" class="copy-icon-btn" title="Скопировать номер региона">
                                    📄
                                </button>
                            </div>
                            <div class="item-content">
                                {int(st_select_region[0:2])}
                            </div>
                        </div>
                        
                        <div class="field-btn">
                            <button onclick="handleFieldHereClick([${{coords[0]}}, ${{coords[1]}}])">
                                ⚽ Здесь футбольное поле
                            </button>
                        </div>
                    `;
                    
                    document.body.appendChild(infoDiv);
                    
                    setTimeout(() => {{
                        document.addEventListener('click', function closeOnOutsideClick(event) {{
                            if (!infoDiv.contains(event.target)) {{
                                infoDiv.remove();
                                document.removeEventListener('click', closeOnOutsideClick);
                            }}
                        }});
                    }}, 10);
                }});
            }} else {{
                lastClickAddress = address;
                lastClickCoords = coords;
                
                const infoDiv = document.createElement('div');
                infoDiv.className = 'address-info';
                infoDiv.innerHTML = `
                    <div class="close-btn" onclick="this.parentElement.remove()">×</div>
                    <div class="address-title">📍 Информация о местоположении</div>
                    
                    <div class="address-item">
                        <div class="item-header">
                            <div class="item-label">Адрес:</div>
                            <button onclick="copyAddress()" class="copy-icon-btn" title="Скопировать адрес">
                                📄
                            </button>
                        </div>
                        <div class="item-content">${{address}}</div>
                    </div>
                    
                    <div class="address-item">
                        <div class="item-header">
                            <div class="item-label">Координаты:</div>
                            <button onclick="copyCoords()" class="copy-icon-btn" title="Скопировать координаты">
                                📄
                            </button>
                        </div>
                        <div class="item-content">
                            ${{coords[0].toFixed(6)}}, ${{coords[1].toFixed(6)}}
                        </div>
                    </div>
                    
                    <div class="address-item">
                        <div class="item-header">
                            <div class="item-label">Номер региона:</div>
                            <button onclick="copyRegionNumber()" class="copy-icon-btn" title="Скопировать номер региона">
                                📄
                            </button>
                        </div>
                        <div class="item-content">
                            {int(st_select_region[0:2])}
                        </div>
                    </div>
                    
                    <div class="field-btn">
                        <button onclick="handleFieldHereClick([${{coords[0]}}, ${{coords[1]}}])">
                            ⚽ Здесь футбольное поле
                        </button>
                    </div>
                `;
                
                document.body.appendChild(infoDiv);
                
                setTimeout(() => {{
                    document.addEventListener('click', function closeOnOutsideClick(event) {{
                        if (!infoDiv.contains(event.target)) {{
                            infoDiv.remove();
                            document.removeEventListener('click', closeOnOutsideClick);
                        }}
                    }});
                }}, 10);
            }}
        }}
        
        ymaps.ready(init);
        
        function init() {{
            map = new ymaps.Map("map-{map_unique_id}", {{
                center: [{center_lat}, {center_lon}],
                zoom: {zoom},
                type: 'yandex#satellite'
            }});

            const geoObjects = new ymaps.GeoObjectCollection(null, {{
                preset: 'islands#circleDotIcon',
                draggable: false
            }});
            
            POINTS_DATA.forEach(point => {{
                if (point.lat && point.lon && point.lat !== 0 && point.lon !== 0) {{
                    const placemark = new ymaps.Placemark(
                        [point.lat, point.lon],
                        {{
                            balloonContent: '<div style="font-size:11px;padding:4px"><b>Загрузка...</b></div>',
                            balloonMaxWidth: 480,
                            balloonMinWidth: 420,
                            id_egora: point.id_egora,
                            index: point.index,
                            originalIconColor: point.color,
                            needsChanges: false,
                            status_of_work: point.status_of_work
                        }},
                        {{
                            preset: 'islands#circleDotIcon',
                            iconColor: point.color,
                            draggable: false
                        }}
                    );
                    
                    placemark.events.add('click', function(e) {{
                        const target = e.get('target');
                        const index = target.properties.get('index');
                        const pointData = POINTS_DATA[index];
                        
                        const balloonContent = getBalloonContent(pointData);
                        target.properties.set('balloonContent', balloonContent);
                    }});
                    
                    geoObjects.add(placemark);
                    placemarks[point.index] = placemark;
                }}
            }});
            
            map.geoObjects.add(geoObjects);

            map.events.add('click', function(e) {{
                const coords = e.get('coords');
                lastClickCoords = coords;
                
                ymaps.geocode(coords).then(function(res) {{
                    const firstGeoObject = res.geoObjects.get(0);
                    let address = 'Адрес не определен';
                    
                    if (firstGeoObject) {{
                        address = firstGeoObject.getAddressLine();
                    }}
                    
                    lastClickAddress = address;
                    createAddressInfo(coords, address);
                }});
            }});
        }}
        </script>
        </body>
        </html>
        """
        
        # Показываем карту
        st.components.v1.html(map_html, height=600, scrolling=False)
    
    # -------------------------------------------------------------------------------------------------------------
    st.sidebar.markdown("---")
    # Используем оригинальные данные для статистики (до фильтрации)
    st.sidebar.write(f'Всего объектов: {original_data.shape[0]}')
    st.sidebar.markdown("---")
    st.sidebar.write('Типы точек:')
    st.sidebar.write(f'🔵 Есть в РОИВ, но нет в ЦП - {original_data[original_data["Наличие в реестрах"] == 1].shape[0]}')  # Синий
    st.sidebar.write(f'🟡 Есть только в ЦП - {original_data[original_data["Наличие в реестрах"] == 2].shape[0]}')          # Желтый
    st.sidebar.write(f'🟢 Есть в РОИВ и в ЦП - {original_data[original_data["Наличие в реестрах"] == 3].shape[0]}')       # Зеленый
    st.sidebar.write(f'''🟣 Добавили новое поле, в стадии рассмотрения - {original_data[original_data["Статус работы"] == '2'].shape[0]}''')  # Фиолетовый
    st.sidebar.write(f'''🔴 Внесли изменения, в стадии рассмотрения - {original_data[original_data["Статус работы"] == '1'].shape[0]}''')       # Красный
    st.sidebar.write('⚪ Нажали "Внести изменения", но не отправили анкету')  # Серый
    st.sidebar.write('⚫ Нажали "Здесь поле", но не отправили анкету')        # Черный

    st.sidebar.markdown("---")
    st.sidebar.write(f'Дополнительно:')
    # Используем оригинальные данные для статистики
    # ЗАМЕНА СТАТИСТИКИ ПО ТИПАМ ПОКРЫТИЙ
    st.sidebar.write(f'Натуральных полей: {original_data[original_data["Тип покрытия"] == "Натуральное"].shape[0]}')
    st.sidebar.write(f'Искусственная трава: {original_data[original_data["Тип покрытия"] == "Искусственная трава"].shape[0]}')
    st.sidebar.write(f'Спортивное (резина, крошка и тп): {original_data[original_data["Тип покрытия"] == "Спортивное (резина, крошка и тп)"].shape[0]}')
    st.sidebar.write(f'Доска (паркет): {original_data[original_data["Тип покрытия"] == "Доска (паркет)"].shape[0]}')
    st.sidebar.write(f'Иное: {original_data[original_data["Тип покрытия"] == "Иное"].shape[0]}')
    st.sidebar.write(f'Нет информации: {original_data[original_data["Тип покрытия"] == "Нет информации"].shape[0]}')
