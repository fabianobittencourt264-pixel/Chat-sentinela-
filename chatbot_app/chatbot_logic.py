import json
import re

class Chatbot:
    """
    The core logic for the chatbot. It loads its configuration from a JSON
    file and uses that to generate responses to user messages.
    """

    def __init__(self, config_path: str):
        """
        Initializes the Chatbot by loading its configuration.

        Args:
            config_path: The file path to the config.json file.
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Pre-compile regexes for intent matching for efficiency
        self.intent_patterns = {
            intent: re.compile(fr'\b{re.escape(term)}\b', re.IGNORECASE)
            for intent, term in self.config['lexicon']['intents'].items()
        }

    def _format_response(self, response_data: dict) -> str:
        """
        Formats the structured response data from the config into a single
        human-readable string.

        Args:
            response_data: A dictionary containing response parts like 'summary',
                           'steps', 'channels', etc.

        Returns:
            A formatted string combining all the available information.
        """
        parts = []
        if 'summary' in response_data:
            parts.append(response_data['summary'])

        if 'points' in response_data and response_data['points']:
            points_str = "\n".join(f"- {point}" for point in response_data['points'])
            parts.append(points_str)

        if 'steps' in response_data and response_data['steps']:
            steps_str = "\n".join(f"- {step}" for step in response_data['steps'])
            parts.append(f"**Passos:**\n{steps_str}")

        if 'documents_taxes_deadlines' in response_data:
            parts.append(f"**Documentos e Prazos:** {response_data['documents_taxes_deadlines']}")

        if 'channels' in response_data:
            # The 'channels' in the example prompts is a string, not a lookup key.
            # This part of the logic needs to be flexible.
            # For now, we just append the string.
            parts.append(f"**Canais de Atendimento:** {response_data['channels']}")

        if 'notes' in response_data:
            parts.append(f"**Observação:** {response_data['notes']}")

        return "\n\n".join(parts)

    def get_response(self, user_message: str) -> str:
        """
        Generates a response by finding the best-matching example prompt.

        It calculates a similarity score between the user's message and each
        example user query in the config file based on word overlap. If a
        sufficiently good match is found, it returns the corresponding
        assistant's response. Otherwise, it returns a fallback message.

        Args:
            user_message: The message sent by the user.

        Returns:
            A string containing the chatbot's reply.
        """
        best_match = None
        # A threshold of 1 means at least two words must match.
        highest_score = 1
        user_words = set(re.findall(r'\b\w+\b', user_message.lower()))

        for example in self.config['example_prompts']:
            example_words = set(re.findall(r'\b\w+\b', example['user'].lower()))
            score = len(user_words.intersection(example_words))

            if score > highest_score:
                highest_score = score
                best_match = example

        # If a good match is found, format and return the response
        if best_match:
            return self._format_response(best_match['assistant'])

        # Otherwise, return the fallback response
        fallback_info = self.config['fallback']['unknown_info']
        if '+ canal' in fallback_info:
            prefeitura_channel = self.config['channels']['prefeitura']
            contact_info = f"Endereço: {prefeitura_channel['address']}, Telefone: {prefeitura_channel['phone']}"
            fallback_message = fallback_info.replace(' + canal', f'\n{contact_info}')
        else:
            fallback_message = fallback_info

        return fallback_message
