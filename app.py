import streamlit as st

st.set_page_config(page_title="3D Shop Manager", layout="wide")

# 1. Инициализация списка товаров (хранится, пока работает приложение)
if "toys" not in st.session_state:
    st.session_state.toys = [
        {
            "name": "Динозавр Трицератопс",
            "price": "3500",
            "image": "https://i.ibb.co.com/Ps2KHdBw/images.jpg"
        }
    ]

# 2. Настройки админки
ADMIN_PASSWORD = "202201" # СМЕНИ ПАРОЛЬ ТУТ

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.title("🤖 Мой 3D Магазин")

# --- ФОРМА ДОБАВЛЕНИЯ (ТОЛЬКО ДЛЯ АДМИНА) ---
if st.session_state.admin_mode:
    st.sidebar.header("➕ Добавить новый товар")
    new_name = st.sidebar.text_input("Название")
    new_price = st.sidebar.text_input("Цена (тенге)")
    new_img = st.sidebar.text_input("Ссылка на фото (URL)")
    
    if st.sidebar.button("Опубликовать товар"):
        if new_name and new_price and new_img:
            new_item = {"name": new_name, "price": new_price, "image": new_img}
            st.session_state.toys.append(new_item)
            st.success("Товар добавлен!")
            st.rerun()
        else:
            st.error("Заполни все поля!")
    
    if st.sidebar.button("Выйти из режима админа"):
        st.session_state.admin_mode = False
        st.rerun()

# --- ВИТРИНА ---
if not st.session_state.toys:
    st.info("В магазине пока нет товаров.")
else:
    cols = st.columns(3)
    for i, toy in enumerate(st.session_state.toys):
        with cols[i % 3]:
            st.image(toy["image"], use_container_width=True)
            st.subheader(toy["name"])
            st.write(f"**Цена:** {toy['price']} тенге")
            
            # Если админ — кнопка удаления
            if st.session_state.admin_mode:
                if st.button(f"❌ Удалить {toy['name']}", key=f"del_{i}"):
                    st.session_state.toys.pop(i)
                    st.rerun()
            else:
                # Если покупатель — кнопка заказа
                wa_link = f"https://wa.me/77089703265?text=Хочу+купить:+{toy['name']}"
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:8px; width:100%; cursor:pointer;">Заказать</button></a>', unsafe_allow_html=True)

# --- СЕКРЕТНЫЙ ВХОД ВНИЗУ ---
st.divider()
if not st.session_state.admin_mode:
    with st.expander("🔐 Вход для владельца"):
        pwd = st.text_input("Введите пароль", type="password")
        if st.button("Войти"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_mode = True
                st.rerun()
            else:
                st.error("Неверный пароль")
