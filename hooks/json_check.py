#!/usr/bin/env python3
"""json_check.py - PostToolUse hook: after Claude writes a .json file, it must parse.

Exit code 2 shows stderr to Claude (the write already happened, so this is feedback, not an undo).
Made with the help of AI by Loupe & Lettres. Python 3 standard library only. MIT licence.
"""
import json
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".json"):
        return 0
    try:
        with open(path, encoding="utf-8") as handle:
            json.load(handle)
    except OSError:
        return 0
    except ValueError as error:
        sys.stderr.write("%s is not valid JSON: %s. Fix it.\n" % (path, error))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
