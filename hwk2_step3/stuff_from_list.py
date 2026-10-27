#!/usr/bin/env python3
import urllib.parse
import urllib.request
import time

URL = "http://localhost:8080/decrypt"
WORDLIST = "web_candidates.txt"

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
        passwords = [line.strip() for line in f if line.strip()]

    total = len(passwords)
    print(f"[*] Loaded {total:,} candidates from {WORDLIST}")
    start = time.time()

    for i, pw in enumerate(passwords, 1):
        if i % 200 == 0:
            elapsed = time.time() - start
            rate = i / elapsed if elapsed else 0
            eta_h = (total - i) / rate / 3600 if rate else 0
            print(f"[*] {i:,}/{total:,} {rate:.1f}/s ETA {eta_h:.1f}h last={pw}", flush=True)
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
