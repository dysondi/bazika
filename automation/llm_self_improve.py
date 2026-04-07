#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TARGETS = ["README.md", "SOUL.md", "IDENTITY.md", "USER.md"]

SYSTEM_PROMPT = """You are a careful self-improvement agent for an OpenClaw Telegram assistant repository.
Your goal is to make exactly one small, useful improvement to one of these files only:
- README.md
- SOUL.md
- IDENTITY.md
- USER.md

Rules:
- Keep the repo's Ukrainian voice and style.
- Make one tiny improvement only: clarity, consistency, role definition, examples, or wording.
- Do not change more than one file.
- Do not invent new capabilities.
- Return strict JSON only.
Schema:
{
  \"target_file\": \"README.md|SOUL.md|IDENTITY.md|USER.md\",
  \"title\": \"short PR title\",
  \"commit_message\": \"short commit message\",
  \"rationale\": \"why this change helps\",
  \"content\": \"full replacement file content\"
}
"""


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def changed_line_count() -> int:
    result = subprocess.run(
        ["git", "diff", "--numstat"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    total = 0
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            total += int(parts[0]) + int(parts[1])
    return total


def call_openai(payload: dict) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    model = os.getenv("OPENAI_MODEL", "gpt-5.4")
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
        },
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()
    text = "".join(
        item.get("text", "")
        for output in data.get("output", [])
        for item in output.get("content", [])
        if item.get("type") == "output_text"
    )
    if not text:
        raise SystemExit("OpenAI returned no output_text")
    return json.loads(text)


def main() -> int:
    payload = {
        "repository": git("remote", "get-url", "origin"),
        "files": {name: (ROOT / name).read_text() for name in ALLOWED_TARGETS if (ROOT / name).exists()},
        "status": git("status", "--short"),
    }
    suggestion = call_openai(payload)
    target = suggestion["target_file"]
    if target not in ALLOWED_TARGETS:
        raise SystemExit(f"Target not allowed: {target}")

    (ROOT / target).write_text(suggestion["content"])

    max_changed_lines = int(os.getenv("SELF_IMPROVEMENT_MAX_CHANGED_LINES", "120"))
    if changed_line_count() > max_changed_lines:
        raise SystemExit("Generated change is too large")

    artifact_path = ROOT / "automation" / "last_improvement.json"
    artifact_path.write_text(json.dumps(suggestion, indent=2, ensure_ascii=False))
    print(json.dumps(suggestion, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
