import streamlit as st
import pandas as pd
import json

# Настройка страницы
st.set_page_config(layout="wide", page_title="Реестр ОФИ")

# Сайдбар
st_select_region = st.sidebar.selectbox("Выберите свой регион", ['Регионы','01','02','03'])

if st_select_region == '01':

    data = pd.read_excel(r"01.xlsx")
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
    in_reestr = data['Наличие в реестрах']
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
                        str(disciplyne.iloc[i]).replace('"', '').replace('nan','-'),
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
        
        # Создаем компактный HTML с чекбоксами
        balloon_text = json.dumps(
            f'''<div style="font-size: 12px; max-width: 500px; padding: 8px; line-height: 1.4;">
                <div style="margin-bottom: 6px;">
                    <strong style="color: #2563eb;">📋 Полное название:</strong><br>
                    <span>{adres_to_map[0]}</span>
                </div>
                <div style="margin-bottom: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                    <strong style="color: #10b981;">⚽ Короткое название:</strong><br>
                    <span>{adres_to_map[1]}</span>
                </div>
                <div style="margin-bottom: 6px; padding-top: 6px; border-top: 1px solid #e5e7eb;">
                    <strong>📍 Адрес:</strong><br>
                    <span>{adres_to_map[2]}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                    <div><strong>📞 Контакт:</strong><br><span>{adres_to_map[3]}</span></div>
                    <div><strong>👤 Собственник(ОГРН):</strong><br><span>{adres_to_map[4]}</span></div>
                    <div><strong>🏢 Управляющая(ОГРН):</strong><br><span>{adres_to_map[5]}</span></div>
                    <div><strong>👥 Пользователь(ОГРН):</strong><br><span>{adres_to_map[6]}</span></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                    <div><strong>РФС ID:</strong><br><span>{adres_to_map[7]}</span></div>
                    <div><strong>Тип:</strong><br><span>{adres_to_map[8]}</span></div>
                    <div><strong>Дисциплина:</strong><br><span>{adres_to_map[9]}</span></div>
                    <div><strong>Размер:</strong><br><span>{adres_to_map[10]}×{adres_to_map[11]}</span></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                    <div><strong>Покрытие:</strong><br><span>{adres_to_map[13]}</span></div>
                    <div><strong>Мест:</strong><br><span>{adres_to_map[14]}</span></div>
                    <div><strong>Дренаж:</strong><br><span>{adres_to_map[15]}</span></div>
                    <div><strong>Подогрев:</strong><br><span>{adres_to_map[16]}</span></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                    <div><strong>Табло:</strong><br><span>{adres_to_map[17]}</span></div>
                    <div><strong>Раздевалки:</strong><br><span>{adres_to_map[18]}</span></div>
                    <div><strong>Год:</strong><br><span>{adres_to_map[19]}</span></div>
                </div>
                <div style="margin-top: 12px; padding-top: 12px; border-top: 2px solid #e5e7eb;">
                    <div style="display: flex; gap: 20px; justify-content: center;">
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
                            <input type="checkbox" class="feedback-checkbox" data-type="confirm" 
                                   onclick="handleCheckboxClick(this, 'confirm')" style="cursor: pointer;">
                            <span style="color: #10b981; font-weight: bold;">✅ Подтвердить</span>
                        </label>
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
                            <input type="checkbox" class="feedback-checkbox" data-type="reject" 
                                   onclick="handleCheckboxClick(this, 'reject')" style="cursor: pointer;">
                            <span style="color: #ef4444; font-weight: bold;">❌ Опровергнуть</span>
                        </label>
                    </div>
                </div>
            </div>''',
            ensure_ascii=False
        )
        if in_reestr[i] == 1:
            icon_color = '#3B82F6'  # Синий
        elif in_reestr[i] == 2:
            icon_color = '#F59E0B'  # Желтый
        else:
            icon_color = '#10B981'  # Зеленый
        points_js += f"""
            new ymaps.Placemark([{sirota[i]}, {dolgota[i]}], {{
                balloonContent: {balloon_text},
                balloonMaxWidth: 520,
                balloonMinWidth: 450
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
            ymaps.ready(init);

            function init() {{
                // Центрируем на средних координатах
                const map = new ymaps.Map("map", {{
                    center: [{center_lat}, {center_lon}],
                    zoom: 10,
                    type: 'yandex#satellite'
                }});

                // Добавляем поиск на карту
                map.controls.add(new ymaps.control.SearchControl({{
                    options: {{
                        provider: 'yandex#search',
                        noPlacemark: false
                    }}
                }}));

                // ДОБАВЛЯЕМ ТОЧКИ АДРЕСОВ
                const points = [{points_js}];
                console.log("Всего точек:", points.length);
                points.forEach(point => map.geoObjects.add(point));

                // Обработка клика на карте
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
                
                // Функция для чекбоксов в balloon
                function handleCheckboxClick(clickedCheckbox, type) {{
                    // Находим все чекбоксы в текущем balloon
                    const balloon = clickedCheckbox.closest('.ymaps-balloon');
                    const checkboxes = balloon.querySelectorAll('.feedback-checkbox');
                    
                    // Если нажат чекбокс
                    if (clickedCheckbox.checked) {{
                        // Проходим по всем чекбоксам
                        checkboxes.forEach(checkbox => {{
                            if (checkbox !== clickedCheckbox) {{
                                // Снимаем все другие чекбоксы
                                checkbox.checked = false;
                            }}
                        }});
                        
                        // Здесь можно добавить логику отправки выбора
                        console.log('Выбрано:', type);
                    }} else {{
                        // Если чекбокс снят, ничего не делаем
                        console.log('Снято:', type);
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    # Показываем карту
    st.components.v1.html(map_html, height=800)
    
    # Показываем информацию о точках
    valid_points = sum(1 for i in range(len(sirota)) 
                      if pd.notna(sirota[i]) and pd.notna(dolgota[i]))