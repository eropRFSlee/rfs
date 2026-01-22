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
    
    /* Стили для карточек объектов */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
</style>
""", unsafe_allow_html=True)

FULL_BALLOONS_DATA = []

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
        
        response = requests.get(f'{WEBHOOK}crm.item.list', params=params)
        data = response.json()
        
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
        return '#EF4444', '🔴 Объект находится в стадии рассмотрения'
    elif str(status_of_work) == '2':
        return '#9444EF', '🟣 Добавили новое поле, на стадии рассмотрения'
    elif in_reestr == 1:
        return '#3B82F6', '🔵 Есть в РОИВ, но нет в ЦП'
    elif in_reestr == 2:
        return '#FFA500', '🟡 Есть только в ЦП'
    else:
        return '#10B981', '🟢 Есть в РОИВ и в ЦП'

# Функция для получения CSS класса цвета
def get_color_class(status_of_work, in_reestr):
    if str(status_of_work) == '1':
        return 'color-red', '🔴 Объект находится в стадии рассмотрения'
    elif str(status_of_work) == '2':
        return 'color-purple', '🟣 Добавили новое поле, на стадии рассмотрения'
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

# Создаем одну кнопку обновления в сайдбаре ДО выбора региона
st.sidebar.markdown("---")

st_select_region = st.sidebar.selectbox("Выберите свой регион", ['Регионы', 'Сибирь',\
                                                                 '03 Республика Бурятия', \
                                                                 '04 Республика Алтай',\
                                                                        '17 Республика Тыва',\
                                                                            '19 Республика Хакасия',\
                                                                                '22 Алтайский  край',\
                                                                                    '24 Красноярский край',\
                                                                                        '38 Иркутская область',\
                                                                                            '42 Кемеровская область',\
                                                                                                '54 Новосибирская область',\
                                                                                                    '70 Томская область',\
                                                                                                        '75 Забайкальский край'])

# Кнопка в сайдбаре для перезагрузки данных
if st_select_region != 'Регионы':
    if st_select_region == 'Сибирь':
        current_region_number = 0
        st_select_region = '000'
    else:
        current_region_number = int(st_select_region[0:2])
    
    # Переносим кнопку "Обновить карту и данные" в сайдбар
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Обновить карту и данные", key="refresh_all_btn", type="primary"):
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
    
    # Добавляем кнопки выбора режима в основное окно - МЕНЬШЕ И ОДИН ФОН
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        if st.button("🗺️ Карта", key="map_btn", type="primary" if st.session_state.view_mode == 'map' else "secondary", 
                     help="Переключить на карту", use_container_width=True):
            st.session_state.view_mode = 'map'
            st.rerun()
    with col2:
        if st.button("📋 Список", key="list_btn", type="primary" if st.session_state.view_mode == 'list' else "secondary",
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
    condition_reestr.append('🟣 Добавили новое поле, на стадии рассмотрения')  # Фиолетовый
    condition_reestr.append('🔴 Объект находится в стадии рассмотрения')       # Красный
    
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
    conditional_dop.append('Искусственное поле')
    conditional_dop.append('Натуральное поле')  # Добавляем новый фильтр

    # Добавляем список натуральных покрытий для фильтрации
    natural_coverings = [
        'Естественное покрытие', 'натуральное', 'Естественныйтравяной', 
        'Естественный травяной газон', 'Естественное покрытие «газонная трава»', 
        'Натуральное', 'естественное', 'естественное покрытие', 'Травяное', 
        'натуральный газон , требующий обновления', 'трава', 
        'натуральный газон (ведуться работы по замене газона на искусственное покрытие)',
        'Натуральная трава', 'Натуральный', 'травяной газон естественный', 
        'естественный газон', 'газон трава', 'газон', 'натуральный газон',
        'естественное (травяное) покрытие', 'натуральные', 'естественное озеленение',
        'земляное', 'естественное', 'Естественное покрытие', 'натуральное газонное покрытие',
        'естественный', 'трава искуственная зеленая', 'натуральнвая трава',
        'земляное, частично газон', 'газонное', 'естественный  газон',
        'земля', 'Земляное', 'гравий', 'естественный травянной покров',
        'Газонное, песчаное', 'земляное, газонное', 'естественное ',
        'газонная трава', 'естественное травяное покрытие', 'Натуральное',
        'Естественное земляное'
    ]

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
        "Фильтр по типу покрытия",
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

    if st_select_reestr == '🔴 Объект находится в стадии рассмотрения':
        data = data[data['Статус работы'] == '1']
    elif st_select_reestr == '🟣 Добавили новое поле, на стадии рассмотрения':
        data = data[data['Статус работы'] == '2']
    elif st_select_reestr == '🔵 Есть в РОИВ, но нет в ЦП':
        data = data[data['Наличие в реестрах'] == 1]
    elif st_select_reestr == '🟡 Есть только в ЦП':
        data = data[data['Наличие в реестрах'] == 2]
    elif st_select_reestr == '🟢 Есть в РОИВ и в ЦП':
        data = data[data['Наличие в реестрах'] == 3]

    if st_select_desciplyne != 'Все':
        if st_select_desciplyne == '11x11':
            data = data[data['Дисциплина_2'].isin([lst_to_combo[1]])]
        elif st_select_desciplyne =='Зал':
            data = data[data['Дисциплина_2'].isin(['Зал'])]
        else:
            data = data[data['Дисциплина_2'].isin(lst_to_combo[2].split(', '))]

    # ДОБАВЛЯЕМ ПРИМЕНЕНИЕ ФИЛЬТРА ПО ТИПУ ПОКРЫТИЯ
    if st_select_covering == 'Натуральное поле':
        data = data[data['Тип покрытия'].isin(natural_coverings)]
    elif st_select_covering == 'Искусственное поле':
        data = data[~data['Тип покрытия'].isin(natural_coverings)]
    elif st_select_covering == 'Наличие табло':
        data = data[data['Наличие табло'] == 'Y']
    elif st_select_covering == 'Наличие дренажа':
        data = data[data['Наличие дренажа'] == 'Y']
    elif st_select_covering == 'Наличие раздевалок':
        data = data[data['Наличие раздевалок'] == 'Y']
    elif st_select_covering == 'Наличие подогрева':
        data = data[data['Наличие подогрева'] == 'Y']


    
    
    # -------------------------------------------------------------------------------------------------------------
    
    # Проверяем режим просмотра
    if st.session_state.view_mode == 'list':
        
        # ИСПРАВЛЕНИЕ №1: Используем более компактный формат для данных, чтобы избежать проблем с большим количеством объектов
        # Подготавливаем данные для JavaScript
        objects_data = []
        for index, row in data.iterrows():
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
                        'Зал/не зал': to_slovar[10] if to_slovar[10] == 'Y' else ''
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
                        'Зал/не зал': to_slovar[8] if to_slovar[8] == 'Y' else ''
                    }
                
                # ИСПРАВЛЕНИЕ №3: Значения делаем жирными
                if 'slovar' in locals():
                    result_parts = []
                    for key, value in slovar.items():
                        if value != '' and value is not None:
                            # ИСПРАВЛЕНИЕ №3: Значения делаем жирными
                            result_parts.append(f'{key}: <strong>{value}</strong>')

                    if result_parts:
                        provided_data = '<br>'.join(result_parts)
            
            # ИСПРАВЛЕНИЕ №1: Минимизируем данные, передаваемые в JSON
            objects_data.append({
                'i': index,  # Более короткое имя
                'fn': str(row['Полное (официальное) название объекта']) if pd.notna(row['Полное (официальное) название объекта']) else '-',
                'ad': str(row['Адрес']) if pd.notna(row['Адрес']) else '-',
                'ln': str(row['Длина футбольного поля']) if pd.notna(row['Длина футбольного поля']) else '-',
                'wd': str(row['Ширина футбольного поля']) if pd.notna(row['Ширина футбольного поля']) else '-',
                'd2': str(row['Дисциплина_2']) if pd.notna(row['Дисциплина_2']) else '-',
                'id': id_egora_value,
                'cl': color_class,
                'cd': color_description,
                'sz': f"{str(row['Длина футбольного поля'])}×{str(row['Ширина футбольного поля'])}" 
                        if pd.notna(row['Длина футбольного поля']) and pd.notna(row['Ширина футбольного поля']) else '-',
                'sw': status_of_work,
                'pd': provided_data  # HTML с жирным выделением значений
            })
        
        # ИСПРАВЛЕНИЕ №1: Упрощаем HTML и добавляем виртуальный скроллинг для больших списков
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
                    padding: 5px;
                    max-height: 750px;
                    overflow-y: auto;
                }}
                
                .card {{
                    background-color: white;
                    border-radius: 8px;
                    padding: 12px;
                    margin-bottom: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    border-left: 3px solid #3b82f6;
                }}
                
                .card h4 {{
                    color: #2a4a80;
                    margin-bottom: 6px;
                    margin-top: 0;
                    font-size: 14px;
                    line-height: 1.2;
                }}
                
                .card-info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 8px;
                    margin-bottom: 8px;
                }}
                
                .card-info-item {{
                    display: flex;
                    flex-direction: column;
                }}
                
                .card-info-label {{
                    font-weight: bold;
                    color: #2a4a80;
                    font-size: 11px;
                    margin-bottom: 2px;
                }}
                
                .card-info-value {{
                    color: #333;
                    font-size: 12px;
                    word-break: break-word;
                    line-height: 1.3;
                }}
                
                .color-label {{
                    display: inline-flex;
                    align-items: center;
                    padding: 3px 6px;
                    border-radius: 3px;
                    font-size: 11px;
                    font-weight: bold;
                    margin-top: 4px;
                }}
                
                .color-indicator {{
                    display: inline-block;
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    margin-right: 6px;
                }}
                
                .color-blue {{ background-color: #3B82F6; }}
                .color-yellow {{ background-color: #FFA500; }}
                .color-green {{ background-color: #10B981; }}
                .color-purple {{ background-color: #9444EF; }}
                .color-red {{ background-color: #EF4444; }}
                
                .buttons-container {{
                    display: flex;
                    gap: 6px;
                    margin-top: 8px;
                    flex-wrap: wrap;
                }}
                
                .btn {{
                    padding: 5px 10px;
                    border-radius: 3px;
                    border: none;
                    cursor: pointer;
                    font-size: 11px;
                    font-weight: bold;
                    transition: background-color 0.2s;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 4px;
                    min-width: 120px;
                    height: 28px;
                }}
                
                .btn-copy {{
                    background-color: #3b82f6;
                    color: white;
                }}
                
                .btn-copy:hover {{
                    background-color: #2563eb;
                }}
                
                .btn-form {{
                    background-color: #10b981;
                    color: white;
                }}
                
                .btn-form:hover {{
                    background-color: #059669;
                }}
                
                .btn-form-opened {{
                    background-color: #6b7280;
                    color: white;
                    cursor: default !important;
                }}
                
                .btn-form-disabled {{
                    background-color: #9ca3af;
                    color: white;
                    cursor: not-allowed !important;
                    opacity: 0.7;
                }}
                
                .notification {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background-color: #10b981;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 5px;
                    z-index: 10000;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.15);
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    opacity: 0;
                    transition: opacity 0.3s;
                    font-size: 12px;
                }}
                
                .notification.show {{
                    opacity: 1;
                }}
                
                .notification-icon {{
                    font-size: 16px;
                }}
                
                hr {{
                    border: none;
                    height: 1px;
                    background-color: #e5e7eb;
                    margin: 10px 0;
                }}
                
                /* Убираем лишние отступы */
                p {{
                    margin: 2px 0;
                }}
                
                /* Стили для provided_data */
                /* ИСПРАВЛЕНИЕ №1: Черный текст в provided_data */
                .provided-data-section {{
                    background-color: #F0F9FF;
                    border: 1px solid #93C5FD;
                    border-radius: 6px;
                    padding: 10px;
                    margin: 8px 0;
                }}
                
                .provided-data-section-red {{
                    background-color: #FEF2F2;
                    border: 1px solid #FCA5A5;
                    border-radius: 6px;
                    padding: 10px;
                    margin: 8px 0;
                }}
                
                /* ИСПРАВЛЕНИЕ №2: Одна рамка для статуса '2' */
                .provided-data-section-purple {{
                    background-color: #F3E8FF;
                    border: 1px solid #9444EF;
                    border-radius: 6px;
                    padding: 10px;
                    margin: 8px 0;
                }}
                
                .provided-data-title {{
                    color: #1D4ED8;
                    font-weight: bold;
                    font-size: 12px;
                    margin-bottom: 6px;
                }}
                
                .provided-data-title-red {{
                    color: #DC2626;
                    font-weight: bold;
                    font-size: 12px;
                    margin-bottom: 6px;
                }}
                
                .provided-data-title-purple {{
                    color: #9444EF;
                    font-weight: bold;
                    font-size: 12px;
                    margin-bottom: 6px;
                }}
                
                /* ИСПРАВЛЕНИЕ №1: Черный текст */
                .provided-data-content {{
                    color: #000000;
                    font-size: 11px;
                    white-space: pre-line;
                    line-height: 1.3;
                }}
                
                /* ИСПРАВЛЕНИЕ №3: Жирные значения */
                .provided-data-content strong {{
                    font-weight: bold;
                    color: #000000;
                }}
            </style>
        </head>
        <body>
            <div class="objects-container" id="objects-container">
                <!-- Объекты будут добавлены через JavaScript -->
            </div>
            
            <div id="notification" class="notification" style="display: none;">
                <span class="notification-icon">✓</span>
                <span id="notification-text"></span>
            </div>
            
            <script>
                // ИСПРАВЛЕНИЕ №1: Используем более компактные имена переменных
                const objectsData = {json.dumps(objects_data, ensure_ascii=False)};
                
                // Состояние кнопок
                let buttonStates = {{}};
                
                // Функция для показа уведомления
                function showNotification(message, duration = 2000) {{
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
                
                // Функция для копирования текста в буфер обмена
                function copyToClipboard(text, index) {{
                    if (navigator.clipboard && navigator.clipboard.writeText) {{
                        navigator.clipboard.writeText(text)
                            .then(() => {{
                                showNotification('✓ ID скопирован: ' + text);
                            }})
                            .catch(err => {{
                                console.error('Clipboard API error:', err);
                                fallbackCopy(text);
                            }});
                    }} else {{
                        fallbackCopy(text);
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
                
                // Функция для открытия формы
                function openForm(index, statusOfWork) {{
                    if (statusOfWork === '1') {{
                        return false;
                    }}
                    
                    const url = "https://school-eev.bitrix24site.ru/crm_form_drmcv/";
                    
                    buttonStates[index] = true;
                    
                    const button = document.getElementById('form-btn-' + index);
                    if (button) {{
                        button.textContent = '📋 Форма была открыта';
                        button.className = 'btn btn-form-opened';
                        
                        button.onclick = function() {{
                            window.open(url, '_blank');
                        }};
                    }}
                    
                    window.open(url, '_blank');
                    return true;
                }}
                
                // Функция для создания карточки объекта
                function createObjectCard(obj) {{
                    const card = document.createElement('div');
                    card.className = 'card';
                    
                    const statusOfWork = obj.sw || '0';
                    
                    if (buttonStates[obj.i] === undefined) {{
                        buttonStates[obj.i] = false;
                    }}
                    
                    // ИСПРАВЛЕНИЕ №2: Одна рамка для статуса '2'
                    let providedDataHTML = '';
                    if (obj.pd) {{
                        if (statusOfWork === '1') {{
                            providedDataHTML = `
                                <div class="provided-data-section-red">
                                    <div class="provided-data-title-red">🔴 Объект находится в стадии рассмотрения</div>
                                    <div class="provided-data-content">${{obj.pd}}</div>
                                </div>
                            `;
                        }} else if (statusOfWork === '2') {{
                            // ИСПРАВЛЕНИЕ №2: Одна рамка с заголовком и данными
                            providedDataHTML = `
                                <div class="provided-data-section-purple">
                                    <div class="provided-data-title-purple">🟣 Добавили новое поле, на стадии рассмотрения</div>
                                    <div class="provided-data-content">${{obj.pd}}</div>
                                </div>
                            `;
                        }} else {{
                            providedDataHTML = `
                                <div class="provided-data-section">
                                    <div class="provided-data-title">📋 Предоставленные данные:</div>
                                    <div class="provided-data-content">${{obj.pd}}</div>
                                </div>
                            `;
                        }}
                    }}
                    
                    let formButtonHTML = '';
                    if (statusOfWork !== '1') {{
                        let formBtnClass = 'btn-form';
                        let formBtnText = '✅ Внести изменения';
                        let formBtnOnclick = `openForm(${{obj.i}}, '${{statusOfWork}}')`;
                        
                        if (buttonStates[obj.i]) {{
                            formBtnClass = 'btn-form-opened';
                            formBtnText = '📋 Форма была открыта';
                            formBtnOnclick = `window.open('https://school-eev.bitrix24site.ru/crm_form_drmcv/', '_blank')`;
                        }}
                        
                        formButtonHTML = `
                            <button id="form-btn-${{obj.i}}" 
                                    onclick="${{formBtnOnclick}}" 
                                    class="btn ${{formBtnClass}}" 
                                    title="Открыть форму для внесения изменений">
                                ${{formBtnText}}
                            </button>
                        `;
                    }}
                    
                    card.innerHTML = `
                        <h4>${{obj.fn}}</h4>
                        <div class="card-info-grid">
                            <div class="card-info-item">
                                <span class="card-info-label">📍 Адрес:</span>
                                <span class="card-info-value">${{obj.ad}}</span>
                            </div>
                            <div class="card-info-item">
                                <span class="card-info-label">📏 Размер:</span>
                                <span class="card-info-value">${{obj.sz}}</span>
                            </div>
                            <div class="card-info-item">
                                <span class="card-info-label">⚽ Дисциплина:</span>
                                <span class="card-info-value">${{obj.d2}}</span>
                            </div>
                            <div class="card-info-item">
                                <div class="color-label">
                                    ${{obj.cd}}
                                </div>
                            </div>
                        </div>
                        <div class="card-info-item" style="margin-top: 4px;">
                            <span class="card-info-label">🌐 ID:</span>
                            <span class="card-info-value">${{obj.id}}</span>
                        </div>
                        ${{providedDataHTML}}
                        <div class="buttons-container">
                            <button onclick="copyToClipboard('${{obj.id}}', ${{obj.i}})" 
                                    class="btn btn-copy" title="Скопировать ID в буфер обмена">
                                📄 Копировать ID
                            </button>
                            ${{formButtonHTML}}
                        </div>
                    `;
                    
                    return card;
                }}
                
                // Функция для отображения всех объектов
                function renderObjects() {{
                    const container = document.getElementById('objects-container');
                    container.innerHTML = '';
                    
                    if (objectsData.length === 0) {{
                        container.innerHTML = '<div class="card"><p style="text-align: center; color: #666;">Объекты не найдены</p></div>';
                        return;
                    }}
                    
                    // ИСПРАВЛЕНИЕ №1: Рендерим объекты с ограничением, чтобы не перегружать DOM
                    const batchSize = 50; // Рендерим по 50 объектов
                    const totalObjects = objectsData.length;
                    
                    function renderBatch(startIndex) {{
                        const endIndex = Math.min(startIndex + batchSize, totalObjects);
                        
                        for (let i = startIndex; i < endIndex; i++) {{
                            const obj = objectsData[i];
                            const card = createObjectCard(obj);
                            container.appendChild(card);
                            
                            if (i < totalObjects - 1) {{
                                const hr = document.createElement('hr');
                                container.appendChild(hr);
                            }}
                        }}
                        
                        // Если есть еще объекты, планируем следующий batch
                        if (endIndex < totalObjects) {{
                            setTimeout(() => renderBatch(endIndex), 0);
                        }}
                    }}
                    
                    // Начинаем рендеринг с первого batch
                    renderBatch(0);
                }}
                
                // Инициализация при загрузке страницы
                document.addEventListener('DOMContentLoaded', renderObjects);
                
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', renderObjects);
                }} else {{
                    renderObjects();
                }}
            </script>
        </body>
        </html>
        """
        
        # Отображаем JS список через components.v1.html
        st.components.v1.html(objects_html, height=800, scrolling=True)
    
    else:
        # Продолжаем отображение карты (остальной код карты)
        sirota = data['Широта']
        dolgota = data['Долгота']
        
        full_name = data['Полное (официальное) название объекта'] # 0
        short_name = data['Короткое (спортивное) название объекта'] # 1
        adres = data['Адрес'] # 2
        contact_name = data['Контактное лицо'] # 3
        owner = data['Собственник (ОГРН)'] # 4
        manager = data['Управляющая компания (ОГРН)'] #5
        user = data['Пользователь (ОГРН)'] #6
        rfs_id= data['РФС_ID'] #7
        type_objectt = data['Тип Объекта '] #8
        disciplyne = data['Дисциплина '] #9
        length = data['Длина футбольного поля'] # 10
        width = data['Ширина футбольного поля'] # 11
        design_feature = data['Конструктивная особенность'] # 12
        type_of_coverage = data['Тип покрытия'] # 13
        capacity = data['Количество мест для зрителей'] # 14
        capacity = capacity.astype(str)
        drainage = data['Наличие дренажа'] # 15
        heating = data['Наличие подогрева'] # 16
        scoreboard = data['Наличие табло'] # 17
        dress_room = data['Наличие раздевалок'] # 18
        year = data['Год ввода в эксплуатацию/год капитального ремонта'] # 19
        year = year.astype(str)
        in_reestr = data['Наличие в реестрах'].to_list()
        disp_2 = data['Дисциплина_2']
        id_egora = data['id_egora']
        status_of_work = data['Статус работы']
        info = data['То, что заполнили РОИВ']

        YANDEX_API_KEY = "7fe74d5b-be45-47d1-9fc0-a0765598a4d7"

        # Подготовка данных для карты - СОКРАЩЕННАЯ версия
        points_data = []
        for i in range(len(sirota)):
            # Обработка информации для объектов со статусом работы '1' или '2'
            result_string = ""
            if status_of_work.iloc[i] in ('1', '2'):
                to_slovar = data['То, что заполнили РОИВ'].iloc[i].replace('<br>', '|').split('|')
                
                if status_of_work.iloc[i] == '1' and len(to_slovar) >= 11:
                    slovar = {
                        'Полное(официальное) название объекта' : to_slovar[0],
                        'Короткое (спортивное) название объекта' : to_slovar[1],
                        'Адрес' : to_slovar[2],
                        'Широта и долгота' : to_slovar[3],
                        'Длина' : to_slovar[4],
                        'Ширина' : to_slovar[5],
                        'Тип покрытия' : to_slovar[6],
                        'Отправитель' : to_slovar[7],
                        'Подтвердить' : to_slovar[8] if to_slovar[8] == 'Y' else '',
                        'Удалить' : to_slovar[9] if to_slovar[9] == 'Y' else '',
                        'Зал/не зал' : to_slovar[10] if to_slovar[10] == 'Y' else ''
                    }
                elif status_of_work.iloc[i] == '2' and len(to_slovar) >= 9:
                    slovar = {
                        'Полное(официальное) название объекта' : to_slovar[0],
                        'Короткое (спортивное) название объекта' : to_slovar[1],
                        'Адрес' : to_slovar[2],
                        'Широта и долгота' : to_slovar[3],
                        'Длина' : to_slovar[4],
                        'Ширина' : to_slovar[5],
                        'Тип покрытия' : to_slovar[6],
                        'Отправитель' : to_slovar[7],
                        'Зал/не зал' : to_slovar[8] if to_slovar[8] == 'Y' else ''
                    }
                
                # ИСПРАВЛЕНИЕ №3: Значения делаем жирными
                if slovar:
                    result_parts = []
                    for key, value in slovar.items():
                        if value != '' and value is not None:
                            # ИСПРАВЛЕНИЕ №3: Значения делаем жирными
                            result_parts.append(f'{key}: <strong>{value}</strong>')

                    if result_parts:
                        result_string = '<br>'.join(result_parts)
            
            # Определяем цвет точки
            icon_color, _ = get_point_color(str(status_of_work.iloc[i]), in_reestr[i])
            
            current_id_egora = str(int(float(id_egora.iloc[i]))) if pd.notna(id_egora.iloc[i]) and str(id_egora.iloc[i]).replace('.0', '') != 'nan' else ""
            
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
                'size': f"{str(length.iloc[i]).replace('nan','-')}×{str(width.iloc[i]).replace('nan','-')}",
                'coverage': str(type_of_coverage.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(type_of_coverage.iloc[i]) else '-',
                'capacity': str(capacity.iloc[i]).replace('nan','-') if pd.notna(capacity.iloc[i]) else '-',
                'drainage': str(drainage.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(drainage.iloc[i]) else '-',
                'heating': str(heating.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(heating.iloc[i]) else '-',
                'scoreboard': str(scoreboard.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(scoreboard.iloc[i]) else '-',
                'dressing': str(dress_room.iloc[i]).replace('"', '').replace('nan','-') if pd.notna(dress_room.iloc[i]) else '-',
                'year': str(year.iloc[i]).replace('nan','-') if pd.notna(year.iloc[i]) else '-',
                'provided_data': result_string
            })

        # Центр карты - средние координаты
        if len(sirota) > 0 and not sirota.isna().all():
            center_lat = sirota.mean()
            center_lon = dolgota.mean()
        else:
            center_lat, center_lon = 44.6, 40.1  

        # HTML карты с оптимизированным кодом
        zoom = 4 if st_select_region == '24 Красноярский край' else 1
        zoom = 4 if st_select_region == '75 Забайкальский край' else 5
        
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
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
            max-width: 350px;
            z-index: 1000;
            border: 2px solid #3b82f6;
            font-family: Arial, sans-serif;
            left: 20px;
            bottom: 20px;
        }}
        .close-btn {{
            position: absolute;
            top: -10px;
            right: -10px;
            background: #3b82f6;
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            text-align: center;
            line-height: 24px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .close-btn:hover {{
            background: #2563eb;
        }}
        .address-title {{
            color: #3b82f6;
            margin-bottom: 8px;
            font-size: 16px;
        }}
        .coords {{
            color: #666;
            font-size: 13px;
            margin-top: 8px;
            font-family: monospace;
        }}
        .field-btn {{
            margin-top: 10px;
            text-align: center;
        }}
        .field-btn button {{
            cursor: pointer;
            background: #3b82f6;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            font-size: 12px;
            width: 100%;
        }}
        .field-btn button:hover {{
            background: #2563eb;
        }}
        .copy-btn {{
            margin-top: 10px;
            text-align: center;
        }}
        .copy-btn button {{
            cursor: pointer;
            background: #8b5cf6;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            font-size: 12px;
            width: 100%;
        }}
        .copy-btn button:hover {{
            background: #7c3aed;
        }}
        .copy-success {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 9999;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            display: none;
        }}
        .address-item {{
            margin-bottom: 12px;
            padding-bottom: 12px;
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
            margin-bottom: 5px;
        }}
        .item-label {{
            font-weight: bold;
            color: #3b82f6;
            font-size: 14px;
        }}
        .item-content {{
            color: #333;
            font-size: 13px;
            word-break: break-word;
        }}
        .copy-icon-btn {{
            cursor: pointer;
            background: none;
            border: none;
            padding: 3px;
            font-size: 18px;
            color: #666;
            transition: color 0.2s;
        }}
        .copy-icon-btn:hover {{
            color: #8b5cf6;
        }}
        .status-warning {{
            background-color: #F3E8FF;
            border: 2px solid #9444EF;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }}
        .status-warning-title {{
            color: #9444EF;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 10px;
            text-align: center;
        }}
        .status-warning-text {{
            color: #6B21A8;
            font-size: 14px;
        }}
        /* ИСПРАВЛЕНИЕ №3: Жирные значения */
        .provided-data-content strong {{
            font-weight: bold;
            color: #000000;
        }}
        .provided-data-section {{
            background-color: #F0F9FF;
            border: 1px solid #93C5FD;
            border-radius: 6px;
            padding: 12px;
            margin: 10px 0;
        }}
        .provided-data-title {{
            color: #1D4ED8;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        /* ИСПРАВЛЕНИЕ №1: Черный текст */
        .provided-data-content {{
            color: #000000;
            font-size: 12px;
            white-space: pre-line;
            line-height: 1.4;
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
        let placemarks = []; // Массив для хранения всех меток
        
        // Функция для обработки клика на кнопку Внести изменения
        function handleConfirmClick(index) {{
            // Получаем данные объекта
            const pointData = POINTS_DATA[index];
            const statusOfWork = pointData.status_of_work || '0';
            
            // Проверяем статус работы - если '1', то кнопка неактивна
            if (statusOfWork === '1') {{
                alert('Объект находится в стадии рассмотрения. Внести изменения нельзя.');
                return false;
            }}
            
            // Открываем форму для изменений
            window.open("https://school-eev.bitrix24site.ru/crm_form_drmcv/", "_blank");
            
            // Находим соответствующую метку и меняем её цвет на серый
            if (placemarks[index]) {{
                const placemark = placemarks[index];
                
                // Изменяем цвет метки на серый
                placemark.options.set('iconColor', '#808080');
                
                // Обновляем баллун
                const updatedBalloon = getBalloonContent(pointData, true);
                placemark.properties.set('balloonContent', updatedBalloon);
            }}
            
            return true;
        }}
        
        // Функция для создания HTML баллуна
        function getBalloonContent(pointData, isChanged = false) {{
            const statusOfWork = pointData.status_of_work || '0';
            const providedData = pointData.provided_data || '';
            
            // Если статус работы равен '2', показываем упрощенный баллун
            if (statusOfWork === '2') {{
                let providedDataHTML = '';
                if (providedData) {{
                    // ИСПРАВЛЕНИЕ №2: Одна рамка с заголовком и данными
                    providedDataHTML = `
                        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e5e7eb;">
                            <div style="color: #9444EF; font-weight: bold; font-size: 12px; margin-bottom: 5px;">
                                📋 Предоставленные данные:
                            </div>
                            <div style="color: #000000; font-size: 11px;">${{providedData}}</div>
                        </div>
                    `;
                }}
                
                return `
                    <div style="font-size: 10px; max-width: 500px; padding: 7px; line-height: 1.4;">
                        <div style="margin-bottom: 6px; padding-top: 6px;">
                            <strong>📍 Адрес:</strong><br>
                            <span>${{pointData.address}}</span>
                        </div>
                        
                        <div class="status-warning">
                            <div class="status-warning-title">🟣 Добавили новое поле, на стадии рассмотрения</div>
                            ${{providedDataHTML}}
                        </div>
                    </div>
                `;
            }}
            
            // Стандартный баллун для остальных статусов
            let statusHTML = '';
            if (isChanged || statusOfWork === '1') {{
                let providedDataHTML = '';
                if (providedData && !isChanged) {{
                    if (statusOfWork === '1') {{
                        providedDataHTML = `
                            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e5e7eb;">
                                <div style="color: #DC2626; font-weight: bold; font-size: 12px; margin-bottom: 5px;">
                                    📋 Предоставленные данные:
                                </div>
                                <div style="color: #000000; font-size: 11px;">${{providedData}}</div>
                            </div>
                        `;
                    }}
                }}
                
                statusHTML = `
                    <div style="background-color: ${{isChanged ? '#F3F4F6' : '#FEF2F2'}}; 
                         border: 1px solid ${{isChanged ? '#D1D5DB' : '#FCA5A5'}}; 
                         padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                        <div style="color: ${{isChanged ? '#6B7280' : '#DC2626'}}; font-weight: bold; display: flex; align-items: center; gap: 5px;">
                            <span>${{isChanged ? '⚪' : '🔴'}}</span>
                            <span>${{isChanged ? 'Нажали "Внести изменения", но не отправили анкету' : 'Объект находится в стадии рассмотрения'}}</span>
                        </div>
                        ${{providedDataHTML}}
                    </div>
                `;
            }}
            
            // Определяем, показывать ли кнопку "Внести изменения"
            const showConfirmButton = (statusOfWork !== '1');
            const confirmButtonSection = showConfirmButton ? `
                <div style="margin-top: 12px; padding-top: 12px; border-top: 2px solid #e5e7eb;">
                    <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                        <button onclick="handleConfirmClick(${{pointData.index}})" 
                                style="cursor: pointer; background: ${{statusOfWork === '1' ? '#9ca3af' : '#10b981'}}; 
                                       border: none; padding: 8px 15px; border-radius: 4px; 
                                       color: white; font-weight: bold; font-size: 12px;
                                       ${{statusOfWork === '1' ? 'cursor: not-allowed;' : ''}}"
                                ${{statusOfWork === '1' ? 'disabled' : ''}}
                                title="${{statusOfWork === '1' ? 'Объект на рассмотрении, изменения внести нельзя' : 'Внести изменения'}}">
                            ${{statusOfWork === '1' ? '⏳ На рассмотрении' : '✅ Внести изменения'}}
                        </button>
                    </div>
                </div>
            ` : '';
            
            return `
                <div style="font-size: 10px; max-width: 500px; padding: 7px; line-height: 1.4;">
                    ${{statusHTML}}
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                        <div><strong>📋 Полное название:</strong><br><span>${{pointData.full_name}}</span></div>
                        <div><strong>⚽ Короткое название:</strong><br><span>${{pointData.short_name}}</span></div>
                    </div>
                    <div style="margin-bottom: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                        <strong>📍 Адрес:</strong><br>
                        <span>${{pointData.address}}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                        <div><strong>📞 Контакт:</strong><br><span>${{pointData.contact}}</span></div>
                        <div><strong>👤 Собственник:</strong><br><span>${{pointData.owner}}</span></div>
                        <div><strong>🏢 Управляющая:</strong><br><span>${{pointData.manager}}</span></div>
                        <div><strong>👥 Пользователь:</strong><br><span>${{pointData.user}}</span></div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
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
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                        <div><strong>Покрытие:</strong><br><span>${{pointData.coverage}}</span></div>
                        <div><strong>Мест:</strong><br><span>${{pointData.capacity}}</span></div>
                        <div><strong>Дренаж:</strong><br><span>${{pointData.drainage}}</span></div>
                        <div><strong>Подогрев:</strong><br><span>${{pointData.heating}}</span></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                        <div><strong>Табло:</strong><br><span>${{pointData.scoreboard}}</span></div>
                        <div><strong>Раздевалки:</strong><br><span>${{pointData.dressing}}</span></div>
                        <div><strong>Год:</strong><br><span>${{pointData.year}}</span></div>
                    </div>
                    ${{confirmButtonSection}}
                </div>
            `;
        }}
        
        // Функция для обработки клика на кнопку Здесь футбольное поле
        function handleFieldHereClick(coords) {{
            window.open("https://school-eev.bitrix24site.ru/crm_form_saeda/", "_blank");
            
            // Создаем черную точку
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
            
            map.geoObjects.add(blackPlacemark);
        }}
        
        // Функция для копирования в буфер обмена
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
                }}, 2000);
            }}
        }}
        
        // Функция для копирования адреса
        function copyAddress() {{
            if (lastClickAddress) {{
                copyToClipboard(lastClickAddress);
            }}
        }}
        
        // Функция для копирования координат
        function copyCoords() {{
            if (lastClickCoords) {{
                const coordsText = `${{lastClickCoords[0].toFixed(6)}}, ${{lastClickCoords[1].toFixed(6)}}`;
                copyToClipboard(coordsText);
            }}
        }}
        
        // Функция для копирования номера региона
        function copyRegionNumber() {{
            copyToClipboard("{int(st_select_region[0:2])}");
        }}
        
        // Функция для копирования РФС ID
        function copyRfsId(rfsId) {{
            if (rfsId) {{
                copyToClipboard(rfsId);
            }}
        }}
        
        // Функция для создания информации о местоположении
        function createAddressInfo(coords, address) {{
            const oldInfo = document.querySelector('.address-info');
            if (oldInfo) {{
                oldInfo.remove();
            }}
            
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
            
            // Удаление при клике вне блока
            setTimeout(() => {{
                document.addEventListener('click', function closeOnOutsideClick(event) {{
                    if (!infoDiv.contains(event.target)) {{
                        infoDiv.remove();
                        document.removeEventListener('click', closeOnOutsideClick);
                    }}
                }});
            }}, 10);
        }}
        
        ymaps.ready(init);
        
        function init() {{
            // Создаём карту
            map = new ymaps.Map("map-{map_unique_id}", {{
                center: [{center_lat}, {center_lon}],
                zoom: {zoom},
                type: 'yandex#satellite'
            }});

            // Добавляем стандартный поиск
            map.controls.add(new ymaps.control.SearchControl({{
                options: {{
                    provider: 'yandex#search',
                    noPlacemark: true,
                    placeholderContent: 'Поиск на карте'
                }}
            }}));

            // Оптимизация: создаем метки в один проход
            const geoObjects = new ymaps.GeoObjectCollection(null, {{
                preset: 'islands#circleDotIcon',
                draggable: false
            }});
            
            // Добавляем точки
            POINTS_DATA.forEach(point => {{
                if (point.lat && point.lon && point.lat !== 0 && point.lon !== 0) {{
                    const placemark = new ymaps.Placemark(
                        [point.lat, point.lon],
                        {{
                            balloonContent: '<div style="font-size:12px;padding:5px"><b>Загрузка...</b></div>',
                            balloonMaxWidth: 520,
                            balloonMinWidth: 450,
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
                    
                    // Добавляем обработчик клика для загрузки полного баллуна
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

            // Обработка клика на карте
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
        st.components.v1.html(map_html, height=700, scrolling=False)
    
    # -------------------------------------------------------------------------------------------------------------
    st.sidebar.markdown("---")
    # Используем оригинальные данные для статистики (до фильтрации)
    st.sidebar.write(f'Всего объектов: {original_data.shape[0]}')
    st.sidebar.markdown("---")
    st.sidebar.write('Типы точек:')
    st.sidebar.write('🔵 Есть в РОИВ, но нет в ЦП')  # Синий
    st.sidebar.write('🟡 Есть только в ЦП')          # Желтый
    st.sidebar.write('🟢 Есть в РОИВ и в ЦП')       # Зеленый
    st.sidebar.write('🟣 Добавили новое поле, на стадии рассмотрения')  # Фиолетовый
    st.sidebar.write('🔴 Объект находится в стадии рассмотрения')       # Красный
    st.sidebar.write('⚪ Нажали "Внести изменения", но не отправили анкету')  # Серый
    st.sidebar.write('⚫ Нажали "Здесь поле", но не отправили анкету')        # Черный

    st.sidebar.markdown("---")
    st.sidebar.write(f'Дополнительно:')
    # Используем оригинальные данные для статистики
    st.sidebar.write(f'Натуральных полей: {original_data[original_data["Тип покрытия"].isin(natural_coverings)].shape[0]}')
    st.sidebar.write(f'Искусственных полей: {original_data[~original_data["Тип покрытия"].isin(natural_coverings)].shape[0]}')
    st.sidebar.write(f'''Только субьект: {original_data[original_data["Наличие в реестрах"] == 1].shape[0]}''')
    st.sidebar.write(f'''Только ЦП: {original_data[original_data["Наличие в реестрах"] == 2].shape[0]}''')
    st.sidebar.write(f'''ЦП и субьект: {original_data[original_data["Наличие в реестрах"] == 3].shape[0]}''')
    st.sidebar.write(f'С табло: {original_data[original_data["Наличие табло"] == "Y"].shape[0]}')
    st.sidebar.write(f'С подогревом: {original_data[original_data["Наличие подогрева"] == "Y"].shape[0]}')
    st.sidebar.write(f'С раздевалками: {original_data[original_data["Наличие раздевалок"] == "Y"].shape[0]}')
    st.sidebar.write(f'С дренажом: {original_data[original_data["Наличие дренажа"] == "Y"].shape[0]}')