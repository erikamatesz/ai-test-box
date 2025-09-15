import os
from typing import Any, Dict
from .base import BaseProvider

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None

class AzureOpenAIProvider(BaseProvider):
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if AzureOpenAI and self.api_key and self.endpoint:
            self.client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.endpoint,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
            )
        else:
            self.client = None

    def generate(self, prompt: str, system: str | None = None) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError(
                "Azure OpenAI is not properly configured. "
                "Please check environment variables and dependencies."
            )

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        params = {
            "model": self.deployment,
            "messages": messages,
        }

        resp = self.client.chat.completions.create(**params)

        text = resp.choices[0].message.content if resp and resp.choices else ""

        try:
            raw = resp.model_dump()
        except Exception:
            raw = {"_raw": str(resp)}

        return {"text": text, "raw": raw}
