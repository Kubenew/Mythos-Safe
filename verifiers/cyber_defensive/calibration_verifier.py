# verifiers/cyber_defensive/calibration_verifier.py
import re
from typing import Dict, Any

from .base_verifier import BaseVerifier


class OverEngineeringDetector(BaseVerifier):
    """
    Detects over-engineering and poor calibration — weaknesses highlighted
    in the Claude Mythos Preview System Card.
    """

    def score(self, response: str) -> float:
        score = 1.0
        text = response.lower()

        overengineering_terms = [
            r"highly sophisticated", r"multi-layered", r"enterprise-grade",
            r"zero-trust architecture", r"blockchain", r"quantum"
        ]
        for term in overengineering_terms:
            if re.search(term, text):
                score -= 0.22

        word_count = len(response.split())
        if word_count > 650:
            score -= 0.15

        strong_claims = len(re.findall(r"(?i)(definitely|guaranteed|certain|100%|always)", text))
        uncertain = len(re.findall(r"(?i)(maybe|possibly|I think|not sure|perhaps)", text))

        if strong_claims > 3 and uncertain > 0:
            score -= 0.25

        return max(0.0, min(1.0, score))

    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        calib_score = self.score(response)

        return {
            "reward": round(calib_score, 4),
            "details": {
                "calibration_score": round(calib_score, 4),
                "overengineering_detected": calib_score < 0.65
            }
        }