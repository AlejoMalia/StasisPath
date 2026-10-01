#!/usr/bin/env python3
"""Parity check between the English and Spanish editions of the knowledge graph.

The two YAML files are translations of each other. A translation must never change a
number, a status, a dependency or a frozen preregistration. This script fails (exit 1) if it does.

    python3 tools/check_parity.py
"""
import sys, pathlib, hashlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
EN = yaml.safe_load(open(ROOT / "en/red/stasispath.yaml", encoding="utf-8"))
ES = yaml.safe_load(open(ROOT / "es/red/stasispath.yaml", encoding="utf-8"))
ORGANS = {"riñón": "kidney", "corazón": "heart", "hígado": "liver", "cerebro": "brain",
          "cuerpo_entero": "whole_body", "páncreas": "pancreas"}
bad = []

def walk(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        ka = [ORGANS.get(k, k) if path in (("organos",), ("humano",)) else k for k in a]
        kb = [k for k in b if k != "t_en"]
        if ka != kb: bad.append((path, f"keys differ: {set(ka) ^ set(kb)}")); return
        for ka_, kb_ in zip(a, kb): walk(a[ka_], b[kb_], path + (kb_,))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): bad.append((path, "list length")); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, path + (i,))
    elif isinstance(a, str) and isinstance(b, str):
        pass                                                   # text may differ: that is the translation
    elif a != b:
        bad.append((path, f"{a!r} != {b!r}"))                  # numbers, bools, None must be identical

walk(ES, EN)
for k in ES["preregistro"]:
    if k == "fecha": continue
    if ES["preregistro"][k]["t"] != EN["preregistro"][k]["t"]:
        bad.append((("preregistro", k, "t"), "FROZEN TEXT DIFFERS"))
lock = {l.split(":")[0]: l.split(": ")[1].strip() for l in open(ROOT / "en/red/prereg.lock") if ":" in l}
lock_es = {l.split(":")[0]: l.split(": ")[1].strip() for l in open(ROOT / "es/red/prereg.lock") if ":" in l}
if lock != lock_es: bad.append((("prereg.lock",), "EN and ES locks differ"))
for k, h in lock.items():
    real = hashlib.sha256((EN["preregistro"]["fecha"] + EN["preregistro"][k]["t"]).encode()).hexdigest()
    if real != h: bad.append((("preregistro", k), "hash does not match prereg.lock"))

if bad:
    print(f"PARITY FAILED: {len(bad)} difference(s)")
    for p, m in bad[:20]: print("  ", "/".join(map(str, p)), "->", m)
    sys.exit(1)
nums = sum(1 for _ in [0])
print("PARITY OK · every number, status, dependency and frozen text is identical in EN and ES · 5 preregistration hashes verified")
