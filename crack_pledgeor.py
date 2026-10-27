#!/usr/bin/env python3
import crypt
from itertools import product
from multiprocessing import Pool, cpu_count
import time

TARGET  = "$5$rounds=1000$89w0wWD1vujG.3F7$iRqfu47TO3VKhxQJfmnELcdCsyl4T5wfCAPjihdera9"
SETTING = "$5$rounds=1000$89w0wWD1vujG.3F7$"
WORDLIST = "wordlist.txt"
LAST = "pledgeor"

def check(pw):
    try:
        if crypt.crypt(pw, SETTING) == TARGET:
            return pw
    except Exception:
        pass
    return None

def main():
    with open(WORDLIST, "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]

    dump = words[3000:6000]   # leaked-password block at the top
    print(f"[*] Dump words: {len(dump)}")
    print(f"[*] Last word locked: {LAST}")
    total = len(dump) ** 2
    print(f"[*] Candidates: {total:,}")
    print(f"[*] Cores: {cpu_count()}")

    start = time.time()
    tried = 0
    found = None
    cands = (a + b + LAST for a, b in product(dump, repeat=2))

    with Pool(cpu_count()) as pool:
        for result in pool.imap_unordered(check, cands, chunksize=64):
            tried += 1
            if tried % 10000 == 0:
                elapsed = time.time() - start
                rate = tried / elapsed if elapsed else 0
                eta = (total - tried) / rate / 3600 if rate else 0
                print(f"[*] {tried:,}/{total:,} ({100*tried/total:.2f}%) "
                      f"{rate:.0f}/s ETA {eta:.1f}h", flush=True)
            if result:
                found = result
                pool.terminate()
                break

    if found:
        print("\n===== SUCCESS =====")
        print("Password:", found)
        open("FOUND_UNIX_PASSWORD.txt", "w").write(found + "\n")
    else:
        print("\n[-] No match in first 3000 dump words + pledgeor")

if __name__ == "__main__":
    main()