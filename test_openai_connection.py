import openai
import json

def get_openai_api_key():
    config_path = "D:/AI_Coordinator_Project/config/openai_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["openai_api_key"]

# Установите ключ OpenAI API
openai.api_key = get_openai_api_key()

# Отправьте тестовый запрос
try:
    response = openai.completions.create(
        model="gpt-3.5-turbo",
        prompt="Hello, world!",
        max_tokens=50
    )
    print("Connection successful! Generated text:")
    print(response['choices'][0]['text'].strip())
except openai.error.APIError as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
