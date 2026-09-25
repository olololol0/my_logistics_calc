import streamlit as st
import pandas as pd
import numpy as np
import math

# Настройка страницы
st.set_page_config(
    page_title="Стоимость доставки", page_icon="🧮", layout="centered"
)

# --- СТИЛИ ---
st.markdown(
    """
    <style>
        div[data-testid="stNumberInput"] label p {
            font-size: 22px !important;
            font-weight: bold !important;
            color: inherit !important;
        }
        div[data-testid="stNumberInput"] input {
            font-size: 26px !important;
            font-weight: bold !important;
            height: 55px !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #d1e7dd !important;
            border: 2px solid #a3cfbb !important;
            border-radius: 8px !important;
            padding-left: 15px !important;
        }
        div[data-testid="stNumberInput"] input:focus {
            background-color: #c1e1d2 !important;
            border-color: #0f5132 !important;
            outline: none !important;
        }
        div[data-testid="stNumberInput"] div[data-baseweb="input"],
        div[data-testid="stNumberInput"] div[data-baseweb="input"] > div {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        div[data-testid="stNumberInput"] button {
            background-color: transparent !important;
            border: none !important;
        }
        div[data-testid="stNumberInput"] {
            margin-bottom: 20px !important;
        }
        div[data-testid="stButton"] button {
            height: 65px !important;
            min-height: 65px !important;
        }
        div[data-testid="stButton"] button p {
            font-size: 24px !important;
            font-weight: bold !important;
        }
        div[data-testid="stSelectbox"] label p {
            font-size: 20px !important;
            font-weight: bold !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            font-size: 20px !important;
            font-weight: bold !important;
            min-height: 55px !important;
            background-color: #d1e7dd !important;
            border: 2px solid #a3cfbb !important;
            border-radius: 8px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= ТАРИФНЫЕ ДАННЫЕ =================
DATA = {
    50: 1690,
    100: 4730,
    200: 12787,
    300: 28611,
    400: 63000,
    500: 78960,
    600: 126084,
    700: 128000,
}

A_COEFF = 3.788485572
B_COEFF = 1.551492140

_PRICES = np.array(sorted(DATA.keys()), dtype=float)
_VOLS = np.array([DATA[p] for p in sorted(DATA.keys())], dtype=float)

MAX_PRICE = 10000
PRICE_STEP = 50


def volume_for_price(price: float) -> float:
    if price <= _PRICES[0]:
        return float(_VOLS[0])
    if price <= _PRICES[-1]:
        return float(np.interp(price, _PRICES, _VOLS))
    return A_COEFF * (price ** B_COEFF)


def price_for_volume(volume: float) -> int:
    if volume <= 0:
        return 0
    for price in range(PRICE_STEP, MAX_PRICE + PRICE_STEP, PRICE_STEP):
        if volume <= volume_for_price(price):
            return price
    return MAX_PRICE


def volume_box(l, w, h):
    return l * w * h


def volume_cylinder(d, h):
    r = d / 2.0
    return math.pi * r * r * h


# ================= ИНТЕРФЕЙС =================
st.title("Стоимость доставки📦")
st.markdown("---")

# --- Шаг 1: выбор формы ---
shape = st.selectbox(
    "Форма посылки",
    options=["📦Коробка", "🛢️Цилиндр(банка, ведро и тд)"],
    key="shape",
)

# --- Шаг 2: тип расчёта (зависит от формы) ---
if shape == "📦Коробка":
    mode_options = ["Одна посылка", "Несколько одинаковых", "Несколько разных"]
else:
    mode_options = ["Одна посылка", "Несколько одинаковых", "Несколько разных"]

# ВАЖНО: при смене shape список опций меняется —
# чтобы избежать конфликта сохранённого значения, используем отдельные ключи
mode_key = f"mode_{shape}"
if mode_key not in st.session_state:
    st.session_state[mode_key] = mode_options[0]

mode = st.selectbox(
    "Тип расчёта",
    options=mode_options,
    key=mode_key,
)

st.markdown("---")

# ================= ЛОГИКА =================

# ---------- КОРОБКА: ОДНА ----------
if shape == "📦Коробка" and mode == "Одна посылка":
    st.subheader("Габариты посылки (см)")
    l = st.number_input("Длина", min_value=0.0, value=20.0, step=1.0, key="b1_l")
    w = st.number_input("Ширина", min_value=0.0, value=15.0, step=1.0, key="b1_w")
    h = st.number_input("Высота", min_value=0.0, value=10.0, step=1.0, key="b1_h")

    if st.button("Рассчитать стоимость", type="primary", use_container_width=True, key="btn_b1"):
        if l <= 0 or w <= 0 or h <= 0:
            st.error("⚠️ Введите корректные размеры больше нуля!")
        else:
            volume = volume_box(l, w, h)
            price = price_for_volume(volume)
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            col1.metric(label="Объём посылки", value=f"{volume:.0f} см³")
            col2.metric(label="Стоимость", value=f"{price} ₽")

# ---------- КОРОБКА: НЕСКОЛЬКО ОДИНАКОВЫХ ----------
elif shape == "📦Коробка" and mode == "Несколько одинаковых":
    st.subheader("Габариты одной посылки (см) и их количество(шт)")
    l = st.number_input("Длина", min_value=0.0, value=20.0, step=1.0, key="b2_l")
    w = st.number_input("Ширина", min_value=0.0, value=15.0, step=1.0, key="b2_w")
    h = st.number_input("Высота", min_value=0.0, value=10.0, step=1.0, key="b2_h")
    qty = st.number_input("Количество", min_value=0, value=2, step=1, key="b2_q")

    if st.button("Рассчитать общую стоимость", type="primary", use_container_width=True, key="btn_b2"):
        errors = []
        if l <= 0 or w <= 0 or h <= 0:
            errors.append("Введите корректные размеры больше нуля!")
        if qty == 0:
            errors.append("Количество не может быть 0!")

        if errors:
            st.error("⚠️ " + "; ".join(e.capitalize() for e in errors))
        else:
            single_volume = volume_box(l, w, h)
            total_volume = single_volume * qty
            price = price_for_volume(total_volume)
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            col1.metric(label="Общий объём партии", value=f"{total_volume:.0f} см³")
            col2.metric(label="Финальная стоимость", value=f"{price} ₽")
            st.caption(f"Объем одной посылки: {single_volume:.0f} см³")

# ---------- КОРОБКА: НЕСКОЛЬКО РАЗНЫХ ----------
elif shape == "📦Коробка" and mode == "Несколько разных":
    st.subheader("Количество посылок(шт) и их габариты(см)")
    boxes_count = st.number_input(
        "Количество",
        min_value=0, value=2, step=1, key="b3_count"
    )
    st.markdown("---")

    total_custom_volume = 0.0
    valid_inputs = True
    table_rows = []

    if boxes_count > 0:
        for i in range(int(boxes_count)):
            st.markdown(f"**📦 Посылка №{i+1}**")
            c1, c2, c3 = st.columns(3)
            with c1:
                l_curr = st.number_input(
                    f"Длина #{i+1}", min_value=0.0, value=20.0, step=1.0,
                    key=f"b3_l_{i}"
                )
            with c2:
                w_curr = st.number_input(
                    f"Ширина #{i+1}", min_value=0.0, value=15.0, step=1.0,
                    key=f"b3_w_{i}"
                )
            with c3:
                h_curr = st.number_input(
                    f"Высота #{i+1}", min_value=0.0, value=10.0, step=1.0,
                    key=f"b3_h_{i}"
                )

            if l_curr > 0 and w_curr > 0 and h_curr > 0:
                box_v = volume_box(l_curr, w_curr, h_curr)
                total_custom_volume += box_v
                table_rows.append({
                    "Номер": f"Посылка №{i+1}",
                    "Габариты (ДхШхВ, см)": f"{l_curr:.0f} x {w_curr:.0f} x {h_curr:.0f}",
                    "Объем (см³)": int(box_v),
                })
            else:
                valid_inputs = False

    st.markdown("---")

    if st.button("Рассчитать общую стоимость", type="primary", use_container_width=True, key="btn_b3"):
        if boxes_count == 0:
            st.error("❌ Ошибка: Количество посылок не может быть равно 0!")
        elif not valid_inputs or total_custom_volume <= 0:
            st.error("⚠️ Убедитесь, что габариты всех посылок больше нуля!")
        else:
            price = price_for_volume(total_custom_volume)
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            col1.metric(label="Общий объём всех посылок", value=f"{total_custom_volume:.0f} см³")
            col2.metric(label="Итоговая стоимость", value=f"{price} ₽")

            st.write("### 📋 Таблица посылок в заказе")
            df_summary = pd.DataFrame(table_rows)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)

# ---------- ЦИЛИНДР: ОДИН ----------
elif shape == "🛢️Цилиндр(банка, ведро и тд)" and mode == "Одна посылка":
    st.subheader("Габариты посылки (см)")
    d = st.number_input("Диаметр", min_value=0.0, value=20.0, step=1.0, key="c1_d")
    h = st.number_input("Высота / длина", min_value=0.0, value=40.0, step=1.0, key="c1_h")

    if st.button("Рассчитать стоимость", type="primary", use_container_width=True, key="btn_c1"):
        if d <= 0 or h <= 0:
            st.error("⚠️ Введите корректные размеры больше нуля!")
        else:
            volume = volume_cylinder(d, h)
            price = price_for_volume(volume)
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            col1.metric(label="Объём цилиндра", value=f"{volume:.0f} см³")
            col2.metric(label="Стоимость", value=f"{price} ₽")
            st.caption(f"⌀{d:.0f} × {h:.0f} см")

# ---------- ЦИЛИНДР: НЕСКОЛЬКО ОДИНАКОВЫХ ----------
elif shape == "🛢️Цилиндр(банка, ведро и тд)" and mode == "Несколько одинаковых":
    st.subheader("Габариты одной посылки (см) и их количество (шт)")
    d = st.number_input("Диаметр", min_value=0.0, value=20.0, step=1.0, key="c2_d")
    h = st.number_input("Высота / длина", min_value=0.0, value=40.0, step=1.0, key="c2_h")
    qty = st.number_input("Количество", min_value=0, value=2, step=1, key="c2_q")

    if st.button("Рассчитать общую стоимость", type="primary", use_container_width=True, key="btn_c2"):
        errors = []
        if d <= 0 or h <= 0:
            errors.append("Введите корректные размеры больше нуля!")
        if qty == 0:
            errors.append("Количество не может быть 0!")

        if errors:
            st.error("⚠️ " + "; ".join(e.capitalize() for e in errors))
        else:
            single_volume = volume_cylinder(d, h)
            total_volume = single_volume * qty
            price = price_for_volume(total_volume)
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            col1.metric(label=f"Общий объём ({qty} шт)", value=f"{total_volume:.0f} см³")
            col2.metric(label="Финальная стоимость", value=f"{price} ₽")
            st.caption(f"Объём одной посылки: {single_volume:.0f} см³")
# ---------- ЦИЛИНДР: НЕСКОЛЬКО РАЗНЫХ ----------
elif shape == "🛢️Цилиндр(банка, ведро и тд)" and mode == "Несколько разных":
    st.subheader("Количество посылок(шт) и их габариты(см)")
    cyls_count = st.number_input(
        "Количество",
        min_value=0, value=2, step=1, key="c3_count"
    )
    st.markdown("---")

    total_custom_volume = 0.0
    valid_inputs = True
    table_rows = []

    if cyls_count > 0:
        for i in range(int(cyls_count)):
            st.markdown(f"**🛢️ Посылка №{i+1}**")
            c1, c2 = st.columns(2)
            with c1:
                d_curr = st.number_input(
                    f"Диаметр #{i+1}", min_value=0.0, value=20.0, step=1.0,
                    key=f"c3_d_{i}"
                )
            with c2:
                h_curr = st.number_input(
                    f"Высота #{i+1}", min_value=0.0, value=40.0, step=1.0,
                    key=f"c3_h_{i}"
                )

            if d_curr > 0 and h_curr > 0:
                cyl_v = volume_cylinder(d_curr, h_curr)
                total_custom_volume += cyl_v
                table_rows.append({
                    "Номер": f"Посылка №{i+1}",
                    "Габариты (⌀ × В, см)": f"⌀{d_curr:.0f} × {h_curr:.0f}",
                    "Объем (см³)": int(cyl_v),
                })
            else:
                valid_inputs = False

    st.markdown("---")

    if st.button("Рассчитать общую стоимость", type="primary", use_container_width=True, key="btn_c3"):
        if cyls_count == 0:
            st.error("❌ Ошибка: Количество не может быть равно 0!")
        elif not valid_inputs or total_custom_volume <= 0:
            st.error("⚠️ Убедитесь, что габариты больше нуля!")
        else:
            price = price_for_volume(total_custom_volume)
            st.success("🎉 Расчёт успешно завершён!")
            col1, col2 = st.columns(2)
            col1.metric(label="Общий объём партии", value=f"{total_custom_volume:.0f} см³")
            col2.metric(label="Итоговая стоимость", value=f"{price} ₽")

            st.write("### 📋 Таблица посылок в заказе")
            df_summary = pd.DataFrame(table_rows)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)