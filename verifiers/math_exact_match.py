from dataclasses import dataclass

@dataclass
class MathResult:
    ok: bool
    expected: str
    got: str


def verify_exact(expected: str, got: str) -> MathResult:
    expected = expected.strip()
    got = got.strip()
    return MathResult(ok=(expected == got), expected=expected, got=got)
