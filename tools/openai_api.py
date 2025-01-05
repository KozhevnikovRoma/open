import openai
import json
import logging
from config.config_manager import Config

# Настройка логирования
logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        # Загружаем конфигурацию OpenAI
        openai_config = Config.load_openai_config()

        if not openai_config:
            raise ValueError("OpenAI configuration is missing or invalid.")
        
        self.api_key = openai_config.get("openai_api_key")
        self.base_url = openai_config.get("openai_base_url")

        # Настройка ключа для OpenAI API
        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise ValueError("API Key for OpenAI is not provided in configuration.")

    def generate_text(self, prompt: str, model="text-davinci-003", max_tokens=100):
        """
        Generate text using OpenAI's GPT model.

        :param prompt: The input prompt for the AI.
        :param model: The model to use (default: "text-davinci-003").
        :param max_tokens: Maximum number of tokens to generate (default: 100).
        :return: Generated text from OpenAI API.
        """
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens
            )
            generated_text = response.choices[0].text.strip()
            return generated_text
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None

# Пример использования
if __name__ == "__main__":
    try:
        openai_client = OpenAIClient()
        prompt = "Hello, how can I assist you today?"
        result = openai_client.generate_text(prompt)
        if result:
            logger.info(f"Generated text: {result}")
        else:
            logger.error("Failed to generate text.")
    except Exception as e:
        logger.error(f"OpenAI client setup failed: {e}")
