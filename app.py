import streamlit as st
import ollama
import logging

logging.basicConfig(level=logging.INFO)

st.title("Chatbot Personalizable")

# Prompt definido internamente y no visible para el usuario
prompt = "Habla como un gitano."

# Inicializar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
user_message = st.chat_input("Escribe tu mensaje aquí...")

def generate_response(user_message, prompt):
    try:
        logging.info(f"Enviando mensaje a Ollama: {user_message}")
        client = ollama.Client(host="https://cool-chefs-listen.loca.lt")
        response = client.chat(
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
        return f"Error: No se pudo conectar con Ollama. Detalles: {str(e)}"

# Lógica del chat
if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        response = generate_response(user_message, prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
