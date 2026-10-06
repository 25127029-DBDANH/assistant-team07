# Smart Virtual Assistant

A Smart Virtual Assistant project for CSC10014 — Computational Thinking, FIT-HCMUS.

## Setup

Prerequisites: Python 3.10+, Git.

    git clone git@github.com:25127029-DBDANH/assistant-team07.git
    cd assistant-team07
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    pip install -e .

## Run

    python -m assistant "where is the library?"
    # -> Library: room B.201, open Mon-Sat 07:00-20:00.

Or run interactively:

    python -m assistant
    # Study assistant (starter). Type 'quit' to exit.

## Test

    pytest -q
    # -> 4 passed

## Project structure

    src/assistant/   - application code (the assistant itself)
    tests/           - automated tests
    docs/            - notes, logs, reports
    data/            - sample data (e.g. offices.csv)
    ui/              - user interface (added later in the course)
    scripts/         - helper scripts (e.g. check_env.py)

## Troubleshooting

- "No module named assistant" -> you forgot `pip install -e .`, or the virtual
  environment is not active (prompt should start with `(.venv)`).
- PowerShell blocks `Activate.ps1` -> run:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`