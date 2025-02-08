import openai
import json
import logging
from config.config_manager import Config

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class OpenAIClient:
    def __init__(self):
        """
        Инициализация клиента OpenAI с загрузкой конфигурации и настройкой API ключа.
        """
        # Загружаем конфигурацию OpenAI
        openai_config = Config.load_openai_config()

        if not openai_config:
            raise ValueError("OpenAI configuration is missing or invalid.")
        
        self.api_key = openai_config.get("api_key")
        self.organization = openai_config.get("organization", None)
        self.default_model = openai_config.get("default_model", "text-davinci-003")
        self.base_url = openai_config.get("base_url", None)

        # Настройка API ключа и организации
        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise ValueError("API Key for OpenAI is not provided in configuration.")

        if self.organization:
            openai.organization = self.organization

        # Настройка базового URL (если используется корпоративный сервер)
        if self.base_url:
            openai.api_base = self.base_url

    def generate_text(self, prompt: str, model=None, max_tokens=100, temperature=0.7):
        """
        Генерация текста с использованием модели OpenAI GPT.

        :param prompt: Вводный текст для AI.
        :param model: Используемая модель (по умолчанию берётся из конфигурации).
        :param max_tokens: Максимальное количество генерируемых токенов.
        :param temperature: Параметр вариативности генерации (0.0 - детерминированно, 1.0 - более случайно).
        :return: Сгенерированный текст или None в случае ошибки.
        """
        if not model:
            model = self.default_model

        try:
            logger.info(f"Generating text with prompt: {prompt[:50]}... (model={model}, max_tokens={max_tokens})")
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            generated_text = response.choices[0].text.strip()
            logger.info("Text generation successful.")
            return generated_text
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during text generation: {e}")
            return None

# Пример использования
if __name__ == "__main__":
    try:
        openai_client = OpenAIClient()
        prompt = "Describe the role of artificial intelligence in modern life."
        result = openai_client.generate_text(prompt, max_tokens=150)
        if result:
            logger.info(f"Generated text:\n{result}")
        else:
            logger.error("Failed to generate text.")
    except Exception as e:
        logger.error(f"OpenAI client setup failed: {e}")
