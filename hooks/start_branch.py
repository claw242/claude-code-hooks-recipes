#!/usr/bin/env python3
"""start_branch.py - SessionStart hook: tell Claude which git branch it starts on.

Plain stdout of a SessionStart hook is added to Claude's context.
Made with the help of AI by Loupe & Lettres. Python 3 standard library only. MIT licence.
"""
import subprocess
import sys


def git(*args):
    try:
        done = subprocess.run(["git"] + list(args), capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def main():
    branch = git("branch", "--show-current")
    if git("rev-parse", "--is-inside-work-tree") != "true":
        return 0
    branch = branch or "(detached HEAD)"
    state = "has uncommitted changes" if git("status", "--porcelain") else "is clean"
    print("Git branch: %s (working tree %s)." % (branch, state))
    return 0


if __name__ == "__main__":
    sys.exit(main())
