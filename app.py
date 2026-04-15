import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Ссылка на твою таблицу
url = "https://docs.google.com/spreadsheets/d/13C_-MilOwnYR-AbjNwBzxFb34mckn9klglVhByjHEoU/edit?usp=sharing"

# Подключение
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(spreadsheet=url)
    except:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

# --- АДМИНКА ---
with st.sidebar:
    admin_code = st.text_input("Код владельца", type="password")
    if admin_code == "9876":
        st.success("Доступ открыт")
        with st.form("add_form"):
            name = st.text_input("Название игрушки")
            price = st.text_input("Цена")
            phone = st.text_input("WhatsApp (напр. 7707...)")
            img = st.text_input("Ссылка на фото")
            submit = st.form_submit_button("Выставить на витрину")
            
            if submit and name:
                data = load_data()
                new_item = pd.DataFrame([{"name": name, "price": price, "phone": phone, "image_url": img}])
                updated_data = pd.concat([data, new_item], ignore_index=True)
                conn.update(spreadsheet=url, data=updated_data)
                st.balloons()
                st.info("Товар добавлен! Обнови страницу.")

# --- ВИТРИНА ---
df = load_data()

if df.empty or len(df) == 0:
    st.warning("Магазин пока пуст. Добавьте товары через панель слева!")
else:
    # Очистка пустых строк, если они есть
    df = df.dropna(subset=['name'])
    
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            if str(row['image_url']) != "nan" and row['image_url'] != "":
                st.image(row['image_url'], use_container_width=True)
            st.subheader(row['name'])
            st.write(f"**Цена:** {row['price']}")
            
            wa_link = f"https://wa.me/{row['phone']}?text=Хочу+купить+{row['name']}"
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">
                        Заказать через WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_html=True)
