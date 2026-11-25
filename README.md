# claude-code-hooks-recipes

Loupe & Lettres - created with the help of AI (créé avec l'aide de l'IA). This repository is published by an AI-assisted shop, not by a named person.

Five small, free Claude Code hooks, one per event, each a single Python 3 file with no dependency. Copy what you need.

## One-line install (the force-push and `rm -rf` guard)

```
mkdir -p .claude/hooks && curl -fsSL -o .claude/hooks/block_dangerous.py https://raw.githubusercontent.com/claw242/claude-code-hooks-recipes/main/hooks/block_dangerous.py
```

Then add the block from `hooks.example.json` (the `PreToolUse` part) to your project's Claude Code hooks configuration. Read the file before you run it: it is 25 lines.

| File | Event | What it does |
|---|---|---|
| `hooks/block_dangerous.py` | PreToolUse (Bash) | refuses `git push --force` and `rm -rf` (exit code 2) |
| `hooks/prompt_check.py` | UserPromptSubmit | blocks a prompt that contains an obvious API key or private key |
| `hooks/start_branch.py` | SessionStart | tells Claude which git branch it starts on |
| `hooks/json_check.py` | PostToolUse (Edit/Write) | feedback to Claude when a written `.json` file does not parse |
| `hooks/stop_tests.py` | Stop | asks Claude to keep working while your test command fails (once) |

## Install all five

1. Copy the five files of `hooks/` to `.claude/hooks/` in your project.
2. Merge `hooks.example.json` into your project's Claude Code hooks configuration.
3. For `stop_tests.py`, write your test command on one line in `.claude/tests-command.txt` (it runs through the shell: only write commands you trust).

## The three rules that matter

- Exit code 0 = success. On UserPromptSubmit and SessionStart, plain stdout is added to Claude's context.
- Exit code 2 is the blocking code: PreToolUse blocks the call (stderr goes to Claude), PostToolUse only gives feedback (the tool already ran), UserPromptSubmit blocks the prompt, Stop prevents Claude from stopping.
- Any other code, including 1, is a non-blocking error by default: the action still happens. A guard that exits 1 guards nothing.

Full explanation of each recipe, with the exact payloads: https://hook-recipes.atelier-4efd18.workers.dev/claude-code-hooks-recipes (source of truth for events and exit codes: https://code.claude.com/docs/en/hooks).

## Limits (read before relying on it)

Seat belts, not a sandbox: the patterns are deliberately simple and a script or an alias can hide a command. Review the code before use. Provided as is; not affiliated with Anthropic. Written with AI assistance and run against sample payloads; not audited by a third party, and not verified inside every Claude Code version.

## More

- Does your own guard hook really block what you think? Free 10-case test: https://hook-recipes.atelier-4efd18.workers.dev/test-claude-code-hook - and **Hook Proof** (9 USD), a tester that replays a corpus of safe and dangerous tool calls against your hook: https://loupeetlettres.gumroad.com/l/gvdarr
- More hook ideas beyond blocking (prompt checks, session context, post-edit checks, stop checks), explained one by one: **Hook Cookbook** (8 USD): https://loupeetlettres.gumroad.com/l/dpehuq
- Three ready-made guards in one pack (destructive commands, secret paths, force push): **Agent Hook Starter** (5 USD): https://loupeetlettres.gumroad.com/l/agent-hook-starter
- Guardrails for unattended nightly runs: **Night Shift Guardrails** (29 USD): https://loupeetlettres.gumroad.com/l/evxhuu
- A free single-file hook against force-push: https://github.com/claw242/force-push-guard-hook

The paid products are sold by Loupe & Lettres, an AI-assisted shop (https://loupeetlettres.gumroad.com/); this free repository works without them.
