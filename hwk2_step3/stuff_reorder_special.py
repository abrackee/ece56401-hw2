#!/usr/bin/env python3
import urllib.parse
import urllib.request
from itertools import permutations

URL = "http://localhost:8080/decrypt"
parts = ["aw2246", "french44", "pledgeor"]
specials = ["", "!", "@", "#", "$", "%", "^", "&", "*", "_", "-", "+", "=", ".", "?", "1", "123"]

def try_pw(pw):
    data = urllib.parse.urlencode({"password": pw}).encode()
    req = urllib.request.Request(URL, data=data)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read()
    except Exception as e:
        if "403" in str(e):
            return None
        raise

def generate():
    seen = set()
    # all 6 orders of the three pieces
    for order in permutations(parts, 3):
        base = "".join(order)
        # special before, after, or both
        for pre in specials:
            for post in specials:
                cand = pre + base + post
                if cand not in seen:
                    seen.add(cand)
                    yield cand
        # special between the pieces
        for mid in specials:
            if not mid:
                continue
            cand = order[0] + mid + order[1] + mid + order[2]
            if cand not in seen:
                seen.add(cand)
                yield cand
            cand = order[0] + mid + order[1] + order[2]
            if cand not in seen:
                seen.add(cand)
                yield cand
            cand = order[0] + order[1] + mid + order[2]
            if cand not in seen:
                seen.add(cand)
                yield cand

def main():
    cands = list(generate())
    print(f"[*] Trying {len(cands)} reorder + special candidates")
    for i, pw in enumerate(cands, 1):
        if i % 50 == 0:
            print(f"[*] {i}/{len(cands)} last={pw}", flush=True)
        body = try_pw(pw)
        if body:
            print("\n===== SUCCESS =====")
            print("Web password:", pw)
            open("FOUND_WEB_PASSWORD.txt", "w").write(pw + "\n")
            open("FOUND_SECRET.html", "wb").write(body)
            print(body[:600])
            return
    print("[-] No match in reorder + special set")

if __name__ == "__main__":
    main()
