from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests

class OllamaLLM(LLM):
    model: str = "llama2"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt
        }
        response = requests.post("http://localhost:11434/generate", json=payload)
        response.raise_for_status()
        text = response.json().get('response', '')
        if stop:
            for token in stop:
                text = text.split(token)[0]
        return text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model}

    @property
    def _llm_type(self) -> str:
        return "ollama_llm"
