import re

regex_float = re.compile("^(0|(0\.[0-9]+)|1)$")

p = input()
while p != "":
    res = regex_float.match(p)
    if res != None:
        print(res)
    p = input()