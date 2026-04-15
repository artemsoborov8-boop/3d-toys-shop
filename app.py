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

# Настройки доступа
ADMIN_PASS = "20222022" 
MY_PHONE = "77089703265"

st.title("🤖 Магазин 3D Игрушек")

# --- АДМИНКА В БОКОВОЙ ПАНЕЛИ ---
with st.sidebar:
    with st.expander("⚙️ Управление"):
        pwd = st.text_input("Пароль", type="password")
    
    if pwd == ADMIN_PASS:
        st.success("Режим админа")
        st.divider()
        st.header("➕ Новый товар")
        name = st.text_input("Название")
        price = st.text_input("Цена (тг)")
        img = st.text_input("Ссылка на фото (https://...)")
        
        if st.button("Опубликовать"):
            if name and price and img.startswith("http"):
                st.session_state.toys.append({"name": name, "price": price, "image": img})
                save_products(st.session_state.toys)
                st.rerun()
            else:
                st.error("Заполни все поля и проверь ссылку!")

# --- ВИТРИНА ---
if not st.session_state.toys:
    st.write("### Добро пожаловать! Скоро здесь появятся новинки. 🚀")
else:
    cols = st.columns(3)
    for i, toy in enumerate(st.session_state.toys):
        with cols[i % 3]:
            try:
                st.image(toy["image"], use_container_width=True)
            except:
                st.warning("Фото недоступно")
            
            st.subheader(toy["name"])
            st.write(f"**Цена:** {toy['price']} тг")
            
            if pwd == ADMIN_PASS:
                if st.button(f"🗑 Удалить", key=f"del_{i}"):
                    st.session_state.toys.pop(i)
                    save_products(st.session_state.toys)
                    st.rerun()
            else:
                # ФОРМА ЗАКАЗА
                with st.popover("🛍 Купить"):
                    st.write("Оформление заказа")
                    client_num = st.text_input("Введите ваш номер", placeholder="8707...", key=f"cl_{i}")
                    
                    if st.button("Заказать в WhatsApp", key=f"btn_{i}"):
                        if client_num:
                            text = f"Здравствуйте! Хочу купить: {toy['name']}. Мой номер: {client_num}"
                            wa_url = f"https://wa.me/{MY_PHONE}?text={text.replace(' ', '+')}"
                            st.markdown(f"**[ПОДТВЕРДИТЬ И ОТПРАВИТЬ СЕЙЧАС]({wa_url})**")
                        else:
                            st.error("Нужен номер телефона!")
            st.write("---")
