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

def generate_candidates(word):
    """Generate practical mutations for one word."""
    if not word or len(word) > 20:          # skip extremely long words
        return

    bases = [
        word,
        word.capitalize(),
        word.upper(),
    ]

    for base in bases:
        for suf in SUFFIXES:
            yield base + suf

def worker(candidate):
    return check(candidate)

def main():
    print("[*] Loading wordlist...")
    with open("/tmp/wordlist.txt", "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]

    print(f"[*] Loaded {len(words)} base words")
    print("[*] Generating candidates (this may take a minute)...")

    # Single-word mutations
    candidates = []
    for w in words:
        candidates.extend(generate_candidates(w))

    # Limited two-word combinations (only short words to keep it feasible)
    short = [w for w in words if 3 <= len(w) <= 6][:3000]   # limit size
    print(f"[*] Adding combinations from {len(short)} short words...")
    for a, b in itertools.product(short, repeat=2):
        candidates.append(a + b)
        candidates.append(a + b.capitalize())

    total = len(candidates)
    print(f"[*] Total candidates to try: {total:,}")
    print(f"[*] Using {cpu_count()} CPU cores")
    print("[*] Starting attack... (this will run for a long time)\n")

    found = None
    tried = 0

    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(worker, candidates, chunksize=64):
            tried += 1
            if tried % 50000 == 0:
                print(f"[*] Tried {tried:,} / {total:,} ({100*tried/total:.1f}%)", flush=True)

            if result is not None:
                found = result
                pool.terminate()
                break

    if found:
        print("\n" + "="*40)
        print(f"  PASSWORD FOUND: {found}")
        print("="*40)
        with open("/tmp/FOUND_PASSWORD.txt", "w") as f:
            f.write(found + "\n")
    else:
        print("\n[-] Finished – password not found with these rules.")

if __name__ == "__main__":
    main()
