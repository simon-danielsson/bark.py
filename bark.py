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

- bark.py -

A minimal snapshot testing tool to harden the bark of your code.

Built by Simon Danielsson

Source: https://github.com/simon-danielsson/bark.py
Author: https://www.simondanielsson.se/

Requirements: Python 3.10+

"""

import sys, subprocess, os, shutil, hashlib
from dataclasses import dataclass
from pathlib import Path
from enum import StrEnum

CWD = "."
BARK_TEST = f"{CWD}/bark_test"
BARK_DIR = f"{CWD}/.bark"
HASH = f"{BARK_DIR}/hash"

_HELP_STR = """
    ./bark.py record
        * Reads a file 'bark_test' with shell commands to be executed.
        * Executes each command and saves their respective stdout/err to a file
          inside a generated directory '.bark'.

    ./bark.py compare
        * Runs the same file of shell commands again and compares their
          stdout/err to their recorded counterparts in the '.bark' directory.
        * Generates a git-style diff to preview errors in the case of a mismatch.
        * Generates a pretty table summarizing each test."""

def msg_info(s: str):
    """debug"""
    print(f"INFO:    {s}")

def msg_succ(s: str):
    """debug"""
    print(f"SUCCESS: {s}")

def msg_error(s: str):
    """debug - also quits the program with exit code 1"""
    print(f"FAILURE: {s} -- use 'bark.py -h' for more details")
    sys.exit(1)

@dataclass
class Test:
    shell_cmd: list[str]
    name: str
    id: int
    stdout: str = ""

    def shell_cmd_as_str(self):
        return " ".join(self.shell_cmd)

    def launch_cmd(self, debug_print: bool):
        """helper - cmd_record()"""
        try:
            self.stdout = subprocess.run(
                    shell=True,
                    args=self.shell_cmd_as_str(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    ).stdout
            if debug_print:
                msg_succ(f"processed: '{self.shell_cmd_as_str()}'")
        except FileNotFoundError:
            msg_error(f"file not found '{self.shell_cmd_as_str()}'")
        except subprocess.CalledProcessError as e:
            msg_error(f"failed to execute '{self.shell_cmd_as_str()}': {e}")

def read_file(file: str | Path) -> list[str]:
    try:
        f = open(file, "r").readlines()
    except OSError:
        msg_error(f"failed to open '{file}' (must be inside working dir)")
    return f

def retrieve_old_tests() -> list[Test]:
    if not os.path.exists(BARK_DIR):
        msg_error(f"dir '{BARK_DIR}' doesn't exist")

    tests = []
    for child in Path(BARK_DIR).iterdir():
        if child.is_file():
            if child.name == "hash":
                continue
            file = read_file(child)
            tests.append(
                    Test(
                        shell_cmd=[],
                        name=file[0][:-1],
                        stdout="".join(file[-1:]),
                        id=int(child.name),
                        )
                    )
    return tests

def retrieve_new_tests() -> list[Test]:
    """helper - cmd_record()"""
    f = read_file(BARK_TEST)
    tests: list[Test] = []
    for i, l in enumerate(f):
        name, command = l.split("|")
        test_cmd = command[:-1].split(" ")
        tests.append(Test(shell_cmd=test_cmd, name=name, id=i))
    return tests

def generate_hash_from_file(file: str) -> str:
    with open(file, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def _compare_hash() -> None:
    """checks if commands to be ran are the same as prev. recorded"""
    current_hash = generate_hash_from_file(BARK_TEST)
    with open(HASH, "r", encoding="utf-8") as f:
        old_hash = f.read().strip()
    if current_hash != old_hash:
        msg_error(f"'{BARK_TEST}' has changed since last recording")

def store_test_results(tests: list[Test]):
    """helper - cmd_record()"""
    if os.path.exists(BARK_DIR):
        msg_info("overwriting old snapshot...")
        shutil.rmtree(BARK_DIR)
    os.makedirs(BARK_DIR)
    for t in tests:
        with open(f"{BARK_DIR}/{t.id}", "w", encoding="utf-8") as f:
            f.write(f"{t.name}\n")
            f.write(t.stdout)
    with open(f"{HASH}", "w", encoding="utf-8") as f:
        f.write(generate_hash_from_file(BARK_TEST))

def cmd_record():
    tests = retrieve_new_tests()
    for t in tests:
        t.launch_cmd(debug_print=True)
    store_test_results(tests)
    msg_succ("a new snapshot was written successfully!")

def cmd_help():
    print(_HELP_STR[1:])

class TestStatus(StrEnum):
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"

def cmd_compare():
    new_tests = retrieve_new_tests()
    old_tests = retrieve_old_tests()

    for n, o in zip(new_tests, old_tests):
        for nl, ol in zip(n.stdout.splitlines(), o.stdout.splitlines()):
            if nl != ol:
                print("failure")

    #         # n.launch_cmd(debug_print=False)
    #         # print(f"NAME: {n.name}")
    #         # print(n.stdout)
    #
    # print("---- old tests ----")
    # for n in old_tests:
    #     print(f"NAME: {n.name}")
    #     print(n.stdout)

def main():
    args = sys.argv
    if len(args) < 2:
        msg_error("no argument was provided")
    for a in args[1:]:
        match a:
            case "-h" | "--help":
                cmd_help()
            case "record":
                cmd_record()
            case "compare":
                _compare_hash()
                cmd_compare()
            case _:
                msg_error(f"unknown argument '{a}'")

if __name__ == "__main__":
    main()
