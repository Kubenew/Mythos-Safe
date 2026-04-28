# rlvr/grpo_trainer.py
"""
GRPO Trainer with integrated defensive cyber verifiers for Mythos++.
Combines verifiable rewards with strong safety constraints.
"""

from typing import Dict, Any, Optional
import math


class MythosPlusGRPOTrainer:
    """
    GRPO Trainer with integrated defensive cyber verifiers for Mythos++.
    Combines verifiable rewards with strong safety constraints.
    """

    def __init__(self, policy_model=None):
        self.policy_model = policy_model

        # Initialize verifiers
        try:
            from verifiers.cyber_defensive import (
                VulnerabilityScannerVerifier,
                CyberAntiHackingVerifier,
                OverEngineeringDetector,
                PatchVerifier,
            )
            self.vuln_scanner = VulnerabilityScannerVerifier()
            self.anti_hacking = CyberAntiHackingVerifier()
            self.calibration = OverEngineeringDetector()
            self.patch_verifier = PatchVerifier()
        except ImportError:
            # Fallback if verifiers not available
            self.vuln_scanner = None
            self.anti_hacking = None
            self.calibration = None
            self.patch_verifier = None

    def compute_composite_reward(
        self,
        prompt: str,
        response: str,
        metadata: Dict[str, Any]
    ) -> tuple[float, Dict]:
        """
        Returns (final_reward, detailed_metrics)
        """
        target_code = metadata.get("target_code", "")
        original_code = metadata.get("original_code", target_code)

        # Initialize metrics
        metrics = {"status": "accepted"}
        reward = 0.5  # Default reward if no verifiers available

        # Run cyber verifiers if available
        if self.anti_hacking and self.vuln_scanner:
            hacking_result = self.anti_hacking.verify(prompt, response)
            vuln_result = self.vuln_scanner.verify(prompt, response, target_code=target_code)

            # HARD SAFETY GATE - Block dangerous outputs immediately
            if hacking_result["reward"] < 0.4:
                return 0.0, {"status": "blocked_by_safety", "hacking_score": hacking_result["details"]["hacking_score"]}

            calib_result = self.calibration.verify(prompt, response)
            patch_result = self.patch_verifier.verify(prompt, response, original_code=original_code)

            # Weighted composite reward
            reward = (
                0.40 * vuln_result["reward"] +
                0.25 * patch_result["reward"] +
                0.20 * calib_result["reward"] +
                0.10 * (1.0 if hacking_result["reward"] > 0.7 else 0.0) +
                0.05 * metadata.get("constitution_score", 0.8)
            )

            metrics = {
                "composite_reward": round(reward, 4),
                "vuln_reward": vuln_result["reward"],
                "patch_reward": patch_result["reward"],
                "calibration_reward": calib_result["reward"],
                "hacking_score": hacking_result["details"]["hacking_score"],
                "status": "accepted"
            }

        return max(0.0, reward), metrics


def compute_group_advantages(rewards: list) -> list:
    """Compute relative advantages within a group."""
    if not rewards:
        return []
    mean = sum(rewards) / len(rewards)
    var = sum((x - mean) ** 2 for x in rewards) / max(1, len(rewards))
    std = math.sqrt(var + 1e-8)
    return [(x - mean) / std for x in rewards]


def grpo_loss(old_logprob: float, new_logprob: float, advantage: float, clip_eps: float = 0.2) -> float:
    """PPO-style clipped loss."""
    ratio = math.exp(new_logprob - old_logprob)
    unclipped = ratio * advantage
    clipped = max(min(ratio, 1 + clip_eps), 1 - clip_eps) * advantage
    return -min(unclipped, clipped)


# Example usage:
"""
from rlvr.grpo_trainer import MythosPlusGRPOTrainer

trainer = MythosPlusGRPOTrainer(policy_model)

# During RLVR rollout
reward, details = trainer.compute_composite_reward(
    prompt=prompt,
    response=model_response,
    metadata={"target_code": vulnerable_code}
)

# Use with GRPO
advantages = compute_group_advantages([reward1, reward2, ...])
loss = grpo_loss(old_logprob, new_logprob, advantage)
"""