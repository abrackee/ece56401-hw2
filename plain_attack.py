#!/usr/bin/env python3
import ctypes
import ctypes.util
import sys

libcrypt = ctypes.CDLL(ctypes.util.find_library("crypt"))
libcrypt.crypt.restype = ctypes.c_char_p
libcrypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

TARGET = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"
SETTING = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$"

wordlist = "/tmp/wordlist.txt"

print(f"[*] Loading wordlist: {wordlist}")
print(f"[*] Target hash: {TARGET.decode()}")
print("[*] Starting attack...\n")

tried = 0
with open(wordlist, "r", errors="ignore") as f:
    for line in f:
        password = line.strip()
        if not password or password.startswith("/data/"):
            continue

        tried += 1
        if tried % 10000 == 0:
            print(f"[*] Tried {tried} passwords...", flush=True)

        result = libcrypt.crypt(password.encode(), SETTING)
        if result == TARGET:
            print("\n===== PASSWORD FOUND =====")
            print(f"Password: {password}")
            print(f"Hash:     {result.decode()}")
            print("==========================")
            sys.exit(0)

print("\n[-] Password not found in the wordlist.")