# Mythos-Safe Blueprint (Defensive RLVR + Alignment Toolkit)

**Generated:** 2026-04-27

This project is a **SAFE** blueprint for building and evaluating advanced LLMs with:
- RLVR (Reinforcement Learning with Verifiable Rewards)
- Constitutional AI-style steering
- Safety evaluation + monitoring
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
- `rlvr/` : RLVR algorithm skeleton (GRPO-style)
- `verifiers/` : Deterministic verifiers (unit tests, math exact-match)
- `eval/` : Evaluation harness
- `monitoring/` : Safety telemetry + incident response templates
- `datasets/` : Dataset schema + generation guidelines (safe)
- `examples/` : Minimal examples and toy tasks

## What You Need To Add

This repo is intentionally **non-operational** for full model training:
- A base model checkpoint
- Your distributed training stack (DeepSpeed/FSDP/etc.)
- Real datasets and legal permissions

## Safety Notes

- Keep all execution sandboxed.
- Log all tool calls and verifier interactions.
- Treat any autonomous agent evaluation as **high risk**.

## License

MIT
