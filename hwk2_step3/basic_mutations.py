#!/usr/bin/env python3
import ctypes, ctypes.util

WORDLIST = "/tmp/wordlist.txt"
TARGET = "$5$rounds=1000$89w0wWD1vujG.3F7$iRqfu47TO3VKhxQJfmnELcdCsyl4T5wfCAPjihdera9"
SETTING = TARGET.rsplit("$", 1)[0] + "$"

lib = ctypes.CDLL(ctypes.util.find_library("crypt"))
lib.crypt.restype = ctypes.c_char_p

def check(pw):
    try:
        r = lib.crypt(pw.encode(), SETTING.encode())
        return r and r.decode() == TARGET
    except Exception:
        return False

def main():
    with open(WORDLIST, errors="ignore") as f:
        words = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]

    count = 0
    # example mutation set that was being tried
    for w1 in words[:2000]:
        for w2 in words[:2000]:
            for cand in (w1 + w2, w1 + w2 + "pledgeor", w2 + w1):
                count += 1
                if count % 100000 == 0:
                    print(f"Tried {count} candidates...")
                if check(cand):
                    print("FOUND", cand)
                    return
    print("Password not found with these mutations.")

if __name__ == "__main__":
    main()