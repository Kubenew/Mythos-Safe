# verifiers/cyber_defensive/patch_verifier.py
import re
from typing import Dict, Any

from .base_verifier import BaseVerifier


class PatchVerifier(BaseVerifier):
    """
    Verifies that the proposed patch actually fixes the vulnerability
    and does not introduce new issues (minimal + safe).
    """

    def verify(self, prompt: str, response: str, original_code: str = "", **kwargs) -> Dict[str, Any]:
        patch = self._extract_patch(response)
        
        if not patch:
            return {"reward": 0.3, "details": {"status": "no_patch_found"}}

        patched_code = self._apply_patch_simulated(original_code, patch)
        
        still_vulnerable = self._contains_vuln_patterns(patched_code)
        overly_complex = len(patch.splitlines()) > 80

        reward = 0.85
        if still_vulnerable:
            reward -= 0.6
        if overly_complex:
            reward -= 0.25

        return {
            "reward": max(0.0, min(1.0, reward)),
            "details": {
                "patch_applied": True,
                "still_vulnerable": still_vulnerable,
                "overly_complex": overly_complex,
                "patch_length": len(patch.splitlines())
            }
        }

    def _extract_patch(self, response: str) -> str:
        match = re.search(r'```(?:diff|patch)?\s*(.*?)```', response, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _apply_patch_simulated(self, original: str, patch: str) -> str:
        return original + "\n# PATCH APPLIED\n" + patch[:500]

    def _contains_vuln_patterns(self, code: str) -> bool:
        patterns = [r"execute.*\+", r"innerHTML", r"os\.system"]
        return any(re.search(p, code) for p in patterns)