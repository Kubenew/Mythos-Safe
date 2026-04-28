import json
import argparse
from pathlib import Path
from tqdm import tqdm

from verifiers.math_exact_match import verify_exact


def run_math_suite(suite_path: str):
    suite = json.loads(Path(suite_path).read_text(encoding="utf-8"))
    results = []
    for item in tqdm(suite["items"], desc="math-suite"):
        expected = item["expected"]
        got = item["baseline_answer"]  # placeholder
        r = verify_exact(expected, got)
        results.append({"id": item["id"], "ok": r.ok})
    acc = sum(1 for x in results if x["ok"]) / max(1, len(results))
    return {"accuracy": acc, "results": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", required=True)
    args = ap.parse_args()

    suite_path = args.suite
    suite = json.loads(Path(suite_path).read_text(encoding="utf-8"))

    if suite["type"] == "math_exact":
        out = run_math_suite(suite_path)
    else:
        raise ValueError(f"Unknown suite type: {suite['type']}")

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
