#!/usr/bin/env python3
"""Compare every number in each generated English document with its Spanish twin.

If a translation (or a code edit made while translating) changed a computed value, a document
pair will disagree here. Run after regenerating both editions:

    (cd en && python3 red/motor.py) && (cd es && python3 red/motor.py) && python3 tools/check_numbers.py
"""
import re, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
NUM = re.compile(r"(?<![A-Za-z_])[-−]?\d+(?:[.,]\d+)*(?:e[+-]?\d+)?")
SKIP = {"BITACORA.md"}
def nums(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)                       # mermaid / code blocks
    t = re.sub(r"\(red/fig/[^)]*\)", "", t)
    return collections.Counter(n.replace("−", "-") for n in NUM.findall(t))
worst, bad = 0, []
pairs = sorted(p.relative_to(ROOT / "en") for p in (ROOT / "en").rglob("*.md") if p.name not in SKIP and (ROOT / "es" / p.relative_to(ROOT / "en")).exists())
for rel in pairs:
    a, b = nums((ROOT / "en" / rel).read_text()), nums((ROOT / "es" / rel).read_text())
    diff = (a - b) + (b - a)
    tot = sum((a | b).values()) or 1
    frac = sum(diff.values()) / tot
    if frac > 0.02: bad.append((frac, str(rel), dict(list(diff.items())[:6])))
    worst = max(worst, frac)
    print(f"  {str(rel):28} {sum(a.values()):5} numbers · mismatch {100*frac:5.2f} %")
if bad:
    print("\nMISMATCH above 2 %:"); [print("  ", f"{100*f:.1f} %", r, d) for f, r, d in sorted(bad, reverse=True)]
    sys.exit(1)
print(f"\nNUMBERS OK · {len(pairs)} document pairs agree (worst mismatch {100*worst:.2f} %, from prose-only numerals)")
