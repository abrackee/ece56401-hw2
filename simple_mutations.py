#!/usr/bin/env python3
import ctypes
import ctypes.util
import sys

libcrypt = ctypes.CDLL(ctypes.util.find_library("crypt"))
libcrypt.crypt.restype = ctypes.c_char_p
libcrypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

TARGET  = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"
SETTING = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$"

def check(password):
    result = libcrypt.crypt(password.encode(), SETTING)
    if result == TARGET:
        print("\n===== PASSWORD FOUND =====")
        print(f"Password: {password}")
        print(f"Hash:     {result.decode()}")
        print("==========================")
        sys.exit(0)

print("[*] Starting mutation attack...")
tried = 0

with open("/tmp/wordlist.txt", "r", errors="ignore") as f:
    for line in f:
        base = line.strip()
        if not base or base.startswith("/data/"):
            continue

        candidates = [
            base,
            base + "1",
            base + "12",
            base + "123",
            base + "!",
            base.capitalize(),
            base.capitalize() + "!",
        ]

        for pwd in candidates:
            tried += 1
            if tried % 20000 == 0:
                print(f"[*] Tried {tried} candidates...", flush=True)
            check(pwd)

print("\n[-] Password not found with these mutations.")