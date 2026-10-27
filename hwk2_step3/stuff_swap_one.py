#!/usr/bin/env python3
import urllib.parse
import urllib.request
import time

URL = "http://localhost:8080/decrypt"
WORDLIST = "wordlist.txt"

FIXED = ["aw2246", "french44", "pledgeor"]

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
    with open(WORDLIST, "r", errors="ignore") as f:
        dump = [w.strip() for w in f if w.strip() and not w.startswith("/data/")][:300000]

    cands = []
    seen = set()

    def add(pw):
        if pw and pw not in seen:
            seen.add(pw)
            cands.append(pw)

    # replace one slot at a time with a dump word, keep the other two
    for w in dump:
        add(w + FIXED[1] + FIXED[2])          # X + french44 + pledgeor
        add(FIXED[0] + w + FIXED[2])          # aw2246 + X + pledgeor
        add(FIXED[0] + FIXED[1] + w)          # aw2246 + french44 + X
        add(w + FIXED[2])                     # X + pledgeor
        add(FIXED[0] + w)                     # aw2246 + X

    print(f"[*] Dump words used: {len(dump)}")
    print(f"[*] Candidates: {len(cands):,}")
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
