#!/usr/bin/env python3
"""
L33t substitutions on the Step 2 password.
Generates many variants: single subs, two same-form subs in different
locations, mixed subs, and reorders of the three pieces.
"""
import urllib.parse
import urllib.request
import time
from itertools import product, combinations, permutations

URL = "http://localhost:8080/decrypt"
parts = ["aw2246", "french44", "pledgeor"]

# letters that can be l33t'd
LEET = {
    "a": ["4", "@"],
    "e": ["3"],
    "i": ["1", "!"],
    "o": ["0"],
    "s": ["5", "$"],
    "t": ["7"],
    "g": ["9"],
    "l": ["1"],
    "b": ["8"],
    "f": ["ph"],
    "c": ["k", "("],
    "h": ["#"],
}

def all_positions(word):
    """Return list of (index, letter) that can be substituted."""
    return [(i, c) for i, c in enumerate(word.lower()) if c in LEET]

def generate_for_string(s, max_subs=2):
    """Generate variants of s with 1 or 2 substitutions."""
    variants = {s}
    positions = all_positions(s)
    # one substitution
    for idx, letter in positions:
        for sub in LEET[letter]:
            chars = list(s)
            chars[idx] = sub
            variants.add("".join(chars))
    # two substitutions (same or different form)
    if len(positions) >= 2:
        for (i1, l1), (i2, l2) in combinations(positions, 2):
            for sub1 in LEET[l1]:
                for sub2 in LEET[l2]:
                    chars = list(s)
                    chars[i1] = sub1
                    chars[i2] = sub2
                    variants.add("".join(chars))
    return variants

def try_pw(pw):
    data = urllib.parse.urlencode({"password": pw}).encode()
    req = urllib.request.Request(URL, data=data)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.read()
        except Exception as e:
            if "403" in str(e):
                return None
            if attempt == 2:
                raise
            time.sleep(1)
    return None

def main():
    cands = set()

    # full password and all reorders of the three pieces
    bases = set()
    bases.add("".join(parts))
    for perm in permutations(parts):
        bases.add("".join(perm))
    # also pairs
    for a, b in permutations(parts, 2):
        bases.add(a + b)

    print(f"[*] Base strings: {len(bases)}")
    for base in bases:
        cands.update(generate_for_string(base))

    # also leet each piece independently then concatenate
    piece_vars = []
    for p in parts:
        piece_vars.append(generate_for_string(p))
    for combo in product(*piece_vars):
        cands.add("".join(combo))
    for perm in permutations(range(3)):
        for combo in product(*[piece_vars[i] for i in perm]):
            cands.add("".join(combo))

    cands = [c for c in cands if c]
    print(f"[*] Trying {len(cands):,} l33t candidates")
    start = time.time()

    for i, pw in enumerate(cands, 1):
        if i % 100 == 0:
            elapsed = time.time() - start
            rate = i / elapsed if elapsed else 0
            eta_min = (len(cands) - i) / rate / 60 if rate else 0
            print(f"[*] {i:,}/{len(cands):,} {rate:.1f}/s ETA {eta_min:.1f}m last={pw}", flush=True)
        body = try_pw(pw)
        if body:
            print("\n===== SUCCESS =====")
            print("Web password:", pw)
            open("FOUND_WEB_PASSWORD.txt", "w").write(pw + "\n")
            open("FOUND_SECRET.html", "wb").write(body)
            print(body[:600])
            return
    print("[-] No match")

if __name__ == "__main__":
    main()
