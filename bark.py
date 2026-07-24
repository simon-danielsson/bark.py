#!/usr/bin/env python3

import sys

def error(s: str):
    print(f"Error: {s} -- use 'bark.py -h' for more details")
    sys.exit(1)

def get_args():
    args = sys.argv
    if len(args) < 2:
        error("no argument was provided")
    for a in args[1:]:
        match a:
            case "-h" | "--help":
                print("help")
            case "record":
                print("record")
            case "compare":
                print("compare")
            case "history":
                print("history")
            case _:
                error(f"unknown argument '{a}'")

def main():
    get_args()

if __name__ == "__main__":
    main()
