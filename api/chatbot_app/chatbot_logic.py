import json
from openai import OpenAI

class Chatbot:
    """
    The core logic for the chatbot. It uses the OpenAI API to generate
    responses, guided by a configuration file.
    """

    def __init__(self, config_path: str, api_key: str):
        """
        Initializes the Chatbot by loading its configuration and setting up
        the OpenAI client.

        Args:
            config_path: The file path to the config.json file.
            api_key: The OpenAI API key.
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        if not api_key:
            raise ValueError("OpenAI API key is required.")

        self.client = OpenAI(api_key=api_key)
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """
        Builds the system prompt from the configuration file to instruct the AI.
        """
        persona = self.config.get('persona', 'um assistente prestativo')
        description = self.config.get('description', '')
        style = self.config.get('style', {})
        tone = style.get('tone', 'claro e conciso')
        language = style.get('language', 'Português do Brasil')

        prompt = (
            f"Você é '{persona}'. {description} "
            f"Seu tom deve ser {tone}. "
            f"Responda em {language}. "
            "Se a pergunta for sobre um serviço público de Natividade da Serra, "
            "use as informações das fontes oficiais para basear sua resposta, mas não "
            "se limite a elas. As fontes são: "
            f"Prefeitura: {self.config['sources']['prefeitura']}, "
            f"Carta de Serviços: {self.config['sources']['carta_geral']}. "
            "Se não souber a resposta, diga que não encontrou a informação e sugira "
            "contatar a ouvidoria."
        )
        return prompt

    def get_response(self, user_message: str) -> str:
        """
        Generates a response to the user's message by calling the OpenAI API.

        Args:
            user_message: The message sent by the user.

        Returns:
            A string containing the chatbot's AI-generated reply.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using a powerful and cost-effective model
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7, # A bit of creativity
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "Desculpe, não consegui me conectar com a minha inteligência artificial no momento. Tente novamente mais tarde."
