import os
from flask import Flask, render_template, request, jsonify
from chatbot_logic import Chatbot

# Initialize the Flask application
app = Flask(__name__)

# --- Robust Path to Config File ---
# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Join it with the filename to create an absolute path to the config file.
# This makes the app runnable from any directory.
CONFIG_PATH = os.path.join(script_dir, 'config.json')

# Create an instance of the chatbot, which loads the configuration
try:
    chatbot = Chatbot(config_path=CONFIG_PATH)
except FileNotFoundError:
    # Handle the case where the config file is missing
    # In a real app, you might log this and exit, but for now, we'll raise an error.
    raise RuntimeError(f"Configuration file not found at {CONFIG_PATH}. Make sure it's in the same directory as app.py.")

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
