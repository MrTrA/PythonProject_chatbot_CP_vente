import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st

# Charger le fichier texte et séparer les questions et réponses
with open("questionvente.txt", 'r', encoding='utf-8') as f:
    data = f.read().splitlines()

# Créer un dictionnaire pour stocker les questions et réponses
qa_pairs = {}
for line in data:
    if ',' in line:
        question, answer = line.split(',', 1)  # Séparer en question et réponse
        qa_pairs[question.strip()] = answer.strip()

# Définir une fonction pour prétraiter le texte
def preprocess(text):
    # Tokeniser le texte en mots
    words = word_tokenize(text)
    # Supprimer les stopwords et la ponctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('french') and word not in string.punctuation]
    # Lemmatiser les mots
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Définir une fonction pour trouver la réponse la plus pertinente
def get_most_relevant_answer(query):
    # Prétraiter la requête
    query = preprocess(query)
    max_similarity = 0
    most_relevant_question = ""
    most_relevant_answer = "Je ne trouve pas de réponse à votre question. Pour plus d'informations, contactez-nous sur tazizpro987@gmail.com."

    # Comparer la requête avec chaque question dans le dictionnaire
    for question in qa_pairs:
        processed_question = preprocess(question)
        
        # Calculate union length and check if it's zero
        union_length = len(set(query).union(processed_question))
        
        if union_length == 0:  # Handle empty union
            similarity = 0  # Or assign a default similarity value
        else:
            similarity = len(set(query).intersection(processed_question)) / float(union_length)

        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_question = question
            most_relevant_answer = qa_pairs[question]

    return most_relevant_answer

# Définir la fonction du chatbot
def chatbot(question):
    # Trouver la réponse la plus pertinente
    answer = get_most_relevant_answer(question)
    # Retourner la réponse
    return answer

# Créer une application Streamlit
def main():
    st.title("AssisBot Client")
    st.write("Bonjour ! Je suis le chargé d'assistance client. Posez-moi des questions sur nos produits et services.")

    # Initialiser la variable de boucle
    continue_chatting = True
    iteration = 0

    while continue_chatting:
        # Obtenir la question de l'utilisateur
        question = st.text_input("Vous :", key=f"question_{iteration}")

        # Afficher la question de l'utilisateur
        if question:
            st.write(f"Vous : {question}")

            # Appeler la fonction du chatbot avec la question et afficher la réponse
            response = chatbot(question)
            st.write(f"AssisBot : {response}")

        # Demander à l'utilisateur s'il souhaite continuer
        continue_chatting = st.checkbox("Continuer à discuter ?", key=f"checkbox_{iteration}")

        # Incrémenter le compteur d'itération
        iteration += 1

if __name__ == "__main__":
    main()