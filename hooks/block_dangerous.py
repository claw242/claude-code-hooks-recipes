#!/usr/bin/env python3
"""block_dangerous.py - PreToolUse hook: refuse a few obviously destructive Bash commands.

Exit code 2 blocks the tool call and sends stderr back to Claude.
Made with the help of AI by Loupe & Lettres. Python 3 standard library only. MIT licence.
"""
import json
import re
import sys

PATTERNS = (
    (r"\bgit\s+push\b.*(--force\b|\s-f\b)", "force push"),
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r", "rm -rf"),
)


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    for pattern, label in PATTERNS:
        if re.search(pattern, command):
            sys.stderr.write("Blocked by block_dangerous.py: %s. Ask the user first.\n" % label)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
