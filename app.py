import streamlit as st
import json
import os

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Файл для хранения данных
DATA_FILE = "products.json"

def load_products():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

if "toys" not in st.session_state:
    st.session_state.toys = load_products()

# Твой пароль и твой номер телефона
ADMIN_PASS = "20222022" 
MY_PHONE = "87089703265" # Твой номер для получения заказов

st.title("🤖 Магазин 3D Игрушек")

# --- АДМИНКА ---
with st.sidebar:
    with st.expander("⚙️ Управление"):
        pwd = st.text_input("Пароль", type="password")
    
    if pwd == ADMIN_PASS:
        st.success("Режим админа")
        st.divider()
        name = st.text_input("Название игрушки")
        price = st.text_input("Цена (тг)")
        img = st.text_input("Ссылка на фото (https://...)")
        
        if st.button("Опубликовать"):
            if name and price and img.startswith("http"):
                st.session_state.toys.append({"name": name, "price": price, "image": img})
                save_products(st.session_state.toys)
                st.rerun()
            else:
                st.error("Заполни все поля правильно!")

# --- ВИТРИНА ---
if not st.session_state.toys:
    st.write("### Добро пожаловать! Скоро здесь появ
