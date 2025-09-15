from abc import ABC, abstractmethod
from typing import Any
from providers.base import BaseProvider

class BaseUseCase(ABC):
    """Interface mínima para um caso de uso."""

    @abstractmethod
    def run(self, provider: BaseProvider, input_text: str, **kwargs: Any) -> str:
        raise NotImplementedError
