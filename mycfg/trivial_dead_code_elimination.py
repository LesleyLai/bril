import sys
import json

from mycfg import form_blocks

def instr_used(used, instr):
    return "dest" not in instr or instr["dest"] in used

def global_dce(instrs):
    while True:
        used = set()
        for instr in instrs:
            if "args" in instr:
                used.update(instr["args"])

        new_instrs = [instr for instr in instrs if instr_used(used, instr)]
        if (len(new_instrs) == len(instrs)):
            return instrs
        instrs = new_instrs

def local_dce(block):
    last_def_index_dict = {}
    to_remove_index = set()
    for i, instr in enumerate(block):

        # check for use
        if "args" in instr:
            for arg in instr["args"]:
                last_def_index_dict.pop(arg)

        # check for def
        if "dest" in instr:
            dest = instr["dest"]
            if dest in last_def_index_dict:
                to_remove_index.add(last_def_index_dict[dest])
            last_def_index_dict[dest] = i

    result = [instr for i, instr in enumerate(block)
              if i not in to_remove_index]

    return result

def flatten(nested_list):
    return [item for sublist in nested_list for item in sublist]


def main():
    prog = json.load(sys.stdin)
    for func in prog["functions"]:
        # global dce
        instrs = func["instrs"]
        instrs = global_dce(instrs)

        # local dce
        blocks = form_blocks(instrs)
        blocks = [local_dce(block) for block in blocks]

        func["instrs"] = flatten(blocks)


    json.dump(prog, sys.stdout)

if __name__ == '__main__':
    main()
