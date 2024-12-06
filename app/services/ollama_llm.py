from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests
import json

class OllamaLLM(LLM):
    model_name: str = "llama3.2"
    api_url: str = "http://localhost:11434/api/generate"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt
        }

        try:
            response = requests.post(self.api_url, json=payload, stream=True)  # Enable streaming
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)  # Parse each chunk as JSON
                        full_response += chunk.get("response", "")  # Accumulate response
                        if chunk.get("done"):  # Check if response is complete
                            break
                    except json.JSONDecodeError as e:
                        print(f"Error parsing chunk: {e}, Line: {line}")

            if stop:
                for token in stop:
                    full_response = full_response.split(token)[0]

            return full_response.strip()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            raise

    @property
    def _llm_type(self) -> str:
        return "ollama"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.model_name}
