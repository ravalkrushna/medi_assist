from flask import Flask, request, jsonify
from chatbot import MedicalChatbot  # assuming your logic is in chatbot.py

app = Flask(__name__)

# Initialize chatbot with the final dataset
chatbot = MedicalChatbot("disease_and_symptoms_with_treatment.csv")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({
            "error": "No message provided"
        }), 400

    response = chatbot.get_response(user_input)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
