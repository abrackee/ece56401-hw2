#!/usr/bin/env python3
import ctypes
import ctypes.util
import sys
from multiprocessing import Pool, cpu_count
import itertools

libcrypt = ctypes.CDLL(ctypes.util.find_library("crypt"))
libcrypt.crypt.restype = ctypes.c_char_p
libcrypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

TARGET  = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"
SETTING = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$"

SUFFIXES = ["", "1", "12", "123", "!", "!!", "@", "#", "$", "123!", "!@#"]

def check(password):
    try:
        result = libcrypt.crypt(password.encode(), SETTING)
        if result == TARGET:
            return password
    except Exception:
        pass
    return None

def main():
    print("[*] Loading wordlist...")
    with open("/tmp/wordlist.txt", "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]

    print(f"[*] Loaded {len(words)} base words")

    candidates = []
    for w in words:
        if len(w) > 18:
            continue
        bases = [w, w.capitalize(), w.upper()]
        for base in bases:
            for suf in SUFFIXES:
                candidates.append(base + suf)

    short = [w for w in words if 3 <= len(w) <= 5][:2000]
    for a, b in itertools.product(short, repeat=2):
        candidates.append(a + b)

    total = len(candidates)
    print(f"[*] Total candidates: {total:,}")
    print(f"[*] Using {min(4, cpu_count())} cores")
    print("[*] Starting...\n")

    tried = 0
    found = None

    with Pool(processes=min(4, cpu_count())) as pool:
        for result in pool.imap_unordered(check, candidates, chunksize=32):
            tried += 1
            if tried % 10000 == 0:
                print(f"[*] Tried {tried:,} / {total:,} ({100*tried/total:.1f}%)", flush=True)

            if result is not None:
                found = result
                pool.terminate()
                break

    if found:
        print("\n" + "="*50)
        print(f"  SUCCESS! Password is: {found}")
        print("="*50)
        with open("/tmp/FOUND_PASSWORD.txt", "w") as f:
            f.write(found + "\n")
    else:
        print("\n[-] Finished – password not found with these rules.")

if __name__ == "__main__":
    main()