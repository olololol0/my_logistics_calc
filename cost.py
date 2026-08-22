import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(
    page_title="Калькулятор стоимости посылки", page_icon="🧮", layout="centered"
)

# --- БЛОК СТИЛЕЙ С ЧЕРНЫМ ШРИФТОМ И КРУПНОЙ КНОПКОЙ ---
st.markdown(
    """
    <style>
        /* 1. Крупный текст заголовков у инпутов */
        div[data-testid="stNumberInput"] label p {
            font-size: 22px !important;
            font-weight: bold !important;
            color: inherit !important;
        }
        
        /* 2. Окрашивание полей ввода и ЧЕРНЫЙ ЦВЕТ ЦИФР */
        div[data-testid="stNumberInput"] input {
            font-size: 26px !important;
            font-weight: bold !important;
            height: 55px !important;
            color: #000000 !important;          
            -webkit-text-fill-color: #000000 !important; 
            
            /* Настройка цвета и рамки */
            background-color: #d1e7dd !important; 
            border: 2px solid #a3cfbb !important;  
            border-radius: 8px !important;
            padding-left: 15px !important;
        }
        
        /* 3. Изменение цвета при клике мышкой (фокус) */
        div[data-testid="stNumberInput"] input:focus {
            background-color: #c1e1d2 !important; 
            border-color: #0f5132 !important;     
            outline: none !important;
        }

        /* 4. Делаем контейнеры вокруг инпута прозрачными */
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
        
        /* Отступ между blocks */
        div[data-testid="stNumberInput"] {
            margin-bottom: 20px !important;
        }

        /* 5. СТИЛИ ДЛЯ КНОПКИ РАССЧЕТА */
        div[data-testid="stButton"] button {
            height: 65px !important;
            min-height: 65px !important;
        }
        
        div[data-testid="stButton"] button p {
            font-size: 24px !important;
            font-weight: bold !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# ----------------------------------------

# Тарифные данные и коэффициенты
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
st.write("Выберите подходящий вариант для расчета объема и стоимости посылок.")

st.markdown("---")

# Создаем три вкладки
tab1, tab2, tab3 = st.tabs([
    "📦 Одна посылка", 
    "📦🔢 Несколько одинаковых", 
    "🛍️ Несколько разных"
])

# ================= ВКЛАДКА 1: ОДНА ПОСЫЛКА =================
with tab1:
    st.subheader("Габариты посылки (см)")
    
    length_1 = st.number_input("Длина", min_value=0.0, value=20.0, step=1.0, key="l1")
    width_1 = st.number_input("Ширина", min_value=0.0, value=15.0, step=1.0, key="w1")
    height_1 = st.number_input("Высота", min_value=0.0, value=10.0, step=1.0, key="h1")
    
    if st.button("Рассчитать стоимость", type="primary", use_container_width=True, key="btn1"):
        if length_1 > 0 and width_1 > 0 and height_1 > 0:
            volume = length_1 * width_1 * height_1
            price = price_for_volume(volume)
            
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Объём посылки", value=f"{volume:.0f} см³")
            with col2:
                st.metric(label="Стоимость", value=f"{price} ₽")
        else:
            st.error("⚠️ Введите корректные размеры больше нуля!")

# ================= ВКЛАДКА 2: НЕСКОЛЬКО ОДИНАКОВЫХ =================
with tab2:
    st.subheader("Габариты одной коробки (cм) и их количество (шт)")
    
    length_2 = st.number_input("Длина", min_value=0.0, value=20.0, step=1.0, key="l2")
    width_2 = st.number_input("Ширина", min_value=0.0, value=15.0, step=1.0, key="w2")
    height_2 = st.number_input("Высота", min_value=0.0, value=10.0, step=1.0, key="h2")
    
    # Минимальное значение 0
    quantity_2 = st.number_input("Количество коробок", min_value=0, value=2, step=1, key="q2")
        
    if st.button("Рассчитать общую стоимость", type="primary", use_container_width=True, key="btn2"):
        if quantity_2 == 0:
            st.error("❌ Ошибка: Количество коробок не может быть равно 0!")
        elif length_2 > 0 and width_2 > 0 and height_2 > 0:
            single_volume = length_2 * width_2 * height_2
            total_volume = single_volume * quantity_2
            price = price_for_volume(total_volume)
            
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Общий объём партии", value=f"{total_volume:.0f} см³")
            with col2:
                st.metric(label="Финальная стоимость", value=f"{price} ₽")
            st.caption(f"Объем одной коробки: {single_volume:.0f} см³")
        else:
            st.error("⚠️ Введите корректные размеры груза!")

# ================= ВКЛАДКА 3: НЕСКОЛЬКО РАЗНЫХ =================
with tab3:
    st.subheader("Расчет посылок разного размера")
    
    boxes_count = st.number_input("Общее количество посылок (шт)", min_value=0, value=2, step=1, key="box_count")
    
    st.markdown("---")
    
    total_custom_volume = 0.0
    valid_inputs = True
    table_rows = [] 
    
    if boxes_count > 0:
        st.write("### Габариты каждой посылки (см):")
        for i in range(int(boxes_count)):
            st.markdown(f"**📦 Посылка №{i+1}**")
            col_l, col_w, col_h = st.columns(3)
            
            with col_l:
                l_curr = st.number_input(f"Длина #{i+1}", min_value=0.0, value=20.0, step=1.0, key=f"l_cust_{i}")
            with col_w:
                w_curr = st.number_input(f"Ширина #{i+1}", min_value=0.0, value=15.0, step=1.0, key=f"w_cust_{i}")
            with col_h:
                h_curr = st.number_input(f"Высота #{i+1}", min_value=0.0, value=10.0, step=1.0, key=f"h_cust_{i}")
                
            if l_curr > 0 and w_curr > 0 and h_curr > 0:
                box_v = l_curr * w_curr * h_curr
                total_custom_volume += box_v
                table_rows.append({
                    "Номер": f"Посылка №{i+1}",
                    "Габариты (ДхШхВ, см)": f"{l_curr:.0f} x {w_curr:.0f} x {h_curr:.0f}",
                    "Объем (см³)": int(box_v)
                })
            else:
                valid_inputs = False

    st.markdown("---")
    
    if st.button("Рассчитать общую стоимость", type="primary", use_container_width=True, key="btn3"):
        if boxes_count == 0:
            st.error("❌ Ошибка: Количество посылок не может быть равно 0!")
        elif valid_inputs and total_custom_volume > 0:
            price = price_for_volume(total_custom_volume)
            
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Общий объём всех посылок", value=f"{total_custom_volume:.0f} см³")
            with col2:
                st.metric(label="Итоговая стоимость", value=f"{price} ₽")
                
            st.write("### 📋 Таблица посылок в заказе")
            df_summary = pd.DataFrame(table_rows)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
        else:
            st.error("⚠️ Пожалуйста, убедитесь, что габариты всех посылок больше нуля!")