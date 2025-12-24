import streamlit as st
import pandas as pd
import json
import requests

# Настройка страницы
st.set_page_config(layout="wide", page_title="Реестр ОФИ")

# CSS для синего фона
st.markdown("""
<style>
    .stApp {
        background-color: #1E3A8A;
    }
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
            /* Стили для модального окна подтверждения */
            .confirmation-modal {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 2000;
                animation: fadeIn 0.3s ease;
            }}
            .modal-content {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                max-width: 400px;
                width: 90%;
                text-align: center;
            }}
            .modal-title {{
                color: #EF4444;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }}
            .modal-message {{
                margin-bottom: 20px;
                color: #333;
                line-height: 1.5;
            }}
            .modal-buttons {{
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            .modal-button {{
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }}
            .cancel-button {{
                background: #E5E7EB;
                color: #333;
            }}
            .delete-button {{
                background: #EF4444;
                color: white;
            }}
            .cancel-button:hover {{
                background: #D1D5DB;
            }}
            .delete-button:hover {{
                background: #DC2626;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
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
            .notification {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 25px;
                border-radius: 8px;
                z-index: 1001;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
                animation: slideIn 0.3s ease;
                font-size: 14px;
                display: flex;
                align-items: center;
                gap: 10px;
                min-width: 300px;
            }}
            .success-notification {{
                background: #10B981;
                color: white;
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
            }}
            .error-notification {{
                background: #EF4444;
                color: white;
                box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
            }}
            .info-notification {{
                background: #3B82F6;
                color: white;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            }}
            @keyframes slideIn {{
                from {{ transform: translateX(100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            @keyframes fadeOut {{
                from {{ opacity: 1; }}
                to {{ opacity: 0; }}
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        
        <!-- Модальное окно подтверждения -->
        <div id="confirmation-modal" class="confirmation-modal" style="display: none;">
            <div class="modal-content">
                <div class="modal-title">⚠️ Подтверждение удаления</div>
                <div class="modal-message" id="modal-message">
                    Вы уверены, что хотите удалить этот объект?
                </div>
                <div class="modal-buttons">
                    <button id="modal-cancel" class="modal-button cancel-button">Отмена</button>
                    <button id="modal-delete" class="modal-button delete-button">Удалить</button>
                </div>
            </div>
        </div>
        
        <!-- Уведомления -->
        <div id="success-notification" class="notification success-notification" style="display: none;"></div>
        <div id="error-notification" class="notification error-notification" style="display: none;"></div>
        <div id="info-notification" class="notification info-notification" style="display: none;"></div>

        <script>
            // Передаём полные данные в JavaScript
            const FULL_BALLOONS = {json.dumps(FULL_BALLOONS_DATA, ensure_ascii=False)};
            const REGION_CODE = "{st_select_region[:2]}";
            const REGION_NAME = "{st_select_region}";
            
            // Глобальные переменные
            let map;
            let currentPlacemark = null;
            let pendingDeleteIndex = null;
            let pendingDeleteIdEgora = null;
            
            // Показать модальное окно подтверждения
            function showConfirmationModal(index, idEgora, fullData) {{
                pendingDeleteIndex = index;
                pendingDeleteIdEgora = idEgora;
                
                // Обновляем текст сообщения
                const message = `Вы уверены, что хотите удалить объект?<br><br>
                                <strong>${{fullData.full_name}}</strong><br>
                                ${{fullData.address}}<br><br>
                                После подтверждения объект будет окрашен в красный цвет и отправлена заявка на удаление.`;
                document.getElementById('modal-message').innerHTML = message;
                
                // Показываем модальное окно
                document.getElementById('confirmation-modal').style.display = 'flex';
                
                // Закрытие по клику на отмену
                document.getElementById('modal-cancel').onclick = function() {{
                    hideConfirmationModal();
                }};
                
                // Обработка подтверждения удаления
                document.getElementById('modal-delete').onclick = async function() {{
                    hideConfirmationModal();
                    await executeDelete(pendingDeleteIndex, pendingDeleteIdEgora, fullData);
                }};
                
                // Закрытие по клику вне модального окна
                document.getElementById('confirmation-modal').onclick = function(e) {{
                    if (e.target.id === 'confirmation-modal') {{
                        hideConfirmationModal();
                    }}
                }};
            }}
            
            // Скрыть модальное окно
            function hideConfirmationModal() {{
                document.getElementById('confirmation-modal').style.display = 'none';
                pendingDeleteIndex = null;
                pendingDeleteIdEgora = null;
            }}
            
            // Показать уведомление
            function showNotification(message, type = 'info') {{
                const notification = document.getElementById(type + '-notification');
                if (!notification) return;
                
                notification.innerHTML = message;
                notification.style.display = 'flex';
                
                // Автоматическое скрытие через 5 секунд
                setTimeout(() => {{
                    notification.style.display = 'none';
                }}, 5000);
            }}
            
            // Обработка клика на кнопку Удалить
            async function handleDeleteClick(index, id_egora, fullData) {{
                showConfirmationModal(index, id_egora, fullData);
            }}
            
            // Функция для отправки в CRM Bitrix24 через CORS-прокси (РАБОТАЕТ НА ЛЮБОМ КОМПЬЮТЕРЕ)
            async function sendDeleteToBitrix24(regionCode, idEgora, fullData) {{
                try {{
                    console.log('Начинаем отправку в Bitrix24 через CORS-прокси...');
                    
                    // Используем CORS-прокси для обхода ограничений браузера
                    const restUrl = 'https://corsproxy.io/?' + encodeURIComponent('https://drlk.rfs.ru/rest/205/kabk0xvmvkd29y00/crm.lead.add');
                    
                    // Данные для создания лида
                    const leadData = {{
                        fields: {{
                            "TITLE": `Заявка на удаление объекта: ${{fullData.full_name}}`,
                            "NAME": regionCode,
                            "SECOND_NAME": idEgora,
                            "PHONE": idEgora,
                            "COMMENTS": `Регион: ${{regionCode}} (${{REGION_NAME}})
    ID объекта: ${{idEgora}}
    Объект: ${{fullData.full_name}}
    Адрес: ${{fullData.address}}
    Контакт: ${{fullData.contact}}
    Тип: ${{fullData.type}}
    Размер: ${{fullData.size}}
    Покрытие: ${{fullData.coverage}}
    Мест: ${{fullData.capacity}}
    Дренаж: ${{fullData.drainage}}
    Подогрев: ${{fullData.heating}}
    Табло: ${{fullData.scoreboard}}
    Раздевалки: ${{fullData.dressing}}
    Год: ${{fullData.year}}
                                            
    Заявка создана автоматически из карты объектов.`,
                            "SOURCE_ID": "WEB",
                            "SOURCE_DESCRIPTION": "Карта спортивных объектов РФС"
                        }}
                    }};
                    
                    // Отправляем POST-запрос к REST API через CORS-прокси
                    const response = await fetch(restUrl, {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify(leadData)
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP ошибка! Статус: ${{response.status}}`);
                    }}
                    
                    const result = await response.json();
                    
                    if (result.error) {{
                        throw new Error(`Ошибка Bitrix24: ${{result.error_description}}`);
                    }}
                    
                    console.log('Заявка успешно отправлена в Bitrix24 через прокси:', result);
                    return true;
                    
                }} catch (error) {{
                    console.error('Ошибка отправки в Bitrix24:', error);
                    
                    // Альтернативный метод: используем другой CORS-прокси
                    try {{
                        console.log('Пробуем альтернативный CORS-прокси...');
                        const altRestUrl = 'https://api.allorigins.win/raw?url=' + encodeURIComponent('https://drlk.rfs.ru/rest/205/kabk0xvmvkd29y00/crm.lead.add');
                        
                        const altLeadData = {{
                            fields: {{
                                "TITLE": `Заявка на удаление: ${{fullData.full_name}}`,
                                "NAME": regionCode,
                                "COMMENTS": `Регион: ${{regionCode}} (${{REGION_NAME}})
    Объект: ${{fullData.full_name}}
    Адрес: ${{fullData.address}}`
                            }}
                        }};
                        
                        const altResponse = await fetch(altRestUrl, {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(altLeadData)
                        }});
                        
                        if (altResponse.ok) {{
                            console.log('Альтернативный метод сработал');
                            return true;
                        }}
                    }} catch (altError) {{
                        console.error('Альтернативный метод тоже не сработал:', altError);
                    }}
                    
                    return false;
                }}
            }}
            
            // Функция для сохранения в localStorage
            function saveToLocalStorage(regionCode, idEgora, fullData) {{
                try {{
                    const deleteRequests = JSON.parse(localStorage.getItem('delete_requests') || '[]');
                    deleteRequests.push({{
                        timestamp: new Date().toISOString(),
                        region_code: regionCode,
                        id_egora: idEgora,
                        object_name: fullData.full_name,
                        object_address: fullData.address,
                        status: 'crm_lead_created'
                    }});
                    localStorage.setItem('delete_requests', JSON.stringify(deleteRequests));
                }} catch (e) {{
                    console.log('Не удалось сохранить в localStorage:', e);
                }}
            }}
            
            // Выполнить удаление после подтверждения
            async function executeDelete(index, id_egora, fullData) {{
                if (!currentPlacemark) return;
                
                // 1. Делаем точку красной
                currentPlacemark.options.set('iconColor', '#EF4444');
                
                // 2. Закрываем баллун
                currentPlacemark.balloon.close();
                
                // 3. Показываем уведомление об отправке
                showNotification('⏳ Отправка заявки в Bitrix24...', 'info');
                
                // 4. Отправляем заявку в Bitrix24
                const success = await sendDeleteToBitrix24(REGION_CODE, id_egora, fullData);
                
                if (success) {{
                    // 5. Сохраняем в localStorage
                    saveToLocalStorage(REGION_CODE, id_egora, fullData);
                    // 6. Показываем уведомление об успехе
                    showNotification('✅ Заявка на удаление отправлена в Bitrix24!', 'success');
                }} else {{
                    // 7. Если отправка не удалась, можно изменить цвет на другой (например, серый)
                    currentPlacemark.options.set('iconColor', '#94A3B8');
                    showNotification('❌ Ошибка при отправке заявки. Объект отмечен.', 'error');
                }}
            }}
            
            // Функция для обработки клика на кнопку Подтвердить
            function handleConfirmClick(index) {{
                // Открываем форму в новой вкладке
                window.open("https://school-eev.bitrix24site.ru/crm_form_1rlgr/", "_blank");
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
                        currentPlacemark = e.get('target');
                        
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
                                
                                <div style="margin-top: 12px; padding-top: 12px; border-top: 2px solid #e5e7eb;">
                                    <div style="display: flex; gap: 20px; justify-content: center;">
                                        <button onclick="handleConfirmClick(${{index}})" style="cursor: pointer; background: none; border: 1px solid #10b981; padding: 5px 15px; border-radius: 4px; color: #10b981; font-weight: bold;">
                                            ✅ Изменить данные
                                        </button>
                                        <button onclick="handleDeleteClick(${{index}}, '${{id_egora}}', FULL_BALLOONS[${{index}}])" style="cursor: pointer; background: none; border: 1px solid #ef4444; padding: 5px 15px; border-radius: 4px; color: #ef4444; font-weight: bold;">
                                            ❌ Удалить поле
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
