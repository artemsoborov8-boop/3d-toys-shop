import streamlit as st
import json
import os

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Файл для постоянного хранения товаров
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

# Инициализация товаров
if "toys" not in st.session_state:
    st.session_state.toys = load_products()

# Твой пароль
ADMIN_PASS = "20222202" 

st.title("🤖 Магазин 3D Игрушек")

# --- СКРЫТАЯ АДМИНКА СЛЕВА ---
with st.sidebar:
    with st.expander("⚙️ Управление"):
        pwd = st.text_input("Пароль", type="password")
    
    if pwd == ADMIN_PASS:
        st.success("Режим админа")
        st.divider()
        st.header("➕ Новый товар")
        name = st.text_input("Название")
        price = st.text_input("Цена")
        img = st.text_input("Ссылка на фото (https://...)")
        
        if st.button("Опубликовать"):
            if name and price and img.startswith("http"):
                st.session_state.toys.append({"name": name, "price": price, "image": img})
                save_products(st.session_state.toys)
                st.rerun()
            else:
                st.error("Заполни все поля и проверь https://")

# --- ВИТРИНА ДЛЯ ВСЕХ ---
if not st.session_state.toys:
    # Вместо инструкции для админа пишем вежливое приветствие
    st.write("### Добро пожаловать! Скоро здесь появятся новинки. 🚀")
else:
    cols = st.columns(3)
    for i, toy in enumerate(st.session_state.toys):
        with cols[i % 3]:
            try:
                st.image(toy["image"], use_container_width=True)
            except:
                st.warning("Фото временно недоступно")
            
            st.subheader(toy["name"])
            st.write(f"**Цена:** {toy['price']} тг")
            
            if pwd == ADMIN_PASS:
                if st.button(f"🗑 Удалить {toy['name']}", key=f"del_{i}"):
                    st.session_state.toys.pop(i)
                    save_products(st.session_state.toys)
                    st.rerun()
            else:
                # Кнопка WhatsApp для заказа
                # Замени номер на свой в формате 7XXXXXXXXXX
                my_phone = "77089703265" 
                message = f"Здравствуйте! Хочу заказать: {toy['name']} за {toy['price']} тг"
                wa_url = f"https://wa.me/{my_phone}?text={message.replace(' ', '+')}"
                
                st.markdown(f'''
                    <a href="{wa_url}" target="_blank">
                        <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">
                            Написать в WhatsApp
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
            st.write("---")
