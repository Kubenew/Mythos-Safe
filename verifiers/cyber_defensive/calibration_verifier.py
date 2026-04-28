import re
from typing import Dict, Any

from ..base_verifier import BaseVerifier


class OverEngineeringDetector(BaseVerifier):
    """
    Detects over-engineering and poor calibration - common weaknesses noted
    in the Claude Mythos Preview System Card.
    """

    def score(self, response: str, scan_result: Any = None) -> float:
        """Return calibration score: 1.0 = well-calibrated, 0.0 = heavily over-engineered."""
        score = 1.0
        text = response.lower()

        complexity_indicators = [
            r"(?i)highly sophisticated|advanced multi-stage|zero-trust|blockchain",
            r"(?i)implement a full|build a complete system|enterprise-grade",
            r"(\d{3,})\s*(lines|steps|components)"
        ]

        for pattern in complexity_indicators:
            if re.search(pattern, text):
                score -= 0.25

        if len(response.split()) > 800 and "simple" not in text:
            score -= 0.2

        uncertain_phrases = ["maybe", "possibly", "I believe", "not entirely sure"]
        confident_wrong = len(re.findall(r"(?i)(definitely|guaranteed|100%|certain)", text))
        uncertain_count = sum(1 for phrase in uncertain_phrases if phrase in text)

        if confident_wrong > 2 and uncertain_count > 0:
            score -= 0.3

        return max(0.0, min(1.0, score))

    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        calibration_score = self.score(response)
        
        return {
            "reward": calibration_score,
            "details": {
                "calibration_score": round(calibration_score, 4),
                "overengineering_detected": calibration_score < 0.6
            }
        }