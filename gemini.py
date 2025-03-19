import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import nltk
from nltk.chat.util import Chat, reflections

# Assurez-vous d'avoir téléchargé les ressources nltk nécessaires


# Configurez votre clé API Gemini
genai.configure(api_key='AIzaSyCR0noLqPfW6gvVWjg4K-TzNlvMG3oomA4') # Remplacez par votre clé API Gemini

# Préparez le chatbot avec des paires de phrases (pour les réponses simples)
pairs = [
    ['bonjour', 'salut, comment puis-je vous aider?'],
    ['comment ça va ?', 'Je vais bien, merci ! Et vous ?'],
    ['au revoir', 'À bientôt !'],
]

chatbot = Chat(pairs, reflections)

# Fonction pour obtenir une réponse de Gemini
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')  # Utilisez le modèle Gemini Pro
    response = model.generate_content(prompt)
    return response.text

# Fonction de reconnaissance vocale (inchangée)
def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Veuillez parler...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='fr-FR')
        st.write("Vous avez dit : " + text)
        return text
    except sr.UnknownValueError:
        st.error("Désolé, je n'ai pas compris.")
        return ""
    except sr.RequestError as e:
        st.error("Erreur de service; {0}".format(e))
        return ""

# Fonction pour obtenir la réponse du chatbot (modifiée pour utiliser Gemini)
def get_response(user_input):
    if user_input:
        # Utilisez Gemini pour obtenir une réponse
        return get_gemini_response(user_input)
    return "Je n'ai pas compris."

# Créer l'application Streamlit (inchangée)
def main():
    st.title("Chatbot à commande vocale ")

    user_input = st.text_input("Entrez votre message / utilisez la commande vocale")

    if st.button("Utiliser la voix"):
        user_input = transcribe_audio()

    if user_input:
        response = get_response(user_input)
        st.write("Chatbot : " + response)

if __name__ == "__main__":
    main()