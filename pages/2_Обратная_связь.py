import streamlit as st

# Синий фон и белый текст через CSS
st.markdown("""
<style>
    .stApp {
        background-color: #204171;
    }
    
    /* Весь текст белого цвета */
    .stApp, .stApp * {
        color: white !important;
    }
    
    /* Сохраняем белый цвет для ссылок */
    a {
        color: white !important;
    }
    
    a:hover {
        color: #cccccc !important;
    }
    
    /* Кнопки с белой обводкой */
    .stButton button {
        color: white !important;
        border-color: white !important;
        background-color: transparent !important;
    }
    
    .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Горизонтальная линия */
    hr {
        border-color: white !important;
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
