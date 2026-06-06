import json
import logging
import time
from typing import Any

import requests

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.services.prompts import ACTION_PROMPT, DECISION_PROMPT, RISK_PROMPT, SUMMARY_PROMPT, TIMELINE_PROMPT
from app.settings import OLLAMA_RETRY_COUNT, OLLAMA_TIMEOUT_SECONDS


logger = logging.getLogger(__name__)


class OllamaService:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = OLLAMA_TIMEOUT_SECONDS
        self.retry_count = OLLAMA_RETRY_COUNT

    def generate_summary(self, document_text: str) -> str:
        return self._generate_text(SUMMARY_PROMPT, document_text)

    def extract_decisions(self, document_text: str) -> list[dict[str, Any]]:
        return self._generate_json(DECISION_PROMPT, document_text)

    def extract_actions(self, document_text: str) -> list[dict[str, Any]]:
        return self._generate_json(ACTION_PROMPT, document_text)

    def extract_risks(self, document_text: str) -> list[dict[str, Any]]:
        return self._generate_json(RISK_PROMPT, document_text)

    def extract_timeline(self, document_text: str) -> list[dict[str, Any]]:
        return self._generate_json(TIMELINE_PROMPT, document_text)

    def _generate_text(self, system_prompt: str, document_text: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nDocument:\n{document_text[:20000]}",
            "stream": False,
        }
        last_error: Exception | None = None
        for attempt in range(1, self.retry_count + 2):
            try:
                response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout_seconds)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()
            except requests.RequestException as exc:
                last_error = exc
                logger.warning("Ollama request failed on attempt %s/%s: %s", attempt, self.retry_count + 1, exc)
                if attempt <= self.retry_count:
                    time.sleep(min(attempt, 3))
        logger.exception("Ollama request failed after retries")
        raise RuntimeError(f"Ollama request failed: {last_error}") from last_error

    def _generate_json(self, system_prompt: str, document_text: str) -> list[dict[str, Any]]:
        raw = self._generate_text(system_prompt, document_text)
        return _parse_json_array(raw)


def _parse_json_array(raw: str) -> list[dict[str, Any]]:
    raw = raw.strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        start = raw.find("[")
        end = raw.rfind("]")
        if start == -1 or end == -1 or end <= start:
            return []
        try:
            parsed = json.loads(raw[start : end + 1])
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
