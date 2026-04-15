import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="3D Store", layout="wide")

# Твоя ссылка
SHEET_ID = "13C_-MilOwnYR-AbjNwBzxFb34mckn9klglVhByjHEoU"
# Ссылка сразу на экспорт в CSV с защитой от кэша
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0&cache_buster={time.time()}"

def load_data():
    try:
        # Читаем данные напрямую, игнорируя старый кэш
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

# Кнопка для тех, у кого не обновилось само
if st.button("🔄 Обновить товары"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

# Проверяем, есть ли что-то в таблице (кроме заголовков)
if df.empty or len(df) == 0:
    st.warning("В таблице пусто. Добавьте товар под заголовками!")
else:
    # Убираем полностью пустые строки
    df = df.dropna(subset=['name'])
    
    if len(df) == 0:
        st.info("Жду, когда вы впишете первый товар в строку №2...")
    else:
        cols = st.columns(3)
        for i, row in df.iterrows():
            with cols[i % 3]:
                # Вывод фото
                img = str(row['image_url']).strip()
                if "http" in img:
                    st.image(img, use_container_width=True)
                else:
                    st.info("Фото загружается...")
                
                st.subheader(row['name'])
                st.write(f"**Цена:** {row['price']} тенге")
                
                # Номер телефона
                phone = str(row['phone']).split('.')[0].replace(" ", "")
                if not phone.startswith('7'): phone = '7' + phone
                
                wa_link = f"https://wa.me/{phone}?text=Хочу+купить:+{row['name']}"
                st.markdown(f'''
                    <a href="{wa_link}" target="_blank">
                        <button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">
                            Заказать в WhatsApp
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
