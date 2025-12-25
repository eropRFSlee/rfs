import streamlit as st
import pandas as pd
import json

# ==================== ОСНОВНОЙ КОД STREAMLIT ПРИЛОЖЕНИЯ ====================

# Настройка страницы
st.set_page_config(
    page_title="Реестр ОФИ", 
    layout="wide" # или другие настройки
)

st.markdown("""
<style>
    /* Фон приложения */
    .stApp {
        background-color: #204171;
    }
    
    /* Сайдбар - БЕЛЫЙ фон, ЧЁРНЫЙ текст */
    section[data-testid="stSidebar"] {
        background-color: white !important;
    }
    
    /* Весь текст в сайдбаре - ЧЁРНЫЙ */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: black !important;
    }
    
    /* Особо для элементов ввода */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] textarea {
        color: black !important;
        border-color: #666 !important;
    }
    
    /* Красные теги тоже с чёрным текстом */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #EF4444 !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="tag"] * {
        color: black !important;
    }
    
    header {
        background-color: #204171 !important;
    }
    
    /* Основной блок */
    .main .block-container {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Глобальный массив для полных данных баллунов
FULL_BALLOONS_DATA = []

# Сайдбар
st_select_region = st.sidebar.selectbox("Выберите свой регион", ['Регионы','01 Республика Адыгея', \
                                                                 '04 Республика Алтай',\
                                                                    '03 Республика Бурятия', \
                                                                        '17 Республика Тыва',\
                                                                            '19 Республика Хакасия',\
                                                                                '22 Алтайский  край',\
                                                                                    '24 Красноярский край',\
                                                                                        '38 Иркутская область',\
                                                                                            '42 Кемеровская область',\
                                                                                                '54 Новосибирская область',\
                                                                                                    '70 Томская область',\
                                                                                                        '75 Забайкальский край'])

if st_select_region != 'Регионы':
    data = pd.read_excel("{}.xlsx".format(st_select_region[:2]))
    
    all_object = data.shape[0]

    one_object = data[data['Наличие в реестрах'] == 1].shape[0]
    two_object = data[data['Наличие в реестрах'] == 2].shape[0]
    three_object = data[data['Наличие в реестрах'] == 3].shape[0]

    cnt_tablo = data[data['Наличие табло'].isin(['Да', 'Имеется'])].shape[0]
    cnt_drinage = data[data['Наличие дренажа'].isin(['Да','Имеется'])].shape[0]
    cnt_dress_room = data[data['Наличие раздевалок'] == 'Да'].shape[0]
    cnt_heat = data[data['Наличие подогрева'].isin(['Да', 'Имеется'])].shape[0]


    condition_reestr = ['Все']
    for x in sorted(data['Наличие в реестрах'].unique()):
        condition_reestr.append(x)
    
    

    conditional_size = ['Все']
    for x in sorted(data['Дисциплина_2'].unique()):
        conditional_size.append(x)
    

    conditional_dop = []
    conditional_dop.append('Наличие табло')
    conditional_dop.append('Наличие дренажа')
    conditional_dop.append('Наличие раздевалок')
    conditional_dop.append('Наличие подогрева')


    
    # -------------------------------------------------------------------------------------------------------------

    st_select_desciplyne = st.sidebar.selectbox("Выбор дисциплины", conditional_size)
    st_select_reestr = st.sidebar.selectbox("Наличие в реестрах", condition_reestr)
    st_select_dop_info = st.sidebar.multiselect("Фильтр по особенностям", conditional_dop,placeholder="Поле с..")

    # -------------------------------------------------------------------------------------------------------------

    if st_select_reestr == 1:
        data = data[data['Наличие в реестрах'] == 1]
    if st_select_reestr == 2:
        data = data[data['Наличие в реестрах'] == 2]
    if st_select_reestr == 3:
        data = data[data['Наличие в реестрах'] == 3]


    
    if st_select_desciplyne != 'Все':
        data = data[data['Дисциплина_2'] == st_select_desciplyne]


    if bool(st_select_dop_info):
       data = data[data[st_select_dop_info].apply(
    lambda row: all(val in ['Да', 'Имеется'] for val in row),
    axis=1)]
   


        
    # -------------------------------------------------------------------------------------------------------------

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

    YANDEX_API_KEY = "7fe74d5b-be45-47d1-9fc0-a0765598a4d7"

    # Создаем точки для адресов ----------------------------------------------------------------------------------------------
    points_js = ""
    for i in range(len(sirota)):
    

        adres_to_map = [str(full_name.iloc[i]).replace('"', '').replace('nan','-'),
                        str(short_name.iloc[i]).replace('"', '').replace('nan','-'),
                        str(adres.iloc[i]).replace('"', '').replace('nan','-'),
                        str(contact_name.iloc[i]).replace('"', '').replace('nan','-'),
                        str(owner.iloc[i]).replace('"', '').replace('nan','-'),
                        str(manager.iloc[i]).replace('"', '').replace('nan','-'),
                        str(user.iloc[i]).replace('"', '').replace('nan','-'),
                        str(rfs_id.iloc[i]).replace('"', '').replace('nan','-'),
                        str(type_objectt.iloc[i]).replace('"', '').replace('nan','-'),
                        str(disp_2.iloc[i]).replace('"', '').replace('nan','-'),
                        str(length.iloc[i]).replace('"', '').replace('nan','-'),
                        str(width.iloc[i]).replace('"', '').replace('nan','-'),
                        str(design_feature.iloc[i]).replace('"', '').replace('nan','-'),
                        str(type_of_coverage.iloc[i]).replace('"', '').replace('nan','-'),
                        str(capacity.iloc[i]).replace('"', '').replace('nan','-').replace('.0',''),
                        str(drainage.iloc[i]).replace('"', '').replace('nan','-'),
                        str(heating.iloc[i]).replace('"', '').replace('nan','-'),
                        str(scoreboard.iloc[i]).replace('"', '').replace('nan','-'),
                        str(dress_room.iloc[i]).replace('"', '').replace('nan','-'),
                        str(year.iloc[i]).replace('"', '').replace('nan','-').replace('.0','')
                        ]
        
        # ЛЁГКИЙ баллун для быстрой загрузки
        balloon_text = json.dumps(
            f'''<div style="font-size:12px;padding:5px">
                <b>Загрузка информации...</b><br>
                📍 {adres_to_map[2][:50]}...
            </div>''',
            ensure_ascii=False
        )
        
        # Сохраняем ПОЛНЫЕ данные для ленивой загрузки
        full_data = {
            'full_name': adres_to_map[0],
            'short_name': adres_to_map[1],
            'address': adres_to_map[2],
            'contact': adres_to_map[3],
            'owner': adres_to_map[4],
            'manager': adres_to_map[5],
            'user': adres_to_map[6],
            'rfs_id': adres_to_map[7],
            'type': adres_to_map[8],
            'discipline': adres_to_map[9],
            'size': f"{adres_to_map[10]}×{adres_to_map[11]}",
            'coverage': adres_to_map[13],
            'capacity': adres_to_map[14],
            'drainage': adres_to_map[15],
            'heating': adres_to_map[16],
            'scoreboard': adres_to_map[17],
            'dressing': adres_to_map[18],
            'year': adres_to_map[19],
            'id_egora': str(id_egora.iloc[i]) if pd.notna(id_egora.iloc[i]) else ""
        }
        FULL_BALLOONS_DATA.append(full_data)
        
        if in_reestr[i] == 1:
            icon_color = '#3B82F6'  # Синий
        elif in_reestr[i] == 2:
            icon_color = '#F59E0B'  # Желтый
        else:
            icon_color = '#10B981'  # Зеленый
        
        current_id_egora = str(id_egora.iloc[i]) if pd.notna(id_egora.iloc[i]) else ""
        
        points_js += f"""
            new ymaps.Placemark([{sirota.iloc[i]}, {dolgota.iloc[i]}], {{
                balloonContent: {balloon_text},
                balloonMaxWidth: 520,
                balloonMinWidth: 450,
                id_egora: "{current_id_egora}",
                index: {i},
                originalIconColor: '{icon_color}'
            }}, {{
                preset: 'islands#circleDotIcon',
                iconColor : '{icon_color}',
                draggable: false
            }})
        """
        
        # Добавляем запятую между точками, кроме последней
        if i < len(sirota) - 1:
            points_js += ","
    
    # Центр карты - средние координаты
    if len(sirota) > 0 and not sirota.isna().all():
        center_lat = sirota.mean()
        center_lon = dolgota.mean()
    else:
        center_lat, center_lon = 44.6, 40.1  

   # HTML карты с ленивой загрузкой баллунов
    zoom = 4 if st_select_region == '24 Красноярский край' else 6
    zoom = 5 if st_select_region == '75 Забайкальский край' else 6

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
        #map {{
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
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="copy-success" class="copy-success">✓ Скопировано в буфер обмена!</div>

    <script>
        // Передаём полные данные в JavaScript
        const FULL_BALLOONS = {json.dumps(FULL_BALLOONS_DATA, ensure_ascii=False)};
        
        // Глобальные переменные
        let map;
        let lastClickCoords = null;
        let lastClickAddress = null;
        
        // Функция для обработки клика на кнопку Изменить данные
        function handleConfirmClick(index) {{
            window.open("https://school-eev.bitrix24site.ru/crm_form_1rlgr/", "_blank");
        }}
        
        // Функция для обработки клика на кнопку Не поле
        function handleNotFieldClick(index) {{
            window.open("https://school-eev.bitrix24site.ru/crm_form_1rlgr/", "_blank");
        }}
        
        // Функция для обработки клика на кнопку Дубликат
        function handleDuplicateClick(index) {{
            window.open("https://school-eev.bitrix24site.ru/crm_form_1rlgr/", "_blank");
        }}
        
        // Функция для обработки клика на кнопку Здесь футбольное поле
        function handleFieldHereClick(coords) {{
            window.open("https://school-eev.bitrix24site.ru/crm_form_1rlgr/", "_blank");
        }}
        
        // Функция для копирования в буфер обмена
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                // Показываем уведомление об успехе
                const successDiv = document.getElementById('copy-success');
                successDiv.style.display = 'block';
                setTimeout(function() {{
                    successDiv.style.display = 'none';
                }}, 2000);
            }}, function(err) {{
                console.error('Ошибка при копировании: ', err);
                // Альтернативный метод для старых браузеров
                const textArea = document.createElement("textarea");
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
                
                // Показываем уведомление об успехе
                const successDiv = document.getElementById('copy-success');
                successDiv.style.display = 'block';
                setTimeout(function() {{
                    successDiv.style.display = 'none';
                }}, 2000);
            }});
        }}
        
        // Функция для копирования адреса и координатов
        function copyAddressAndCoords() {{
            if (lastClickAddress && lastClickCoords) {{
                const text = `Адрес: ${{lastClickAddress}}\\nКоординаты: ${{lastClickCoords[0].toFixed(6)}}, ${{lastClickCoords[1].toFixed(6)}}`;
                copyToClipboard(text);
            }}
        }}
        
        ymaps.ready(init);
        
        function init() {{
            // Создаём карту
            map = new ymaps.Map("map", {{
                center: [{center_lat}, {center_lon}],
                zoom: {zoom},
                type: 'yandex#satellite'
            }});

            // Добавляем поиск на карту
            map.controls.add(new ymaps.control.SearchControl({{
                options: {{
                    provider: 'yandex#search',
                    noPlacemark: false
                }}
            }}));

            // Добавляем точки на карту
            const points = [{points_js}];
            
            // При клике на точку загружаем полный баллун
            points.forEach(function(point, index) {{
                point.events.add('click', function(e) {{
                    var fullData = FULL_BALLOONS[index];
                    var id_egora = point.properties.get('id_egora');
                    
                    // Создаём полный HTML баллун
                    var fullBalloon = `
                        <div style="font-size: 10px; max-width: 500px; padding: 7px; line-height: 1.4;">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                                <div><strong>📋 Полное название:</strong><br><span>${{fullData.full_name}}</span></div>
                                <div><strong>⚽ Короткое название:</strong><br><span>${{fullData.short_name}}</span></div>
                            </div>
                            <div style="margin-bottom: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                                <strong>📍 Адрес:</strong><br>
                                <span>${{fullData.address}}</span>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                                <div><strong>📞 Контакт:</strong><br><span>${{fullData.contact}}</span></div>
                                <div><strong>👤 Собственник:</strong><br><span>${{fullData.owner}}</span></div>
                                <div><strong>🏢 Управляющая:</strong><br><span>${{fullData.manager}}</span></div>
                                <div><strong>👥 Пользователь:</strong><br><span>${{fullData.user}}</span></div>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                                <div><strong>🌐 РФС ID:</strong><br><span>${{fullData.id_egora}}</span></div>
                                <div><strong>Тип:</strong><br><span>${{fullData.type}}</span></div>
                                <div><strong>Дисциплина:</strong><br><span>${{fullData.discipline}}</span></div>
                                <div><strong>Размер:</strong><br><span>${{fullData.size}} м</span></div>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                                <div><strong>Покрытие:</strong><br><span>${{fullData.coverage}}</span></div>
                                <div><strong>Мест:</strong><br><span>${{fullData.capacity}}</span></div>
                                <div><strong>Дренаж:</strong><br><span>${{fullData.drainage}}</span></div>
                                <div><strong>Подогрев:</strong><br><span>${{fullData.heating}}</span></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                                <div><strong>Табло:</strong><br><span>${{fullData.scoreboard}}</span></div>
                                <div><strong>Раздевалки:</strong><br><span>${{fullData.dressing}}</span></div>
                                <div><strong>Год:</strong><br><span>${{fullData.year}}</span></div>
                            </div>
                            
                            <div style="margin-top: 12px; padding-top: 12px; border-top: 2px solid #e5e7eb;">
                                <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                                    <button onclick="handleConfirmClick(${{index}})" style="cursor: pointer; background: #10b981; border: none; padding: 8px 15px; border-radius: 4px; color: white; font-weight: bold; font-size: 12px;">
                                        ✅ Изменить данные
                                    </button>
                                    <button onclick="handleNotFieldClick(${{index}})" style="cursor: pointer; background: #ef4444; border: none; padding: 8px 15px; border-radius: 4px; color: white; font-weight: bold; font-size: 12px;">
                                        ❌ Отсутствует поле
                                    </button>
                                    <button onclick="handleDuplicateClick(${{index}})" style="cursor: pointer; background: #f59e0b; border: none; padding: 8px 15px; border-radius: 4px; color: white; font-weight: bold; font-size: 12px;">
                                        🔄 Дубликат
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    // Обновляем баллун точки
                    e.get('target').properties.set('balloonContent', fullBalloon);
                }});
                
                map.geoObjects.add(point);
            }});

            // Обработка клика на карте (для адреса по координатам)
            map.events.add('click', function(e) {{
                const coords = e.get('coords');
                const pixelCoords = e.get('pagePixels');
                lastClickCoords = coords;
                
                const oldInfo = document.querySelector('.address-info');
                if (oldInfo) {{
                    oldInfo.remove();
                }}
                
                ymaps.geocode(coords).then(function(res) {{
                    const firstGeoObject = res.geoObjects.get(0);
                    let address = 'Адрес не определен';
                    
                    if (firstGeoObject) {{
                        address = firstGeoObject.getAddressLine();
                    }}
                    
                    lastClickAddress = address;
                    
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'address-info';
                    infoDiv.style.left = (pixelCoords[0] + 15) + 'px';
                    infoDiv.style.top = (pixelCoords[1] - 15) + 'px';
                    
                    infoDiv.innerHTML = `
                        <div class="close-btn" onclick="this.parentElement.remove()">×</div>
                        <div class="address-title">📍 Адрес:</div>
                        <div style="margin-bottom: 10px;">${{address}}</div>
                        <div class="coords">
                            Координаты:<br>
                            ${{coords[0].toFixed(6)}}, ${{coords[1].toFixed(6)}}
                        </div>
                        <button onclick="copyAddressAndCoords()" 
                style="cursor: pointer; background: none; border: none; padding: 3px; font-size: 18px; color: #666; margin-left: 10px;"
                onmouseover="this.style.color='#8b5cf6'" 
                onmouseout="this.style.color='#666'"
                title="Скопировать адрес и координаты">
            📄
        </button>
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
            }});
        }}
        </script>
        </body>
        </html>
        """
    
    # Показываем карту
    st.components.v1.html(map_html, height=800)
    
     # -------------------------------------------------------------------------------------------------------------
    st.write(f'Всего объектов: {all_object}')
    st.write('По типам реестра:')
    st.write(f'Тип 1: {one_object}')
    st.write(f'Тип 2: {two_object}')
    st.write(f'Тип 3: {three_object}')

    st.write(f'Дополнительно:')
    st.write(f'С табло: {cnt_tablo}')
    st.write(f'С подогревом: {cnt_heat}')
    st.write(f'С раздевалками: {cnt_dress_room}')
    st.write(f'С дренажом: {cnt_drinage}')
