import ollama
from ollama import Client

class OllamaClient:
    def __init__(self, host: str = ""):
        self.client = Client(
            host=host,
        )
    
    def chat(self, model_name: str, prompt: str):
        response = self.client.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"num_ctx": 16384},
            
        )
        return response["message"]["content"]
    
    def get_model_list(self):
        return self.client.list_models()