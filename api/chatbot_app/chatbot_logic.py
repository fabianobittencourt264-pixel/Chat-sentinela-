import json
import google.generativeai as genai

class Chatbot:
    """
    The core logic for the chatbot. It uses the Google Gemini API to generate
    responses, guided by a configuration file.
    """

    def __init__(self, config_path: str, api_key: str):
        """
        Initializes the Chatbot by loading its configuration and setting up
        the Google Gemini client.

        Args:
            config_path: The file path to the config.json file.
            api_key: The Google Gemini API key.
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        if not api_key:
            raise ValueError("Google Gemini API key is required.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.system_prompt_base = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """
        Builds the instructional part of the prompt from the config file.
        """
        persona = self.config.get('persona', 'um assistente prestativo')
        description = self.config.get('description', '')
        style = self.config.get('style', {})
        tone = style.get('tone', 'claro e conciso')
        language = style.get('language', 'Português do Brasil')

        prompt = (
            f"INSTRUÇÕES: Você é '{persona}'. {description} "
            f"Seu tom deve ser {tone}. Responda em {language}. "
            "Se a pergunta for sobre um serviço público de Natividade da Serra, "
            "use as informações das fontes oficiais para basear sua resposta. Fontes: "
            f"Prefeitura: {self.config['sources']['prefeitura']}, "
            f"Carta de Serviços: {self.config['sources']['carta_geral']}. "
            "Se não souber a resposta, diga que não encontrou a informação e sugira "
            "contatar a ouvidoria. Não invente informações. "
            "A seguir, a pergunta do usuário.\n\nPERGUNTA: "
        )
        return prompt

    def get_response(self, user_message: str) -> str:
        """
        Generates a response to the user's message by calling the Gemini API.

        Args:
            user_message: The message sent by the user.

        Returns:
            A string containing the chatbot's AI-generated reply.
        """
        full_prompt = self.system_prompt_base + user_message

        try:
            response = self.model.generate_content(full_prompt)
            # Add basic safety check for blocked responses
            if not response.parts:
                return "Não posso responder a essa pergunta. Por favor, tente reformular."
            return response.text.strip()
        except Exception as e:
            print(f"Error calling Google Gemini API: {e}")
            return "Desculpe, não consegui me conectar com a minha inteligência artificial no momento. Tente novamente mais tarde."
