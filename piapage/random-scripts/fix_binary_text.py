import os
import sys
import ast

for arg in sys.argv[1:]:
    if arg[-12:-9] != 'PIA': continue
    if arg[-4:] != '.txt': continue

    with open(arg, 'r', encoding='utf-8') as f:
        content = f.read()

    if content[:2] != "b'": continue

    try:
        text = ast.literal_eval(content)
    except (SyntaxError, ValueError) as exc:
        print(f"Skipping {arg}: invalid literal ({exc})", file=sys.stderr)
        continue

    if isinstance(text, bytes):
        text = text.decode('utf-8')
    elif not isinstance(text, str):
        print(f"Skipping {arg}: unexpected literal type {type(text).__name__}", file=sys.stderr)
        continue

    with open(arg, 'w', encoding='utf-8') as f:
        f.write(text)
