#!/usr/bin/env python3
import urllib.parse
import urllib.request
import time
from itertools import permutations

URL = "http://localhost:8080/decrypt"
parts = ["aw2246", "french44", "pledgeor"]
specials = ["", "!", "@", "#", "$", "%", "^", "&", "*", "_", "-", "+", "=", ".", "?", "1", "123", "!!", "0"]

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

def generate():
    seen = set()

    def add(pw):
        if pw and pw not in seen:
            seen.add(pw)
            yield pw

    # plain reorders, pairs, singles, case
    for order in permutations(parts, 3):
        base = "".join(order)
        yield from add(base)
        yield from add(base.lower())
        yield from add(base.upper())
        yield from add(base.capitalize())
    for a, b in permutations(parts, 2):
        yield from add(a + b)
    for p in parts:
        yield from add(p)

    # specials on every reorder
    for order in permutations(parts, 3):
        base = "".join(order)
        for pre in specials:
            for post in specials:
                yield from add(pre + base + post)
        for mid in specials:
            if not mid:
                continue
            yield from add(order[0] + mid + order[1] + order[2])
            yield from add(order[0] + order[1] + mid + order[2])
            yield from add(order[0] + mid + order[1] + mid + order[2])

    # big number sweep: aw 0-9999, french 0-99 (this is the bulk)
    for n1 in range(10000):
        for n2 in range(100):
            yield from add(f"aw{n1}french{n2}pledgeor")
            if n1 < 1000 and n2 < 50:
                yield from add(f"aw{n1:04d}french{n2:02d}pledgeor")

    # offsets around the known numbers
    for d1 in range(-200, 201):
        for d2 in range(-50, 51):
            yield from add(f"aw{2246 + d1}french{44 + d2}pledgeor")

def main():
    print("[*] Generating candidates (this may take a moment)...")
    cands = list(generate())
    print(f"[*] Trying {len(cands):,} candidates")
    start = time.time()
    for i, pw in enumerate(cands, 1):
        if i % 200 == 0:
            elapsed = time.time() - start
            rate = i / elapsed if elapsed else 0
            eta_h = (len(cands) - i) / rate / 3600 if rate else 0
            print(f"[*] {i:,}/{len(cands):,} {rate:.1f}/s ETA {eta_h:.1f}h last={pw}", flush=True)
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
