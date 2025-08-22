import os
from flask import Flask, render_template, request, jsonify
# Use a relative import now that this is a package
from .chatbot_logic import Chatbot

# Initialize the Flask application
app = Flask(__name__)

# --- Robust Path to Config File ---
# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Join it with the filename to create an absolute path to the config file.
# This makes the app runnable from any directory.
CONFIG_PATH = os.path.join(script_dir, 'config.json')

# --- Secure API Key and Chatbot Initialization ---
# Load the OpenAI API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")

chatbot = None
initialization_error = None

try:
    # Pass the API key to the Chatbot constructor
    chatbot = Chatbot(config_path=CONFIG_PATH, api_key=api_key)
except (FileNotFoundError, ValueError) as e:
    # Catch initialization errors (e.g., missing config or API key)
    # and store them to be reported via the API.
    initialization_error = str(e)
    print(f"FATAL: Chatbot could not be initialized. Error: {initialization_error}")

@app.route("/health")
def health_check():
    """
    A simple health check endpoint to confirm the app is running.
    """
    return {"status": "ok"}


@app.route("/")
def index():
    """
    Serves the main chat interface page.
    """
    return render_template("index.html")

@app.route("/ask", methods=['POST'])
def ask():
    """
    Handles the user's message from the frontend, gets a response from the
    chatbot logic, and returns it as JSON.
    """
    # First, check if the chatbot was initialized correctly.
    if initialization_error:
        return jsonify({"error": f"Chatbot is not available: {initialization_error}"}), 503

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Missing 'message' in request"}), 400

    # Get a response from the chatbot logic
    bot_reply = chatbot.get_response(user_message)

    # Return the response in the required JSON format
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    """
    Main entry point for running the Flask application.
    Debug mode is enabled for development convenience.
    """
    app.run(debug=True)
