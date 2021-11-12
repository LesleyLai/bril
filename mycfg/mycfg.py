import sys
import json
from collections import OrderedDict

TERMINATORS = ["jmp", "br", "ret"]

def form_blocks(instrs):
    cur_block = []
    for instr in instrs:
        if "op" in instr: # instruction
            cur_block.append(instr)
            if instr["op"] in TERMINATORS:
                if cur_block:
                    yield cur_block
                cur_block = []

        else:             # a label
            if cur_block:
                yield cur_block
            cur_block = [instr]

    yield cur_block

def associate_label_to_blocks(blocks):
    result = OrderedDict()
    for block in blocks:
        if "label" in block[0]:
            name = block[0]["label"]
            block = block[1:]
        else:
            name = f'B{len(result)}'
        result[name] = block
    return result

def form_cfg(label2block: OrderedDict):
    cfg = {}
    for i, (label, block) in enumerate(label2block.items()):
        last = block[-1]
        if "labels" in last:  # jmp or br
            successors = last["labels"]
        elif last["op"] == "ret":
            successors = []
        else:
            if (i < len(label2block) - 1):
                successors = [list(label2block.keys())[i + 1]]
            else:
                successors = []
        cfg[label] = successors
    return cfg

def main():
    prog = json.load(sys.stdin)
    for func in prog["functions"]:
        blocks = form_blocks(func["instrs"])
        label2block = associate_label_to_blocks(blocks)
        for label, block in label2block.items():
            print(f"{label}:\n  {block}")
        cfg = form_cfg(label2block)
        print(cfg)



if __name__ == '__main__':
    main()
