import os
import sys

for arg in sys.argv[1:]:
    if arg[-12:-9] != 'PIA': continue
    if arg[-4:] != '.txt': continue

    with open(arg, 'r') as f:
        content = f.read()

    if content[:2] != "b'": continue

    text = eval(content)

    with open(arg, 'w') as f:
        f.write(text)
