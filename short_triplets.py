#!/usr/bin/env python3
import crypt
from itertools import product
from multiprocessing import Pool, cpu_count
import time

TARGET  = "$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"
SETTING = "$y$j9T$F/vLDJRdzzspQonYxyqKl1$"

#checks that the code is working with known hash
def check(pw):
    try:
        if crypt.crypt(pw, SETTING) == TARGET:
            return pw
    except:
        pass
    return None

def main():
    print("[*] Loading wordlist...")
    with open("wordlist.txt", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]

    # Phase 1 filter: length 3-5 only
    short = [w for w in words if 3 <= len(w) <= 5]
    print(f"[*] Total words          : {len(words):,}")
    print(f"[*] Words length 3-5     : {len(short):,}")

    total = len(short) ** 3
    print(f"[*] Triplets to try      : {total:,}")
    print(f"[*] Cores                : {cpu_count()}")
    print("[*] Starting Phase 1...\n")

    start = time.time()
    tried = 0
    found = None

    candidates = (a + b + c for a, b, c in product(short, repeat=3))

    with Pool(cpu_count()) as pool:
        for result in pool.imap_unordered(check, candidates, chunksize=512):
            tried += 1
            if tried % 200000 == 0:
                elapsed = time.time() - start
                rate = tried / elapsed
                eta_h = (total - tried) / rate / 3600 if rate > 0 else 0
                print(f"[*] {tried:,}/{total:,} ({100*tried/total:.2f}%) "
                      f"{rate:.0f}/s  ETA {eta_h:.1f}h", flush=True)

            if result:
                found = result
                pool.terminate()
                break

    if found:
        print("\n" + "="*50)
        print(f"  PASSWORD FOUND: {found}")
        print("="*50)
        open("FOUND.txt", "w").write(found + "\n")
    else:
        print("\n[-] Phase 1 finished – no match.")

if __name__ == "__main__":
    main()