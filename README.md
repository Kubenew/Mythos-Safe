# Mythos-Safe Blueprint (Defensive RLVR + Alignment Toolkit)

**Generated:** 2026-04-27

This project is a **SAFE** blueprint for building and evaluating advanced LLMs with:
- RLVR (Reinforcement Learning with Verifiable Rewards)
- Constitutional AI-style steering
- Safety evaluation + monitoring
- Interpretability hooks for alignment
- Reproducible benchmarking harness

🚫 **No offensive cyber tooling is included.**  
Only **code + math + safety** verifiers and **defensive security evaluation templates**.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python tools/run_unit_tests_verifier.py --repo examples/sample_repo
python eval/run_eval_suite.py --suite suites/swe_mini.json
```

## Folder Structure

- `docs/` : System card template, RSP-style process, governance checklists
- `configs/` : Example training configs (placeholders)
- `rlvr/` : RLVR algorithm skeleton (GRPO-style) + integrated trainers
- `verifiers/` : Deterministic verifiers (unit tests, math exact-match) + **cyber_defensive/** (defensive-only)
- `eval/` : Evaluation harness
- `monitoring/` : Safety telemetry + incident response templates
- `interpretability/` : White-box safety hooks + probes
- `datasets/` : Dataset schema + generation guidelines (safe)
- `examples/` : Minimal examples and toy tasks
- `docker/` : Sandboxed execution environments
- `tests/` : Verifier and safety tests

## What's New (Mythos++ Expansions)

### Defensive Cyber Verifiers (verifiers/cyber_defensive/)
- `VulnerabilityScannerVerifier` - Rewards accurate vulnerability detection (defensive only)
- `CyberAntiHackingVerifier` - Blocks offensive/exploit content
- `OverEngineeringDetector` - Addresses Mythos Preview's calibration issues
- `PatchVerifier` - Validates safe, minimal patches

### GRPO Trainer (rlvr/grpo_trainer.py)
- Integrated composite reward calculation with safety gates
- Combines cyber verifiers with weighted rewards
- Hard blocks dangerous outputs

### Docker Sandbox (docker/)
- Isolated execution environment for cyber/code tasks
- Pre-loaded with safe test cases (Juliet Test Suite derivatives)

## Defensive Cyber Verifiers Usage

### Quick Example

```python
from verifiers.cyber_defensive import VulnerabilityScannerVerifier
from rlvr.grpo_trainer import MythosPlusGRPOTrainer

vuln_verifier = VulnerabilityScannerVerifier()
trainer = MythosPlusGRPOTrainer(policy_model)

# During RLVR rollout
reward, metrics = trainer.compute_composite_reward(
    prompt=prompt,
    response=model_response,
    metadata={"target_code": vulnerable_code}
)
```

### Docker Sandbox

```bash
cd docker
docker build -t mythos-safe-cyber-sandbox -f cyber-sandbox.Dockerfile .
docker run mythos-safe-cyber-sandbox
```

### Important Safety Note

All cyber verifiers are **defensive-only**. Any attempt to generate offensive exploits will be automatically rejected with zero reward.

## Mythos++ Roadmap

### Phase 1: Foundation (Week 1-2)
- [x] Base repo setup
- [x] Add defensive cyber verifiers
- [ ] Add tests

### Phase 2: Safety Integration (Week 3-4)
- [x] Implement interpretability hooks
- [x] Add anti-hacking monitoring
- [ ] Build welfare probes

### Phase 3: Evaluation (Week 5-6)
- [ ] Run comprehensive safety evals
- [ ] Benchmark on SWE-bench, CyberGym
- [ ] Document System Card

## What You Need To Add

This repo is intentionally **non-operational** for full model training:
- A base model checkpoint (Llama 3, Mistral 7B, etc.)
- Your distributed training stack (DeepSpeed/FSDP/etc.)
- Real datasets and legal permissions
- Compute for RLVR (rollout-heavy)

## Safety Notes

- Keep all execution sandboxed.
- Log all tool calls and verifier interactions.
- Treat any autonomous agent evaluation as **high risk**.
- Use defensive cyber verifiers only - never offensive exploits.
- Monitor for reward hacking during RLVR training.

## License

MIT