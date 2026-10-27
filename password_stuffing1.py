import urllib.parse, urllib.request, itertools

url = "http://localhost:8080/decrypt"
parts = ["aw2246", "french44", "pledgeor"]
extras = ["bob", "secret", "password", "pirate"]

cands = set(parts)
for a,b in itertools.permutations(parts, 2):
    cands.add(a+b)
for a,b,c in itertools.permutations(parts, 3):
    cands.add(a+b+c)
for e in extras:
    for p in parts:
        cands.add(e+p); cands.add(p+e)

print("trying", len(cands), "passwords")
for pw in sorted(cands, key=len):
    data = urllib.parse.urlencode({"password": pw}).encode()
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            body = r.read()
            print("SUCCESS", pw)
            open("FOUND_WEB_PASSWORD.txt","w").write(pw+"\n")
            open("FOUND_SECRET.html","wb").write(body)
            print(body[:500])
            break
    except Exception as e:
        if "403" not in str(e):
            print("error", pw, e)
else:
    print("no match in this small set")
