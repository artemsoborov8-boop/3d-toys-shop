import streamlit as st

# 1. ТВОЯ ВИТРИНА (Добавляй новые товары сюда)
# Просто копируй блок от { до }, чтобы добавить новую игрушку
TOYS = [
    {
        "name": "Динозавр Трицератопс",
        "price": "3500",
        "phone": "77089703265",
        "image": "https://i.ibb.co.com/Ps2KHdBw/images.jpg"
    },
    {
        "name": "Робот-шпион",
        "price": "5000",
        "phone": "77089703265",
        "image": "https://i.ibb.co.com/Ng05BMwZ/images.jpg"
    }
]

# --- ДАЛЬШЕ КОД МОЖНО НЕ ТРОГАТЬ ---

st.set_page_config(page_title="3D Toy Store", layout="wide")
st.title("🤖 Мой Магазин 3D Игрушек")
st.subheader("Все товары в наличии")

# Сетка из 3 колонок
cols = st.columns(3)

for i, toy in enumerate(TOYS):
    with cols[i % 3]:
        # Показываем фото
        st.image(toy["image"], use_container_width=True)
        
        # Инфо о товаре
        st.subheader(toy["name"])
        st.write(f"**Цена:** {toy['price']} тенге")
        
        # Кнопка WhatsApp
        wa_link = f"https://wa.me/{toy['phone']}?text=Хочу+купить:+{toy['name']}"
        st.markdown(f'''
            <a href="{wa_link}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">
                    Заказать в WhatsApp
                </button>
            </a>
        ''', unsafe_allow_html=True)
        st.write("---")
