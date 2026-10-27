#!/usr/bin/env python3
import ctypes
import ctypes.util

WORDLIST = "/tmp/wordlist.txt"
TARGET = "$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"
SETTING = "$y$j9T$F/vLDJRdzzspQonYxyqKl1$"

lib = ctypes.util.find_library("crypt")
libcrypt = ctypes.CDLL(lib)
libcrypt.crypt.restype = ctypes.c_char_p

def check(pw):
    try:
        result = libcrypt.crypt(pw.encode(), SETTING.encode())
        if result and result.decode() == TARGET:
            return True
    except Exception:
        pass
    return False

def main():
    with open(WORDLIST, "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]

    for i, pw in enumerate(words, 1):
        if i % 10000 == 0:
            print(f"[*] Tried {i} passwords...")
        if check(pw):
            print(f"[+] Found: {pw}")
            return
    print("[-] Password not found in the wordlist.")

if __name__ == "__main__":
    main()