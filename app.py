import streamlit as st
import json
import os

st.set_page_config(page_title="3D Shop Admin", layout="wide")

# Файл, где будут лежать твои товары
DATA_FILE = "products.json"

# Загрузка товаров
def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение товаров
def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

if "toys" not in st.session_state:
    st.session_state.toys = load_products()

# Пароль для тебя
ADMIN_PASS = "20222022" 

st.title("🤖 Управление магазином 3D")

# --- ПАНЕЛЬ УПРАВЛЕНИЯ ---
with st.sidebar:
    st.header("🔐 Вход")
    pwd = st.text_input("Пароль", type="password")
    if pwd == ADMIN_PASS:
        st.success("Режим админа включен")
        st.divider()
        st.header("➕ Новый товар")
        name = st.text_input("Название")
        price = st.text_input("Цена")
        # ТУТ ВАЖНО: Ссылка должна начинаться с https://
        img = st.text_input("Ссылка на фото (с https://)")
        
        if st.button("Опубликовать на сайт"):
            if name and price and img.startswith("http"):
                st.session_state.toys.append({"name": name, "price": price, "image": img})
                save_products(st.session_state.toys)
                st.rerun()
            else:
                st.error("Проверь ссылку! Должна быть https://...")

# --- ВИТРИНА ---
if not st.session_state.toys:
    st.info("Пока нет товаров. Зайди в админку слева!")
else:
    cols = st.columns(3)
    for i, toy in enumerate(st.session_state.toys):
        with cols[i % 3]:
            # Проверка картинки, чтобы сайт не падал
            try:
                st.image(toy["image"], use_container_width=True)
            except:
                st.error("Ошибка картинки")
            
            st.subheader(toy["name"])
            st.write(f"Цена: {toy['price']} тг")
            
            if pwd == ADMIN_PASS:
                if st.button(f"🗑 Удалить {toy['name']}", key=f"del_{i}"):
                    st.session_state.toys.pop(i)
                    save_products(st.session_state.toys)
                    st.rerun()
            else:
                wa_url = f"https://wa.me/77089703265?text=Хочу:{toy['name']}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:8px; width:100%; cursor:pointer;">Заказать</button></a>', unsafe_allow_html=True)
