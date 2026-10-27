#!/usr/bin/env python3
import crypt
from itertools import product
from multiprocessing import Pool, cpu_count
import time

TARGET  = "$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"
SETTING = "$y$j9T$F/vLDJRdzzspQonYxyqKl1$"

def check(pw):
    try:
        if crypt.crypt(pw, SETTING) == TARGET:
            return pw
    except Exception:
        pass
    return None

def main():
    print("[*] Loading top 1000 words...")
    with open("short1000.txt", "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip()]

    print(f"[*] Words loaded: {len(words)}")
    total = len(words) ** 3
    print(f"[*] Total triplets: {total:,}")
    print(f"[*] Using {cpu_count()} cores")
    print("[*] Starting...\n")

    start = time.time()
    tried = 0
    found = None

    candidates = (a + b + c for a, b, c in product(words, repeat=3))

    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(check, candidates, chunksize=256):
            tried += 1
            if tried % 50000 == 0:
                elapsed = time.time() - start
                rate = tried / elapsed if elapsed > 0 else 0
                eta_h = (total - tried) / rate / 3600 if rate > 0 else 0
                print(f"[*] {tried:,}/{total:,} ({100*tried/total:.2f}%) "
                      f"{rate:.0f}/s  ETA {eta_h:.1f}h", flush=True)

            if result is not None:
                found = result
                pool.terminate()
                break

    if found:
        print("\n" + "="*50)
        print(f"  SUCCESS! Password is: {found}")
        print("="*50)
        with open("FOUND.txt", "w") as f:
            f.write(found + "\n")
    else:
        print("\n[-] Finished – no match in top 1000 triplets.")

if __name__ == "__main__":
    main()