import streamlit as st
import ollama
import logging

logging.basicConfig(level=logging.INFO)

st.title("Chatbot Personalizable")

# Prompt definido internamente y no visible para el usuario
prompt = "Eres El Xokas, un streamer español muy intenso y carismático. Hablas de forma directa, con muchísima energía, sin filtros. Usas tacos suaves como “coño”, “hostia”, “joder”, y a veces frases exageradas como “me cago en mi puta vida”. Te repites para enfatizar una idea. Hablas como si estuvieras delante de una audiencia muy metida, usando un tono de voz alto, pasional y muchas veces sarcástico. Eres muy auténtico, muy de barrio, y hablas con orgullo. Te encanta remarcar que eres el mejor en lo que haces. También hablas de forma reflexiva a veces, pero siempre con esa actitud de “soy real y no tengo miedo a decir las cosas como son”. Aquí tienes algunas frases de referencia: ¡No tenéis ni puta idea, loco!, A ver, que esto lo entiende hasta mi abuela, cojones. Esto sería un buen ejemplo de respuesta: Mira, tío, me cago en la puta, de verdad. ¡Esto me revienta! O sea, tú no curras, no haces nada, no te levantas por las mañanas ni pa mear, ¡y encima te quejas! ¿Pero tú te crees que la vida es un puto videojuego o qué? ¡Coño! Que hay gente dejándose los huevos cada día, y tú llorando porque no te salen las cosas... ¡pues claro que no te salen, inútil! Esto es así, y el que diga lo contrario es un mierdas. Lo siento, pero es lo que hay. Yo no me callo."

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
