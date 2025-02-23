import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS for frontend-backend communication

# Fetch API Key from Environment Variable
API_KEY = GENAI_API_KEY

if not API_KEY:
    raise ValueError("API key is missing! Set the GENAI_API_KEY environment variable.")

# Configure Generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Route to serve chatbot UI
@app.route("/")
def index():
    return render_template("cbb.html")

# Chat API route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    print("Received message:", user_message)
    
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    try:
        response = model.generate_content(user_message)
        bot_message = response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't generate a response."
    except Exception as e:
        bot_message = f"Error: {e}"

    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
