import streamlit as st
import urllib.parse

# Настройки страницы
st.set_page_config(page_title="3D Toy Store", layout="wide")

# Инициализация "базы данных" в памяти (после перезагрузки данные очистятся)
# Для сохранения надолго обычно используют файлы или БД
if 'toys' not in st.session_state:
    st.session_state.toys = []

# --- БОКОВАЯ ПАНЕЛЬ (АДМИНКА) ---
st.sidebar.header("Вход для владельца")
admin_code = st.sidebar.text_input("Введите код доступа", type="password")

if admin_code == "9876":
    st.sidebar.success("Доступ разрешен")
    st.sidebar.subheader("Добавить новую игрушку")
    
    with st.sidebar.form("add_toy_form"):
        name = st.form_submit_button("Добавить")
        toy_name = st.text_input("Название игрушки")
        toy_price = st.number_input("Цена (тг/руб)", min_value=0)
        toy_photo = st.file_uploader("Загрузите фото", type=["jpg", "png", "jpeg"])
        whatsapp_phone = st.text_input("Ваш номер WhatsApp (напр. 77071234567)")
        
        submit = st.form_submit_button("Опубликовать")
        
        if submit and toy_photo and toy_name:
            new_toy = {
                "name": toy_name,
                "price": toy_price,
                "image": toy_photo,
                "phone": whatsapp_phone
            }
            st.session_state.toys.append(new_toy)
            st.sidebar.info(f"Игрушка '{toy_name}' добавлена!")

# --- ОСНОВНОЙ ИНТЕРФЕЙС (ВИТРИНА) ---
st.title("🤖 Магазин 3D игрушек")
st.write("Выбирайте модель и пишите мне напрямую в WhatsApp!")

if not st.session_state.toys:
    st.warning("На данный момент товаров нет. Владелец скоро их добавит!")
else:
    # Отображение товаров сеткой
    cols = st.columns(3)
    for idx, toy in enumerate(st.session_state.toys):
        with cols[idx % 3]:
            st.image(toy["image"], use_container_width=True)
            st.subheader(toy["name"])
            st.write(f"**Цена:** {toy['price']} тенге")
            
            # Генерация ссылки для WhatsApp
            message = urllib.parse.quote(f"Здравствуйте! Хочу купить 3D игрушку: {toy['name']} за {toy['price']}")
            wa_link = f"https://wa.me/{toy['phone']}?text={message}"
            
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="
                        background-color: #25D366;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        width: 100%;">
                        Заказать через WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_ Hicks=True)