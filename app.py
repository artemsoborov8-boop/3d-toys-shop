import streamlit as st
import pandas as pd
import time

# Настройка страницы для всех устройств
st.set_page_config(page_title="3D Toy Shop", layout="wide")

# ID твоей таблицы из ссылки
SHEET_ID = "13C_-MilOwnYR-AbjNwBzxFb34mckn9klglVhByjHEoU"
# Прямая ссылка на данные
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

def load_data():
    try:
        # Добавляем метку времени, чтобы Google не подсовывал старые данные
        url_with_cache_buster = f"{CSV_URL}&cache={time.time()}"
        return pd.read_csv(url_with_cache_buster)
    except:
        return pd.DataFrame()

st.title("🤖 Постоянный магазин 3D игрушек")

# Загружаем товары
df = load_data()

if df.empty or len(df) == 0:
    st.info("Магазин скоро откроется! Добавляем товары в таблицу...")
else:
    # Убираем пустые строки, если они есть
    df = df.dropna(subset=['name'])
    
    # Сетка товаров (3 колонки)
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            # Показываем картинку
            img = str(row['image_url']).strip()
            if "http" in img:
                st.image(img, use_container_width=True)
            else:
                st.warning("Фото в очереди на загрузку")
            
            st.subheader(row['name'])
            st.write(f"**Цена:** {row['price']} тенге")
            
            # Кнопка WhatsApp
            phone = str(row['phone']).split('.')[0].replace(" ", "").replace("+", "")
            wa_url = f"https://wa.me/{phone}?text=Здравствуйте!+Хочу+заказать:+{row['name']}"
            
            st.markdown(f'''
                <a href="{wa_url}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">
                        Купить через WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_html=True)

st.divider()
st.caption("Данные обновляются автоматически из Google Таблицы")
