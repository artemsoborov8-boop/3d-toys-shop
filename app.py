import streamlit as st
import pandas as pd

st.set_page_config(page_title="3D Store", layout="wide")

# Ссылка на твою таблицу (ОБЯЗАТЕЛЬНО СДЕЛАЙ ЕЕ ДОСТУПНОЙ ДЛЯ ВСЕХ)
SHEET_URL = "https://docs.google.com/spreadsheets/d/13C_-MilOwnYR-AbjNwBzxFb34mckn9kIglVhByjHEoU/edit?usp=sharing"

def get_csv_url(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv&gid=0"
    return url

def load_data():
    try:
        # Добавляем случайный параметр, чтобы Google не выдавал старую копию файла
        import time
        csv_url = get_csv_url(SHEET_URL) + f"&cache_buster={time.time()}"
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

# Кнопка ручного обновления
if st.button("🔄 Обновить витрину"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df.empty or len(df) == 0:
    st.warning("Товары не найдены. Проверьте ссылку на таблицу и заголовки (name, price, phone, image_url)")
else:
    df = df.dropna(subset=['name']) # Убираем пустые строки
    
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            img = str(row['image_url'])
            if len(img) > 10:
                st.image(img, use_container_width=True)
            
            st.subheader(row['name'])
            st.write(f"**Цена:** {row['price']} тенге")
            
            # Чистим номер телефона от лишних знаков
            phone = str(row['phone']).split('.')[0].replace(" ", "").replace("+", "")
            wa_link = f"https://wa.me/{phone}?text=Хочу+заказать:+{row['name']}"
            
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer; font-size:16px;">
                        Заказать через WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_html=True)
