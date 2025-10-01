from typing import Any, Dict
from .base import BaseUseCase
from providers.base import BaseProvider

JOBS_SYSTEM = (
    "You are an assistant that analyzes job descriptions. "
    "Your goal is to condense the requirements into a clear, unique list of "
    "skills, tools, and knowledge areas that a candidate should study "
    "to prepare and apply. "
    "Do not repeat any item more than once, even if it appears in multiple job descriptions."
)

class JobRequirementsUseCase(BaseUseCase):
    def run(self, provider: BaseProvider, job_descriptions: str, **kwargs: Any) -> Dict[str, Any]:
        system = kwargs.get("system") or JOBS_SYSTEM

        prompt = (
            "Analyze the job descriptions below and extract the key "
            "requirements in terms of knowledge and skills. "
            "Consolidate them into a unique list, removing any duplicates. "
            "Each requirement should appear only once, even if it was mentioned multiple times. "
            "Provide the output as a clear, concise bullet-point list.\n\n"
            f"Job descriptions:\n{job_descriptions}"
        )

        return provider.generate(prompt=prompt, system=system)
