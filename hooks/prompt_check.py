#!/usr/bin/env python3
"""prompt_check.py - UserPromptSubmit hook: block a prompt that contains an obvious credential.

Printing {"decision": "block", "reason": ...} and exiting 0 blocks the prompt. The credential is never echoed back.
Simple patterns only: a seat belt, not a scanner. Made with the help of AI by Loupe & Lettres. Python 3 standard library only. MIT licence.
"""
import json
import re
import sys

# Patterns are assembled from pieces so this file itself holds no credential-looking text.
PATTERNS = (
    ("an API key that starts with sk-", re.compile("s" + "k-[A-Za-z0-9_-]{20,}")),
    ("an AWS access key id", re.compile("AK" + "IA[0-9A-Z]{16}")),
    ("a private key block", re.compile("-{5}BEGIN [A-Z ]*PRIVATE " + "KEY-{5}")),
    ("a GitHub token", re.compile("gh[pousr]_[A-Za-z0-9]{30,}")),
)


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    prompt = payload.get("prompt") if isinstance(payload, dict) else None
    if not isinstance(prompt, str):
        return 0
    for label, pattern in PATTERNS:
        if pattern.search(prompt):
            print(json.dumps({"decision": "block", "reason": "Prompt blocked: it looks like it contains %s. Remove it and send again." % label}))
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
