#!/usr/bin/env python3
import crypt
from itertools import product
from multiprocessing import Pool, cpu_count
import time

#TARGET  = "$5$rounds=1000$89w0wWD1vujG.3F7$VKWdkoyVliKfeHaihvPYBjnfy7SbXeq2eThsVHdlmr7"
TARGET  = "$5$rounds=1000$89w0wWD1vujG.3F7$iRqfu47TO3VKhxQJfmnELcdCsyl4T5wfCAPjihdera9"
SETTING = "$5$rounds=1000$89w0wWD1vujG.3F7$"
WORDLIST = "bob_official_themed_2.txt"

def check(pw):
    try:
        if crypt.crypt(pw, SETTING) == TARGET:
            return pw
    except Exception:
        pass
    return None

def candidates(words):
    for a, b, c in product(words, repeat=3):
        yield a + b + c

def main():
    with open(WORDLIST, "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip()][:600]
    #words = ["bob", "secret", "gold"]

    print(f"[*] Words loaded from official list filter: {len(words)}")
    print(f"[*] First 15: {words[:15]}")
    total = len(words) ** 3
    print(f"[*] Triplets: {total:,}")
    print(f"[*] Cores: {cpu_count()}")
    print("[*] Starting...\n")

    start = time.time()
    tried = 0
    found = None

    with Pool(cpu_count()) as pool:
        for result in pool.imap_unordered(check, candidates(words), chunksize=64):
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
        print("\n[-] No match in this official themed 600-word triplet set.")

if __name__ == "__main__":
    main()
