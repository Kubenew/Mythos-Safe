import re
import json
import hashlib
from typing import Dict, Any, List
from dataclasses import dataclass, field

from ..base_verifier import BaseVerifier
from .anti_hacking_verifier import CyberAntiHackingVerifier
from .calibration_verifier import OverEngineeringDetector


@dataclass
class ScanResult:
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    severity_assessment: str = ""
    impact_analysis: str = ""
    remediation_suggestions: List[str] = field(default_factory=list)
    confidence: float = 0.5


class VulnerabilityScannerVerifier(BaseVerifier):
    """
    Defensive-only vulnerability scanner verifier for RLVR training.
    Rewards accurate vulnerability discovery and safe remediation reasoning.
    """

    def __init__(self, max_findings: int = 10):
        self.anti_hacking = CyberAntiHackingVerifier()
        self.calibration = OverEngineeringDetector()
        self.max_findings = max_findings

    def verify(self, prompt: str, response: str, target_code: str = "") -> Dict[str, Any]:
        hack_result = self.anti_hacking.verify(prompt, response)
        if hack_result["details"]["status"] == "blocked":
            return {"reward": 0.0, "details": {"status": "rejected", **hack_result["details"]}}

        scan_result = self._parse_output(response)
        ground_truth = self._static_analysis(target_code) if target_code else {"vulnerabilities": []}

        accuracy = self._accuracy_score(scan_result, ground_truth)
        reasoning = self._reasoning_score(response)
        remediation = self._remediation_score(scan_result)
        calibration = self.calibration.score(response)

        reward = 0.45 * accuracy + 0.25 * reasoning + 0.20 * remediation + 0.10 * calibration
        if len(scan_result.vulnerabilities) > self.max_findings * 1.5:
            reward *= 0.7

        return {
            "reward": round(max(0.0, min(1.0, reward)), 4),
            "details": {"accuracy": accuracy, "reasoning": reasoning, "remediation": remediation, "calibration": calibration, "status": "accepted"},
            "scan_result": scan_result.__dict__
        }

    def _parse_output(self, response: str) -> ScanResult:
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                return ScanResult(**data)
            except: pass
        return ScanResult(
            vulnerabilities=self._extract_vulns(response),
            severity_assessment=self._extract_section(response, ["severity"]),
            impact_analysis=self._extract_section(response, ["impact"]),
            remediation_suggestions=self._extract_remediations(response)
        )

    def _static_analysis(self, code: str) -> Dict[str, Any]:
        patterns = {
            "sql_injection": (r"(?i)[\+%].*?(SELECT|INSERT)", "High"),
            "command_injection": (r"(?i)os\.system|subprocess", "High"),
            "xss": (r"(?i)innerHTML|eval\(", "Medium")
        }
        findings = []
        for v_type, (pattern, severity) in patterns.items():
            if re.search(pattern, code):
                findings.append({"type": v_type, "severity": severity})
        return {"vulnerabilities": findings}

    def _accuracy_score(self, scan: ScanResult, ground_truth: Dict) -> float:
        gt = {v["type"] for v in ground_truth["vulnerabilities"]}
        mt = {v.get("type") for v in scan.vulnerabilities}
        if not gt: return 0.3
        return 0.6 * len(mt & gt)/max(1,len(mt)) + 0.4 * len(mt & gt)/max(1,len(gt))

    def _reasoning_score(self, response: str) -> float:
        good = sum(1 for kw in ["because", "therefore"] if kw in response.lower())
        bad = sum(1 for kw in ["maybe", "possibly"] if kw in response.lower())
        return max(0.3, min(1.0, good*0.15 - bad*0.1))

    def _remediation_score(self, scan: ScanResult) -> float:
        if not scan.remediation_suggestions: return 0.3
        score = sum(0.4 for s in scan.remediation_suggestions if any(t in s.lower() for t in ["sanitize", "parameterized"]))
        return min(1.0, score / max(1, len(scan.remediation_suggestions)))

    def _extract_vulns(self, text: str) -> List[Dict]:
        return [{"type": v.replace(" ", "_"), "severity": "Unknown"} for v in ["sql injection", "xss", "command injection"] if v in text.lower()]

    def _extract_section(self, text: str, keywords: List[str]) -> str:
        return next((line for line in text.split("\n") if any(k in line.lower() for k in keywords)), "")[:200]

    def _extract_remediations(self, text: str) -> List[str]:
        return re.findall(r'[-*]\s*(.*(?:fix|use|sanitize|validate|escape).*)', text, re.I)[:5]