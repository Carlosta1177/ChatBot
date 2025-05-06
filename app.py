import streamlit as st
import ollama
import logging

logging.basicConfig(level=logging.INFO)

st.title("Chatbot Personalizable")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("Prompt inicial (cómo debe actuar el chatbot):")
default_prompt = "Actúa como un asistente amigable y profesional."
prompt = st.text_area("Prompt", value=default_prompt, height=100)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Escribe tu mensaje aquí...")

def generate_response(user_message, prompt):
    try:
        logging.info(f"Enviando mensaje a Ollama: {user_message}")
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
        )
        logging.info(f"Respuesta recibida: {response['message']['content']}")
        return response['message']['content']
    except Exception as e:
        logging.error(f"Error en Ollama: {str(e)}")
        return f"Error: No se pudo conectar con Ollama. Asegúrate de que Ollama esté corriendo y el modelo esté descargado. Detalles: {str(e)}"

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)
    
    with st.chat_message("assistant"):
        response = generate_response(user_message, prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
