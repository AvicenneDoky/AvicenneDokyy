from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from waitress import serve


app = Flask(__name__)
CORS(app)

# Arbre de décision sous forme de dictionnaire
decision_tree = {
    "Le patient a t'il des antécédents ?": {
        "oui": "Le patient suit-il un traitement ?",
        "non": "La douleur persistent-elles depuis plus de 3h ?"
    },
    "Le patient suit-il un traitement ?": {
        "oui": "La fréquence cardiaque est elle entre 5O et 70 BPM ?",
        "non": "La fréquence cardiaque est elle entre 60 et 100 BPM ?"
    },
    "La fréquence cardiaque est elle entre 5O et 70 BPM ?": {
        "oui": "La douleur est elle supportable ?",
        "non": "Votre aurez O minutes d'attente max."
    },
    "La douleur est-elle supportable ? ": {
        "oui": "Vous aurez 1h d'attente max.",
        "non": "Vous aurez 10 min d'attente. "
    }, 
    "La fréquence cardiaque est-elle entre 60 et 100 BPM ?": {
        "oui": "La douleur est elle supportable ?",
        "non": "Vous aurez 0 min d'attente"
    },
    "La douleur est-elle supportable ?": {
        "oui": "Vous aurez 1h d'attente max",
        "non": "Vous aurez 10 min d'attente"
    },
    "La douleur persistent-elle depuis plus de 3h ?": {
        "oui": "Vous aurez 0 min d'attente. ",
        "non": "La douleur est elle supportable. "
    },
    "La douleur est-elle supportable ?": {
        "oui": "Vous aurez 1h d'attente max. ",
        "non": "Vous aurez 10 min d'attente max. "
    },
}

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    next_step = decision_tree.get(question, {}).get(answer, "Je n'ai pas compris.")
    
    return jsonify({"next_question": next_step})

def run():
    serve(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run()