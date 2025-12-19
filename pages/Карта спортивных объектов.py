import streamlit as st
import pandas as pd
import json


st.set_page_config(layout="wide", page_title="Реестр ОФИ")


FULL_BALLOONS_DATA = []


st_select_region = st.sidebar.selectbox("Выберите свой регион", ['Регионы','01 Республика Адыгея', \
                                                                 '04 Республика Алтай',\
                                                                    '03 Республика Бурятия', \
                                                                        '17 Республика Тыва',\
                                                                            '19 Республика Хакасия',\
                                                                                '22 Алтайский  край',\
                                                                                    '24 Краснодарский край',\
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
    with st.sidebar:
        st.components.v1.iframe(
            src="https://school-eev.bitrix24site.ru/crm_form_1rlgr/",
            height=500,
            scrolling=True
        )
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

    #
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
        
        # 
        balloon_text = json.dumps(
            f'''<div style="font-size:12px;padding:5px">
                <b>Загрузка информации...</b><br>
                📍 {adres_to_map[2][:50]}...
            </div>''',
            ensure_ascii=False
        )
        
        # 
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
            'year': adres_to_map[19]
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
                index: {i}
            }}, {{
                preset: 'islands#circleDotIcon',
                iconColor : '{icon_color}',
                draggable: false
            }})
        """
        
        # 
        if i < len(sirota) - 1:
            points_js += ","
    
    # 
    if len(sirota) > 0 and not sirota.isna().all():
        center_lat = sirota.mean()
        center_lon = dolgota.mean()
    else:
        center_lat, center_lon = 44.6, 40.1  

    # 
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
        </style>
    </head>
    <body>
        <div id="map"></div>

        <script>
            // 
            const FULL_BALLOONS = {json.dumps(FULL_BALLOONS_DATA, ensure_ascii=False)};
            
            ymaps.ready(init);
            
            function init() {{
                // Создаём карту
                var map = new ymaps.Map("map", {{
                    center: [{center_lat}, {center_lon}],
                    zoom: 10,
                    type: 'yandex#satellite'
                }});

                // 
                map.controls.add(new ymaps.control.SearchControl({{
                    options: {{
                        provider: 'yandex#search',
                        noPlacemark: false
                    }}
                }}));

                // 
                const points = [{points_js}];
                
                // 
                points.forEach(function(point, index) {{
                    point.events.add('click', function(e) {{
                        var fullData = FULL_BALLOONS[index];
                        
                        // 
                        var fullBalloon = `
                            <div style="font-size: 12px; max-width: 500px; padding: 8px; line-height: 1.4;">
                                <div style="margin-bottom: 6px;">
                                    <strong style="color: #2563eb;">📋 Полное название:</strong><br>
                                    <span>${{fullData.full_name}}</span>
                                </div>
                                <div style="margin-bottom: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                                    <strong style="color: #10b981;">⚽ Короткое название:</strong><br>
                                    <span>${{fullData.short_name}}</span>
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
                                    <div><strong>🌐 РФС ID:</strong><br><span>${{fullData.rfs_id}}</span></div>
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
                            </div>
                        `;
                        
                        // 
                        e.get('target').properties.set('balloonContent', fullBalloon);
                    }});
                    
                    map.geoObjects.add(point);
                }});

                // 
                map.events.add('click', function(e) {{
                    const coords = e.get('coords');
                    const pixelCoords = e.get('pagePixels');
                    
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
    
    # 
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



