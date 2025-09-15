from typing import Any, Dict
from .base import BaseUseCase
from providers.base import BaseProvider

# Default system prompt (can be overridden by the UI via kwargs["system"])
SUMMARY_SYSTEM = "You are an assistant that summarizes texts into clear, highlighting the key points."

class SummarizeUseCase(BaseUseCase):
    def run(self, provider: BaseProvider, input_text: str, **kwargs: Any) -> Dict[str, Any]:
        # UI can pass a custom system prompt; fallback to default if not provided
        system = kwargs.get("system") or SUMMARY_SYSTEM

        prompt = (
            "Summarize the text below into one clear, objective paragraph, keeping only the main ideas.\n\n"
            f"Text:\n{input_text}"
        )
        return provider.generate(prompt=prompt, system=system)
