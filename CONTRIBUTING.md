# Contributing to Smart Virtual Assistant

Thank you for contributing! Please read the guidelines below before
submitting changes.

## Getting started

1. Clone the repository and set up the virtual environment (see
   [README.md](README.md#setup)).
2. Create a feature branch from `main` — never commit directly to `main`.
3. Run `pytest -q` before pushing to make sure nothing is broken.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes:

| Prefix  | When to use               |
| ------- | ------------------------- |
| `feat`  | New feature               |
| `fix`   | Bug fix                   |
| `docs`  | Documentation only        |
| `test`  | Adding / updating tests   |
| `chore` | Maintenance / tooling     |

End every commit message with `(refs #<issue-number>)`.

## Pull requests

- Fill in the PR template completely (What, Why, How tested, AI use).
- Reference the issue with `Closes #<issue-number>` in the PR body.
- Wait for at least one approving review before merging.

## Secrets

> **Never commit passwords, API keys, tokens, or any other secret to the
> repository.**

| Do                                    | Don't                              |
| ------------------------------------- | ---------------------------------- |
| Store secrets in a local `.env` file  | Hard-code secrets in source files  |
| Copy `.env.example` → `.env`          | Commit `.env` to version control   |
| Use environment variables at runtime  | Share secrets in issues or PRs     |
| Rotate a key immediately if leaked    | Ignore `.gitignore` rules          |

### How to manage environment variables

1. Copy the template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and replace the placeholder values with your real keys.
3. Access variables in Python:
   ```python
   import os
   api_key = os.environ.get("OPENAI_API_KEY")
   ```
4. The `.gitignore` already contains rules to ignore `.env` and `.env.*`
   while keeping `.env.example` tracked.

### What to do if a secret is leaked

1. **Rotate / revoke** the compromised key immediately on the provider's
   dashboard.
2. Remove the secret from git history (ask a maintainer for help with
   `git filter-repo` or BFG Repo-Cleaner).
3. Force-push the cleaned history and notify the team.

## Definition of Done

See [DEFINITION_OF_DONE.md](DEFINITION_OF_DONE.md) for the full checklist
every task must satisfy before it can be considered complete.
