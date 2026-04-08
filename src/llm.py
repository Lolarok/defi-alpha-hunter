# LLM Abstraction Layer
import os
from typing import Dict, Any, Optional
import openai
import anthropic
from google.cloud import genai

class LLMClient:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers = {}
        
        # Initialize providers if keys are provided
        openai.api_key = os.getenv("OPENAI_API_KEY")
        anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")
        # Google GenAI would need credentials setup
        
    def get_provider(self, name: str):
        """Get LLM provider"""
        if name == "openai":
            return self._openai_provider
        elif name == "anthropic":
            return self._anthropic_provider
        elif name == "google"
            return self._google_provider
        else:
            raise ValueError(f"Unknown provider: {name}")
    
    def _openai_provider(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """Use OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI error: {str(e)}"
    
    def _anthropic_provider(self, prompt: str, model: str = "claude-sonnet") -> str:
        """Use Anthropic API"""
        try:
            response = anthropic.chat_completion(
                model=model,
                max_tokens=1024,
                temperature=0.7,
                message=prompt
            )
            return response.message.content
        except Exception as e:
            return f"Anthropic error: {str(e)}"
    
    def _google_provider(self, prompt: str, model: str = "gemini-1.5-pro") -> str:
        """Use Google GenAI API"""
        try:
            # Implementation would require Google Cloud credentials
            return "Google GenAI not implemented in demo"
        except Exception as e:
            return f"Google error: {str(e)}"
    
    def generate_text(self, prompt: str, provider: str = "openai", model: str = None) -> str:
        """Generate text using specified provider"""
        provider_func = self.get_provider(provider)
        return provider_func(prompt, model)