#!/usr/bin/python3 

import sys

def main():
    supress = False

    for line in sys.stdin:
        if line.startswith("!-------------------------------------------------------------------|"):
            supress = True
            continue
        elif line.startswith("|-------------------------------------------------------------------!"):
            line = "[WARNING: removed/supressed ProofPoint tag]\n"
            supress = False
        elif supress:
            continue

        # write out the line (changed or not)
        sys.stdout.write(line)

if __name__ == '__main__':
    main()
