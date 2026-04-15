import streamlit as st
import pandas as pd
import os

# Файл, где будут храниться товары
DB_FILE = "toys_db.csv"

# Загрузка данных из файла
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["name", "price", "phone"])

# Сохранение данных в файл
def save_data(df):
    df.to_csv(DB_FILE, index=False)

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Загружаем текущие товары
toys_df = load_data()

# --- АДМИНКА ---
st.sidebar.header("Вход")
admin_code = st.sidebar.text_input("Код", type="password")

if admin_code == "9876":
    st.sidebar.success("Доступ есть")
    with st.sidebar.form("add_form"):
        name = st.text_input("Название")
        price = st.number_input("Цена", min_value=0)
        phone = st.text_input("WhatsApp (7...)")
        submit = st.form_submit_button("Опубликовать на все устройства")
        
        if submit and name:
            new_row = pd.DataFrame([{"name": name, "price": price, "phone": phone}])
            toys_df = pd.concat([toys_df, new_row], ignore_index=True)
            save_data(toys_df)
            st.sidebar.info("Сохранено! Обновите страницу.")

# --- ВИТРИНА ---
st.title("🤖 Постоянный магазин 3D игрушек")

if toys_df.empty:
    st.info("Товаров пока нет")
else:
    for index, row in toys_df.iterrows():
        with st.container():
            st.subheader(f"🧸 {row['name']}")
            st.write(f"Цена: {row['price']} тенге")
            wa_link = f"https://wa.me/{row['phone']}"
            st.markdown(f'[Заказать в WhatsApp]({wa_link})')
            st.write("---")
