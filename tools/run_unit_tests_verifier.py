import argparse
from verifiers.unit_test_verifier import run_pytest

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    args = ap.parse_args()

    r = run_pytest(args.repo)
    print("OK:", r.ok)
    print("RETURN:", r.returncode)
    print("--- STDOUT ---")
    print(r.stdout)
    print("--- STDERR ---")
    print(r.stderr)

if __name__ == "__main__":
    main()
