#!/usr/bin/env python3
import crypt
from itertools import product
from multiprocessing import Pool, cpu_count
import time

TARGET  = "$5$rounds=1000$89w0wWD1vujG.3F7$iRqfu47TO3VKhxQJfmnELcdCsyl4T5wfCAPjihdera9"
SETTING = "$5$rounds=1000$89w0wWD1vujG.3F7$"
WORDLIST = "wordlist.txt"
LASTS = ["pledgeor", "Pledgeor"]

THEME = [
    "bob","pirate","hacker","hack","money","gold","secret","password","shadow",
    "dragon","winter","wolf","king","queen","captain","ship","island","radio",
    "newyork","yankees","black","pearl","sparrow","treasure","chest","bank",
    "cash","steal","thief","knight","wizard","magic","iron","fire","ice",
    "crown","master","root","admin","login","key","lock","vault","flag",
    "hidden","video","music","song","station","computer","internet","system",
    "security","access","test","bond007","iceman","phantom","ninja","roger",
    "skull","rum","boat","cannon","port","harbor","storm","sea","ocean",
    "sail","wave","loot","rich","dollar","silver","diamond","ruby","jewel",
    "coin","broadway","brooklyn","hockey","qwerty","letmein","welcome",
    "change","changeme","guest","user","pass","passwd","hunter","ranger",
]

def check(pw):
    try:
        if crypt.crypt(pw, SETTING) == TARGET:
            return pw
    except Exception:
        pass
    return None

def uniq(seq):
    out, seen = [], set()
    for w in seq:
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out

def main():
    with open(WORDLIST, "r", errors="ignore") as f:
        official = [w.strip() for w in f if w.strip() and not w.startswith("/data/")]
    official_l = {w.lower(): w for w in official}

    dump = official[:2500]
    dump_vars = uniq(dump + [w.lower() for w in dump if w.lower() in official_l])

    theme = []
    for t in THEME:
        if t in official_l:
            theme.append(official_l[t])
        if t.lower() in official_l:
            theme.append(official_l[t.lower()])
    theme = uniq(theme)

    cands = []
    for last in LASTS:
        for a, b in product(dump_vars, theme):
            cands.append(a + b + last)
            cands.append(b + a + last)
        # also two short dump words + pledgeor, but only first 400
        small = dump_vars[:400]
        for a, b in product(small, repeat=2):
            cands.append(a + b + last)

    cands = uniq(cands)
    total = len(cands)
    print(f"[*] Dump vars: {len(dump_vars)}")
    print(f"[*] Theme words: {len(theme)}")
    print(f"[*] Candidates: {total:,}")
    print(f"[*] Cores: {cpu_count()}")

    start = time.time()
    tried = 0
    found = None
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
        print("\n[-] No match in dump+theme+pledgeor set")

if __name__ == "__main__":
    main()