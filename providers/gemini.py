import os
from typing import Any, Dict, Optional
from .base import BaseProvider

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None


class GeminiProvider(BaseProvider):
    def __init__(self):
        self.api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.thinking_budget: int = int(os.getenv("GEMINI_THINKING_BUDGET", "-1"))

        if genai and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None
        else:
            self.client = None

    def generate(self, prompt: str, system: str | None = None) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError(
                "Gemini não está configurado corretamente. "
                "Verifique dependências e a variável de ambiente GEMINI_API_KEY."
            )

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

        config_kwargs: Dict[str, Any] = {}
        if system:
            config_kwargs["system_instruction"] = system

        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=self.thinking_budget
        )

        generate_content_config = types.GenerateContentConfig(**config_kwargs)

        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            )
        except Exception as e:
            raise RuntimeError(f"Falha ao chamar Gemini: {e}") from e

        text = getattr(resp, "text", "") or ""
        try:
            raw = resp.to_dict() if hasattr(resp, "to_dict") else {"_raw": str(resp)}
        except Exception:
            raw = {"_raw": str(resp)}

        return {"text": text, "raw": raw}
