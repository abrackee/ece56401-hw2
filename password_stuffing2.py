# tries original password but with changing the numbers

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

def candidates():
    seen = set()
    # keep stems, vary the numbers
    for n1 in range(10000):          # 0 .. 9999
        forms1 = {str(n1), f"{n1:04d}"}
        for n2 in range(100):        # 0 .. 99
            forms2 = {str(n2), f"{n2:02d}"}
            for a in forms1:
                for b in forms2:
                    pw = f"aw{a}french{b}pledgeor"
                    if pw not in seen:
                        seen.add(pw)
                        yield pw

def main():
    # unique count is a bit under 1e6 because 12 and 0012 collide etc.
    print("[*] Trying aw + [0-9999] + french + [0-99] + pledgeor")
    print("[*] This may take a while. Progress every 50 tries.")
    tried = 0
    for pw in candidates():
        tried += 1
        if tried % 50 == 0:
            print(f"[*] {tried} last={pw}", flush=True)
        body = try_pw(pw)
        if body:
            print("\n===== SUCCESS =====")
            print("Web password:", pw)
            open("FOUND_WEB_PASSWORD.txt", "w").write(pw + "\n")
            open("FOUND_SECRET.html", "wb").write(body)
            print(body[:800])
            return
    print("[-] No match. Tried", tried)

if __name__ == "__main__":
    main()