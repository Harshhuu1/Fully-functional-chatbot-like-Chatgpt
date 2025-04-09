import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini, load_geminiimage, embedding_model
from PIL import Image

st.set_page_config(
    page_title='Your Chatbot',
    page_icon='🧠',
    layout='centered',
    initial_sidebar_state='expanded'
)

with st.sidebar:
    selected = option_menu(
        menu_title='🤖 Gemini AI',
        options=['ChatBot', 'Image Captioning', 'Embedded Text', 'Ask Me Anything?'],
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        menu_icon='robot',
        default_index=0
    )

st.title(f"You selected: {selected}")

def translate(role):
    return 'assistant' if role == 'model' else role

# 💬 ChatBot
if selected == 'ChatBot':
    st.header("🧠 Gemini Chatbot")
    model = load_gemini()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate(message.role)):
            st.markdown(message.parts[0].text)

    user_input = st.chat_input("Ask something...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        response = st.session_state.chat_session.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)

# 🖼️ Image Captioning
elif selected == 'Image Captioning':
    st.header("📸 Image Captioning")
    uploaded_image = st.file_uploader("Upload an image...", type=['jpg', 'jpeg', 'png'])
    if uploaded_image and st.button('Generate Caption'):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)
        with col1:
            resized = image.resize((800, 500))
            st.image(resized)
        with col2:
            caption = load_geminiimage("Write a short caption for this image", image)
            st.info(caption)

# 📍 Embedded Text
elif selected == 'Embedded Text':
    st.header('📨 Embedded Text')
    input_text = st.text_area("", placeholder="Enter the text to get embeddings")
    if st.button("Get Embedding"):
        response = embedding_model(input_text)
        st.json(response)

# ❓ Ask Me Anything
elif selected == "Ask Me Anything?":
    st.header("🤔 Ask Me Anything...")
    user_prompt = st.text_area("", placeholder="Ask the chatbot...")
    if st.button("Get an Answer"):
        model = load_gemini()
        response = model.generate_content(user_prompt)
        st.markdown(response.text)