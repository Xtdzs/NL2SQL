from llms.ollama_client import OllamaClient

def generate(client: OllamaClient, model_name: str, prompt: str):
    response = client.chat(
        model_name=model_name,
        prompt=prompt,
    )
    return response