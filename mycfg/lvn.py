import sys
import json

from mycfg import form_blocks


def main():
    prog = json.load(sys.stdin)
    for func in prog["functions"]:
        instrs = func["instrs"]
        blocks = form_blocks(instrs)



    json.dump(prog, sys.stdout)

if __name__ == '__main__':
    main()
