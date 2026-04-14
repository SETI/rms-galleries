import os
import sys
import ast

for arg in sys.argv[1:]:
    if arg[-12:-9] != 'PIA': continue
    if arg[-4:] != '.txt': continue

    with open(arg, 'r', encoding='utf-8') as f:
        content = f.read()

    if content[:2] != "b'": continue

    text = ast.literal_eval(content)

    with open(arg, 'w', encoding='utf-8') as f:
        f.write(text)
