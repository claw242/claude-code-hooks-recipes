#!/usr/bin/env python3
"""stop_tests.py - Stop hook: if your test command fails, ask Claude to keep working (once).

Put your test command on one line in .claude/tests-command.txt. It is run through the shell: only write commands you trust.
Made with the help of AI by Loupe & Lettres. Python 3 standard library only. MIT licence.
"""
import json
import os
import subprocess
import sys


TIMEOUT = 300  # seconds


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if payload.get("stop_hook_active"):
        return 0  # already continuing because of this hook: never block twice, no endless loop
    root = payload.get("cwd") or os.getcwd()
    try:
        with open(os.path.join(root, ".claude", "tests-command.txt"), encoding="utf-8") as handle:
            command = handle.read().strip()
    except OSError:
        return 0
    if not command:
        return 0
    try:
        done = subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print(json.dumps({"decision": "block", "reason": "The tests did not finish within %d seconds. Check them before stopping." % TIMEOUT}))
        return 0
    if done.returncode != 0:
        tail = (done.stdout + done.stderr)[-1500:]
        print(json.dumps({"decision": "block", "reason": "The tests fail. Fix them before stopping.\n" + tail}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
