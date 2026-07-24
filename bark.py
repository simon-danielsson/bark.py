#!/usr/bin/env python3

# Copyright © 2026 Simon Danielsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files, to deal in the Software
# without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Requirements: Python 3.10+

- bark.py -
Minimal snapshot testing tool

Built by Simon Danielsson

https://github.com/simon-danielsson/bark.py
https://www.simondanielsson.se/

"""

import sys

HELP_STR = """
    ./bark.py record
        * Reads a file 'bark_test' with shell commands to be executed.
        * Executes each command and saves their respective stdout to a file
          inside a generated directory '.bark'.

    ./bark.py compare
        * Runs the same file of shell commands again and compares their stdout
          to the previously recorded counterparts in the '.bark' directory.
        * Generates a git-style diff to preview errors in the case of a mismatch.
        * Generates a pretty table summarizing each test.

    ./bark.py history
        * Display history of previous test results.
        * Generates a pretty table summarizing each test."""

def cmd_help():
    print(HELP_STR[1:])

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
                cmd_help()
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
