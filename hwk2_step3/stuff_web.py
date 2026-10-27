#REORDERS NUMBERS


#!/usr/bin/env python3
import urllib.parse
import urllib.request
from itertools import permutations

URL = "http://localhost:8080/decrypt"
parts = ["aw2246", "french44", "pledgeor"]

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

def main():
    cands = set()
    # all orders of the three known pieces
    for a, b, c in permutations(parts, 3):
        cands.add(a + b + c)
    # pairs
    for a, b in permutations(parts, 2):
        cands.add(a + b)
    # singles
    cands.update(parts)
    # simple number mutations around the known numbers
    for n1 in range(0, 50):          # vary the 2246 side a little
        for n2 in range(0, 20):      # vary the 44 side a little
            cands.add(f"aw{n1}french{n2}pledgeor")
            cands.add(f"aw{n1:04d}french{n2:02d}pledgeor")
    # known numbers with small offsets
    for d in range(-20, 21):
        cands.add(f"aw{2246+d}french44pledgeor")
        cands.add(f"aw2246french{44+d}pledgeor")
        cands.add(f"aw{2246+d}french{44+d}pledgeor")

    print(f"[*] Trying {len(cands)} passwords")
    for i, pw in enumerate(sorted(cands, key=len), 1):
        if i % 25 == 0:
            print(f"[*] {i}/{len(cands)} last={pw}")
        body = try_pw(pw)
        if body:
            print("\n===== SUCCESS =====")
            print("Web password:", pw)
            open("FOUND_WEB_PASSWORD.txt", "w").write(pw + "\n")
            open("FOUND_SECRET.html", "wb").write(body)
            print(body[:600])
            return
    print("[-] No match in this set")

if __name__ == "__main__":
    main()