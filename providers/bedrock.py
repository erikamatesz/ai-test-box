import os
from typing import Any, Dict, Optional
from .base import BaseProvider

try:
    import boto3
except Exception:
    boto3 = None


class AWSBedrockProvider(BaseProvider):
    def __init__(self):
        self.api_key: Optional[str] = os.getenv("AWS_BEDROCK_API_KEY")
        self.region: str = os.getenv("AWS_REGION", "us-east-1")
        self.model: str = os.getenv("AWS_BEDROCK_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
        self.max_tokens: int = int(os.getenv("AWS_BEDROCK_MAX_TOKENS", "512"))
        self.temperature: float = float(os.getenv("AWS_BEDROCK_TEMPERATURE", "0.2"))

        if self.api_key:
            os.environ.setdefault("AWS_BEARER_TOKEN_BEDROCK", self.api_key)

        if boto3 and self.api_key:
            try:
                self.client = boto3.client("bedrock-runtime", region_name=self.region)
            except Exception:
                self.client = None
        else:
            self.client = None

    def generate(self, prompt: str, system: str | None = None) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("AWS Bedrock is not configured correctly. Check boto3 and AWS_BEDROCK_API_KEY.")

        messages = [
            {"role": "user", "content": [{"text": prompt}]}
        ]

        kwargs = {
            "modelId": self.model,
            "messages": messages,
            "inferenceConfig": {"maxTokens": self.max_tokens, "temperature": self.temperature},
        }
        if system:
            kwargs["system"] = [{"text": system}]

        try:
            resp = self.client.converse(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to call AWS Bedrock: {e}") from e

        try:
            text = resp["output"]["message"]["content"][0].get("text", "")
        except Exception:
            text = ""

        return {"text": text, "raw": resp}
