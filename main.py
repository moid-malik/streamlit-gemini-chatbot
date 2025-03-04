import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_util import lb, page_header, translate_role
from gemini_util import load_gemini_pro, img_caption, llm_response

# Page Configuration
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Sidebar Menu
with st.sidebar:
    st.markdown("### 🚀 Navigate")
    selected = option_menu(
        menu_title="AI Tools",
        options=["Chatbot", "Image Captioning", "Q&A"],
        icons=["chat-dots-fill", "image-fill", "question-circle-fill"],
        default_index=0,
        styles={
            "container": {"background-color": "#111"},
            "icon": {"color": "#fff", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#387478", "color": "white"},
        }
    )

# Chatbot Page
if selected == "Chatbot":
    model = load_gemini_pro("gemini-1.5-pro")
    st.session_state.setdefault("chat_session", model.start_chat(history=[]))

    page_header("🤖 Gemini Chatbot", color="#fff")
    st.markdown("Engage with Gemini AI for interactive conversations.")

    for msg in st.session_state.chat_session.history:
        with st.chat_message(translate_role(msg.role)):
            st.markdown(msg.parts[0].text)

    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        with st.spinner("Thinking..."):
            response = st.session_state.chat_session.send_message(user_input).text
        with st.chat_message("assistant"):
            st.markdown(response)

# Image Captioning Page
elif selected == "Image Captioning":
    page_header("📸 AI Image Captioning", color="#fff")
    st.markdown("Upload an image to generate an AI-powered caption.")

    image_upload = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if image_upload and st.button("Generate Caption", use_container_width=True):
        image = Image.open(image_upload)
        with st.spinner("Analyzing image..."):
            caption = img_caption(image)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        with col2:
            st.subheader("📌 Generated Caption")
            st.info(caption)

# Q&A Page
elif selected == "Q&A":
    page_header("❓ Ask Me Anything", color="#fff")
    st.markdown("Enter any question, and Gemini AI will provide an answer.")

    input_question = st.text_area("Enter your question:", placeholder="e.g. What is the speed of light?")
    
    if st.button("Ask Gemini", use_container_width=True):
        with st.spinner("Thinking..."):
            answer = llm_response(input_question)

        st.subheader("📢 AI Response")
        st.success(answer)
