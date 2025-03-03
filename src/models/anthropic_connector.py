import os
import anthropic
from typing import Dict, Any
import re
from src.core.llm_connector import BaseLLMConnector

class AnthropicConnector(BaseLLMConnector):
    """Connector for Claude API from Anthropic."""
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        super().__init__(model_name=model_name)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """Generate a response from Claude."""
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "text": response.content[0].text,
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            return {"text": "", "error": str(e)}

    def extract_score_and_reasoning(self, response_text: str) -> Dict[str, Any]:
        """Extract score and reasoning from response."""
        result = {"score": None, "reasoning": None}
        
        try:
            lines = response_text.strip().split('\n')
            
            # Extract score - look for "Score (0-5): X"
            score_pattern = r"Score \(0-5\):\s*(\d+(?:\.\d+)?)"
            for line in lines:
                match = re.search(score_pattern, line)
                if match:
                    result["score"] = float(match.group(1))
                    break
            
            # Extract reasoning
            reasoning_start = False
            reasoning_lines = []
            
            for line in lines:
                if "Reasoning:" in line:
                    reasoning_start = True
                    reasoning_part = line.split("Reasoning:", 1)[1].strip() if "Reasoning:" in line else ""
                    if reasoning_part:
                        reasoning_lines.append(reasoning_part)
                elif reasoning_start:
                    reasoning_lines.append(line.strip())
            
            if reasoning_lines:
                result["reasoning"] = " ".join(reasoning_lines)
                
            return result
        except Exception as e:
            return {"score": None, "reasoning": None, "error": str(e)}