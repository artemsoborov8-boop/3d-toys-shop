import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="3D Toy Store", layout="wide")

# ТВОЯ ССЫЛКА (убедись, что она верная!)
SHEET_URL = "https://docs.google.com/spreadsheets/d/13C_-MilOwnYR-AbjNwBzxFb34mckn9klglVhByjHEoU/edit?usp=sharing"

def get_csv_url(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv&gid=0"
    return url

def load_data():
    try:
        csv_url = get_csv_url(SHEET_URL) + f"&cache_buster={time.time()}"
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

if st.button("🔄 Обновить витрину"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df.empty or len(df) == 0:
    st.warning("Товары не найдены. Проверьте заголовки в таблице: name, price, phone, image_url")
else:
    df = df.dropna(subset=['name'])
    
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            # БЕЗОПАСНЫЙ ВЫВОД КАРТИНКИ
            img = str(row['image_url'])
            if len(img) > 10 and (img.startswith("http")):
                try:
                    st.image(img, use_container_width=True)
                except:
                    st.error("Ошибка ссылки на фото")
            else:
                st.info("Фото не добавлено")
            
            st.subheader(row['name'])
            st.write(f"**Цена:** {row['price']}")
            
            phone = str(row['phone']).split('.')[0].replace(" ", "").replace("+", "")
            wa_link = f"https://wa.me/{phone}?text=Хочу+заказать:+{row['name']}"
            
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer;">
                        Заказать в WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_html=True)
