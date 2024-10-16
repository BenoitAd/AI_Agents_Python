import os
from flask import Flask, request, jsonify
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Désactiver les logs de l'API OpenTelemetry
logging.getLogger('opentelemetry').setLevel(logging.WARNING)

load_dotenv()

# Configuration de l'API OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")

# Initialiser l'application Flask
app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Configuration de l'agent juridique
agent_juridique = Agent(
    role="Agent Juridique",
    goal="Fournir des réponses juridiques précises et contextualisées sur la modération de contenu lié aux messages haineux et aux comportements frauduleux sur les réseaux sociaux.",
    backstory="Je suis un agent juridique spécialisé dans la modération de contenu sur les réseaux sociaux. Je suis formé pour répondre à des questions juridiques concernant des messages haineux ou des comportements frauduleux."
)

# Configuration de l'agent de soutiens émotionnels
agent_emotionnel = Agent(
    role="Agent de Soutien Emotionnel",
    goal="Fournir un soutien émotionnel et des conseils sur la gestion des émotions liées à la modération de contenu et le harcèlement sur les réseaux sociaux.",
    backstory="Je suis un agent de soutien émotionnel formé pour aider les individus à gérer les émotions négatives liées à la modération de contenu et au harcèlement sur les réseaux sociaux."
)

# Configuration de l'agent de sécurité informatique
agent_securite = Agent(
    role="Agent de Sécurité Informatique",
    goal="Fournir des conseils sur les bonnes pratiques de sécurité en ligne et les comportements sécuritaires à adopter sur les réseaux sociaux.",
    backstory="Je suis un expert en sécurité informatique spécialisé dans la protection des utilisateurs et des données personnelles sur les réseaux sociaux."
)

# Route pour traiter les messages de l'utilisateur
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Récupérer les données envoyées par le front-end
        data = request.json
        user_input = data.get('message')
        agent_choice = data.get('agent')

        # Vérifier que le message et l'agent sont fournis
        if not user_input or not agent_choice:
            return jsonify({"error": "Le message et le choix de l'agent sont requis."}), 400

        # Sélectionner l'agent correspondant selon le choix de l'utilisateur
        if agent_choice == 1:
            selected_agent = agent_juridique
            task_output = "Répondre avec des conseils juridiques appropriés."
        elif agent_choice == 2:
            selected_agent = agent_emotionnel
            task_output = "Fournir un soutien émotionnel et des conseils sur la gestion des émotions."
        elif agent_choice == 3:
            selected_agent = agent_securite
            task_output = "Donner des conseils sur les bonnes pratiques de sécurité en ligne."
        else:
            return jsonify({"error": "Choix d'agent invalide. Choisissez 1 (juridique), 2 (émotionnel), ou 3 (sécurité informatique)."}), 400

        # Créer la tâche en fonction de l'agent sélectionné
        task = Task(
            description=user_input,
            expected_output=task_output,
            agent=selected_agent
        )

        # Créer l'équipe avec l'agent sélectionné
        crew = Crew(
            agents=[selected_agent],
            tasks=[task],
            verbose=True
        )

        # Lancer l'exécution
        result = crew.kickoff()

        # Conversion de CrewOutput en une chaîne de caractères
        response_str = str(result)  # Assure que le résultat est une chaîne sérialisable en JSON
        response = jsonify({"response": response_str})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'  # Forcer UTF-8 dans l'en-tête
        return response

    except Exception as e:
        response = jsonify({"error": str(e)})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'  # Forcer UTF-8 dans l'en-tête
        return response, 500

# Démarrer l'application Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)