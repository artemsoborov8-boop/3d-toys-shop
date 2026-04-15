import streamlit as st
import pandas as pd

st.set_page_config(page_title="3D Toy Store", layout="wide")

# Ссылка на твою таблицу
# Нажми "Поделиться" в таблице, скопируй ссылку и вставь её ниже
SHEET_URL = "https://docs.google.com/spreadsheets/d/13C_-MilOwnYR-AbjNwBzxFb34mckn9kIglVhByjHEoU/edit?usp=sharing"

def get_csv_url(url):
    # Превращаем обычную ссылку в ссылку для скачивания данных
    if "/edit" in url:
        return url.replace("/edit", "/export?format=csv")
    return url

def load_data():
    try:
        csv_url = get_csv_url(SHEET_URL)
        return pd.read_csv(csv_url)
    except Exception as e:
        return pd.DataFrame(columns=["name", "price", "phone", "image_url"])

st.title("🤖 Мой 3D Магазин")

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.header("Управление")
    st.write("Чтобы добавить или удалить товар, просто отредактируйте свою Google Таблицу.")
    st.link_button("Открыть таблицу", SHEET_URL)
    if st.button("Обновить витрину"):
        st.rerun()

# --- ВИТРИНА ---
df = load_data()

if df.empty or len(df) == 0:
    st.warning("В таблице пока нет данных или ссылка указана неверно.")
else:
    # Убираем пустые строки
    df = df.dropna(subset=['name'])
    
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            # Показываем фото
            img_url = str(row['image_url'])
            if img_url != "nan" and len(img_url) > 10:
                st.image(img_url, use_container_width=True)
            else:
                st.info("Нет фото")
                
            st.subheader(row['name'])
            st.write(f"**Цена:** {row['price']}")
            
            # Кнопка WhatsApp
            phone = str(row['phone']).replace(".0", "") # Убираем лишние точки из номера
            wa_link = f"https://wa.me/{phone}?text=Здравствуйте!+Хочу+купить+{row['name']}"
            
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">
                        Заказать в WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_html=True)
