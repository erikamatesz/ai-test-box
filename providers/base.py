from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseProvider(ABC):
    """Minimal interface for providers."""

    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> Dict[str, Any]:
        """
        Should return a dictionary with:
        - text: str  -> text ready to display in the UI
        - raw:  Any  -> raw API object/dict, useful for debugging
        """
        raise NotImplementedError
