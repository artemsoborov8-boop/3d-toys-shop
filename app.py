import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Ссылка на таблицу
SHEET_URL = "https://docs.google.com/spreadsheets/d/13C_-MilOwnYR-AbjNwBzxFb34mckn9klglVhByjHEoU/edit?usp=sharing"

def get_csv_url(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv&gid=0"
    return url

def clean_url(text):
    """Находит чистую ссылку на картинку в тексте"""
    if pd.isna(text): return ""
    urls = re.findall(r'(https?://[^\s\]\[]+)', str(text))
    for u in urls:
        if any(ext in u.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            return u
    return urls[0] if urls else str(text)

def load_data():
    try:
        csv_url = get_csv_url(SHEET_URL)
        # Добавляем случайное число, чтобы данные обновлялись сразу
        import time
        csv_url += f"&cache={time.time()}"
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

if st.button("🔄 Обновить витрину"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df.empty or len(df) == 0:
    st.warning("Товары не найдены. Проверь строку №1 в таблице!")
else:
    # Удаляем пустые строки по колонке name
    df = df.dropna(subset=['name'])
    
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            # Чистим ссылку на фото
            raw_img = str(row['image_url'])
            img = clean_url(raw_img)
            
            if len(img) > 10:
                st.image(img, use_container_width=True)
            else:
                st.info("Нет фото")
                
            st.subheader(row['name'])
            st.write(f"**Цена:** {row['price']}")
            
            # Чистим номер телефона
            phone = str(row['phone']).split('.')[0].replace(" ", "").replace("+", "")
            if not phone.startswith('7'): phone = '7' + phone
            
            wa_link = f"https://wa.me/{phone}?text=Хочу+купить:+{row['name']}"
            st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer;">Заказать</button></a>', unsafe_allow_html=True)
