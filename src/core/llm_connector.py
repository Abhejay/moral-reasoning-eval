from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLLMConnector(ABC):
    """Base abstract class for all LLM API connectors."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
    
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def extract_score_and_reasoning(self, response_text: str) -> Dict[str, Any]:
        """Extract structured data from LLM response."""
        pass