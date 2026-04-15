import streamlit as st
import pandas as pd

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Ссылка на твою таблицу (в формате CSV для простоты)
sheet_id = "13C_-MilOwnYR-AbjNwBzxFb34mckn9klglVhByjHEoU"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def load_data():
    try:
        # Читаем напрямую по ссылке
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

# --- АДМИНКА ---
with st.sidebar:
    admin_code = st.text_input("Код владельца", type="password")
    if admin_code == "9876":
        st.success("Доступ открыт")
        st.info("Чтобы добавить товар, впишите его прямо в Google Таблицу. Она сразу обновится здесь!")
        st.write(f"[Открыть таблицу для правки](https://docs.google.com/spreadsheets/d/{sheet_id}/edit)")

# --- ВИТРИНА ---
df = load_data()

if df.empty:
    st.warning("Магазин пока пуст.")
else:
    cols = st.columns(3)
    for i, row in df.iterrows():
        # Проверка на пустые строки
        if pd.isna(row['name']): continue
        
        with cols[i % 3]:
            if str(row['image_url']) != "nan" and len(str(row['image_url'])) > 5:
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
