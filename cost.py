import streamlit as st

# Настройка страницы (заголовок вкладки в браузере и иконка)
st.set_page_config(
    page_title="Логистический Калькулятор", page_icon="🧮", layout="centered"
)

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
st.title("📦 Калькулятор стоимости")
st.write("Рассчитайте точный объем и стоимость вашей посылки.")

st.markdown("---")  # Разделительная линия

# Создаем красивую карточку с полями ввода
with st.container():
    st.subheader("📐 Габариты посылки")

    # Поля ввода для чисел с плавающей точкой (минимальное значение 0.0)
    length = st.number_input(
        "Длина (см)", min_value=0.0, value=20.0, step=1.0
    )
    width = st.number_input(
        "Ширина (см)", min_value=0.0, value=15.0, step=1.0
    )
    height = st.number_input(
        "Высота (см)", min_value=0.0, value=10.0, step=1.0
    )

st.markdown("---")

# Кнопка расчета
if st.button("Рассчитать стоимость", type="primary", use_container_width=True):
    if length > 0 and width > 0 and height > 0:
        # Расчет данных
        volume = length * width * height
        price = price_for_volume(volume)

        # Вывод результатов в красивых виджетах
        st.success("🎉 Расчёт успешно завершён!")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Итоговый объём", value=f"{volume:.0f} см³")
        with col2:
            st.metric(label="Финальная стоимость", value=f"{price} ₽")
    else:
        st.error("⚠️ Пожалуйста, введите корректные размеры больше нуля!")