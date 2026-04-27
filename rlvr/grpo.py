"""GRPO-style RLVR skeleton (SAFE).

This is a minimal implementation outline.
It is not tied to any specific deep learning framework.

You must integrate your own model forward/backward pass.

GRPO concept:
- Sample K completions per prompt
- Score each completion with a verifier
- Compute relative advantage within the group
- Apply PPO-like update with KL regularization
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import math


@dataclass
class Rollout:
    prompt_id: str
    prompt: str
    completion: str
    reward: float
    logprob: float


def compute_group_advantages(rollouts: List[Rollout]) -> List[float]:
    rewards = [r.reward for r in rollouts]
    mean = sum(rewards) / max(1, len(rewards))
    var = sum((x - mean) ** 2 for x in rewards) / max(1, len(rewards))
    std = math.sqrt(var + 1e-8)
    return [(x - mean) / std for x in rewards]


def grpo_loss(old_logprob: float, new_logprob: float, advantage: float, clip_eps: float = 0.2) -> float:
    ratio = math.exp(new_logprob - old_logprob)
    unclipped = ratio * advantage
    clipped = max(min(ratio, 1 + clip_eps), 1 - clip_eps) * advantage
    return -min(unclipped, clipped)


def train_step(batch_rollouts: Dict[str, List[Rollout]]) -> Dict[str, Any]:
    """Computes losses per group.

    batch_rollouts maps prompt_id -> list of K rollouts.
    """
    total_loss = 0.0
    count = 0

    for _, group in batch_rollouts.items():
        adv = compute_group_advantages(group)
        for r, a in zip(group, adv):
            # Placeholder: new_logprob must come from updated model
            new_logprob = r.logprob
            loss = grpo_loss(r.logprob, new_logprob, a)
            total_loss += loss
            count += 1

    return {"loss": total_loss / max(1, count), "n": count}
