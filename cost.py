import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Калькулятор стоимости посылки", page_icon="🧮", layout="centered"
)

# --- НОВЫЙ БЛОК СТИЛЕЙ С ГАРАНТИРОВАННЫМ ОКРАШИВАНИЕМ ПОЛЕЙ ---
st.markdown(
    """
    <style>
        /* 1. Крупный текст заголовков */
        div[data-testid="stNumberInput"] label p {
            font-size: 22px !important;
            font-weight: bold !important;
            color: inherit !important;
        }
        
        /* 2. Окрашивание полей ввода */
        div[data-testid="stNumberInput"] input {
            font-size: 26px !important;
            font-weight: bold !important;
            height: 55px !important;
            
            /* Настройка цвета и рамки */
            background-color: #d1e7dd !important; /* Наш светло-зеленый фон */
            border: 2px solid #a3cfbb !important;  /* Зеленоватая рамка */
            border-radius: 8px !important;
            padding-left: 15px !important;
        }
        
        /* 3. Изменение цвета при клике мышкой (фокус) */
        div[data-testid="stNumberInput"] input:focus {
            background-color: #c1e1d2 !important; /* Чуть темнее при клике */
            border-color: #0f5132 !important;     /* Темная рамка при клике */
            outline: none !important;
        }

        /* 4. Делаем контейнеры вокруг инпута прозрачными, чтобы не было серых рамок */
        div[data-testid="stNumberInput"] div[data-baseweb="input"],
        div[data-testid="stNumberInput"] div[data-baseweb="input"] > div {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }


        /* Убираем серый фон у кнопок "+" и "-" внутри инпута */
        div[data-testid="stNumberInput"] button {
            background-color: transparent !important;
            border: none !important;
        }
        
        /* Отступ между блоками */
        div[data-testid="stNumberInput"] {
            margin-bottom: 20px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# ----------------------------------------

# Новые тарифные данные и коэффициенты
DATA = {50: 1690, 100: 4730, 200: 12787, 300: 28611}
A_COEFF = 3.788485572
B_COEFF = 1.551492140


def volume_for_price(price):
    if price in DATA:
        return DATA[price]
    return A_COEFF * (price**B_COEFF)


def price_for_volume(volume):
    for price in range(50, 10001, 50):
        if volume <= volume_for_price(price):
            return price
    return 10000


# Оформление интерфейса сайта
st.title("Калькулятор стоимости")
st.write("Рассчитайте объем и стоимость одной посылки или партии.")

st.markdown("---")

# Создаем красивую карточку с полями ввода
with st.container():
    st.subheader("Габариты посылки (см)")

    # Поля ввода для размеров одной коробки
    length = st.number_input(
        "Длина", min_value=0.0, value=20.0, step=1.0
    )
    width = st.number_input(
        "Ширина", min_value=0.0, value=15.0, step=1.0
    )
    height = st.number_input(
        "Высота", min_value=0.0, value=10.0, step=1.0
    )
    
    # Поле для ввода количества
    quantity = st.number_input(
        "Количество коробок (шт)", min_value=1, value=1, step=1
    )

st.markdown("---")

# Кнопка расчета
if st.button("Рассчитать стоимость", type="primary", use_container_width=True):
    if length > 0 and width > 0 and height > 0 and quantity > 0:
        single_volume = length * width * height
        total_volume = single_volume * quantity
        price = price_for_volume(total_volume)

        st.success("🎉 Расчёт успешно завершён!")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Общий объём партии", value=f"{total_volume:.0f} см³")
        with col2:
            st.metric(label="Финальная стоимость", value=f"{price} ₽")
            
        if quantity > 1:
            st.caption(f"Объем одной коробки: {single_volume:.0f} см³")
        else:
            st.error("⚠️ Пожалуйста, введите корректные размеры и количество больше нуля!")