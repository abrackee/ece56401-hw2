#!/usr/bin/env python3
import urllib.parse
import urllib.request

URL = "http://localhost:8080/decrypt"

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

    # Wider: aw 0-999 (and 4-digit padded), french 0-99 (and 2-digit padded)
    for n1 in range(1000):
        for n2 in range(100):
            cands.add(f"aw{n1}french{n2}pledgeor")
            cands.add(f"aw{n1:04d}french{n2:02d}pledgeor")

    # Also try the original numbers with bigger offsets
    for d in range(-100, 101):
        cands.add(f"aw{2246 + d}french44pledgeor")
        cands.add(f"aw2246french{44 + d}pledgeor")
        cands.add(f"aw{2246 + d}french{44 + d}pledgeor")

    # Drop one number
    for n in range(100):
        cands.add(f"awfrench{n}pledgeor")
        cands.add(f"aw{n}frenchpledgeor")
    cands.add("awfrenchpledgeor")

    print(f"[*] Trying {len(cands)} passwords")
    for i, pw in enumerate(sorted(cands, key=len), 1):
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
    print("[-] No match in this wider set")

if __name__ == "__main__":
    main()