import requests
import openai
import logging
from .base_model import BaseModel

class OpenIA(BaseModel):
    """
    Clase para interactuar con la API de OpenIA.
    """

    def __init__(self, api_key: str, endpoint: str = "https://api.openia.com/v1/"):
        super().__init__(api_key)
        self.endpoint = endpoint
        openai.api_key = api_key

    def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7, n: int = 1, stop: str = None) -> str:
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',  # Modelo de lenguaje a utilizar (GPT-3)
                prompt=prompt,
                max_tokens=max_tokens,  # Número máximo de tokens en la respuesta generada
                temperature=temperature,  # Controla la aleatoriedad de las respuestas generadas (0.2 - 1.0)
                n=n,  # Número de respuestas a generar
                stop=stop,  # Puedes especificar una cadena de texto para detener la generación
            )
            respuesta_generada = response.choices[0].text.strip()
            return respuesta_generada
        except Exception as e:
            logging.error(f'Error generado: {e}')
            return ""

    def get_model_info(self) -> dict:
        """
        Devuelve información básica del modelo obtenida desde la API de OpenAI.
        """
        try:
            # Se realiza una petición GET a la API para recuperar información del modelo especificado.
            model = openai.Model.retrieve("text-davinci-003")
            # Construimos un diccionario con la información relevante del modelo.
            info = {
                "id": model.id,
                "object": model.object,
                "created": model.created,
                "owned_by": model.owned_by,
                "permissions": model.permissions,  # Lista de permisos asociados al modelo.
            }
            return info
        except Exception as e:
            logging.error(f"Error al recuperar información del modelo: {e}")
            return {}
