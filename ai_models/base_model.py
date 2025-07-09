from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Clase base abstracta para definir la estructura de los modelos de IA.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Método abstracto para generar texto a partir de un prompt.
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Método abstracto para obtener información del modelo.
        """
        pass
