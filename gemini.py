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

# Fonction de reconnaissance vocale (modifiée pour le téléchargement de fichier)
def transcribe_audio_from_file():
    uploaded_file = st.file_uploader("Téléchargez un fichier audio pour la transcription", type=["wav", "flac", "mp3"])
    if uploaded_file is not None:
        try:
            r = sr.Recognizer()
            with sr.AudioFile(uploaded_file) as source:
                audio = r.record(source)  # read the entire audio file
            try:
                text = r.recognize_google(audio, language='fr-FR')
                st.write("Vous avez dit (à partir du fichier) : " + text)
                return text
            except sr.UnknownValueError:
                st.error("Désolé, Google Speech Recognition n'a pas pu comprendre l'audio dans le fichier.")
            except sr.RequestError as e:
                st.error(f"Erreur de service Google Speech Recognition ; {e}")
        except Exception as e:
            st.error(f"Erreur lors du traitement du fichier audio : {e}")
    return None


# Fonction pour obtenir la réponse du chatbot (modifiée pour utiliser Gemini)
def get_response(user_input):
    if user_input:
        # Utilisez Gemini pour obtenir une réponse
        return get_gemini_response(user_input)
    return "Je n'ai pas compris."

# Créer l'application Streamlit
def main():
    st.title("Chatbot (avec transcription audio depuis un fichier)")

    user_input = st.text_input("Entrez votre message")
    transcribed_text = transcribe_audio_from_file()

    final_input = user_input
    if transcribed_text:
        final_input = transcribed_text

    if st.button("Envoyer"):
        if final_input:
            response = get_response(final_input)
            st.write("Chatbot : " + response)
        else:
            st.warning("Veuillez entrer un message ou télécharger un fichier audio.")

if __name__ == "__main__":
    main()
