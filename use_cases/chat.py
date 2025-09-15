from typing import Any
from .base import BaseUseCase
from providers.base import BaseProvider

class ChatUseCase(BaseUseCase):
    def run(self, provider: BaseProvider, input_text: str, **kwargs: Any) -> str:
        system = kwargs.get("system")
        return provider.generate(prompt=input_text, system=system)
