#!/usr/bin/env python3
"""Generate a lesson plan using the "teaching-lesson-plan" skill via the
GitHub Copilot SDK, and save the result into the lessons/ directory.

Prerequisites:
    pip install -r scripts/requirements.txt
    python -m copilot download-runtime
    copilot login   # authenticate the bundled CLI once, if not already signed in

Usage:
    python scripts/generate_lesson.py \\
        --topic "Introduction to Recursion" \\
        --audience "High school students, no prior programming experience" \\
        --duration 60 \\
        --setting classroom \\
        --goal "Understand recursion and write a simple recursive function" \\
        --prior-knowledge "Basic Python syntax, loops"

Any input not supplied on the command line is prompted for interactively.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData, SessionIdleData

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = REPO_ROOT / "skills" / "teaching-lesson-plan.md"
LESSONS_DIR = REPO_ROOT / "lessons"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate a lesson plan using the "teaching-lesson-plan" '
        "skill via the GitHub Copilot SDK."
    )
    parser.add_argument("--topic", help="Subject or topic of the lesson")
    parser.add_argument(
        "--audience", help="Audience: age group, experience level, group size"
    )
    parser.add_argument("--duration", help="Session length in minutes (e.g. 60)")
    parser.add_argument(
        "--setting",
        help="Setting: classroom / workshop / online / corporate training / one-to-one",
    )
    parser.add_argument(
        "--goal", help="Learning goal: what participants should know/do by the end"
    )
    parser.add_argument(
        "--prior-knowledge",
        dest="prior_knowledge",
        help="What can be assumed the audience already knows",
    )
    parser.add_argument(
        "--model", default="claude-sonnet-5", help="Copilot model to use (default: claude-sonnet-5)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: lessons/lesson-<topic-slug>.md)",
    )
    return parser.parse_args()


def prompt_if_missing(value: str | None, prompt_text: str) -> str:
    if value:
        return value
    response = input(f"{prompt_text}: ").strip()
    while not response:
        response = input(f"{prompt_text}: ").strip()
    return response


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "lesson"


def build_prompt(skill_content: str, inputs: dict[str, str]) -> str:
    details = "\n".join(
        f"- **{key.replace('_', ' ').title()}**: {value}" for key, value in inputs.items()
    )
    return f"""{skill_content}

---

Use the skill above to design a complete lesson plan with the following inputs:

{details}

Respond with ONLY the completed lesson plan in markdown, following the "Output
Structure" section of the skill exactly. Do not include any preamble,
explanation, or commentary outside of the lesson plan itself.
"""


async def generate_lesson(prompt: str, model: str) -> str:
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model=model,
        ) as session:
            result: dict[str, str] = {"content": ""}
            done = asyncio.Event()

            def on_event(event):
                match event.data:
                    case AssistantMessageData() as data:
                        result["content"] = data.content
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(prompt)
            await done.wait()

            return result["content"]


def main() -> None:
    args = parse_args()

    if not SKILL_FILE.exists():
        sys.exit(f"Skill file not found: {SKILL_FILE}")

    skill_content = SKILL_FILE.read_text(encoding="utf-8")

    inputs = {
        "topic": prompt_if_missing(args.topic, "Subject or topic"),
        "audience": prompt_if_missing(
            args.audience, "Audience (age group, experience level, group size)"
        ),
        "duration": prompt_if_missing(args.duration, "Session length (minutes)"),
        "setting": prompt_if_missing(
            args.setting,
            "Setting (classroom / workshop / online / corporate training / one-to-one)",
        ),
        "goal": prompt_if_missing(args.goal, "Learning goal"),
        "prior_knowledge": prompt_if_missing(args.prior_knowledge, "Prior knowledge"),
    }

    prompt = build_prompt(skill_content, inputs)

    print("Generating lesson plan with the GitHub Copilot SDK...")
    content = asyncio.run(generate_lesson(prompt, args.model))

    if not content.strip():
        sys.exit("No content was returned by Copilot.")

    output_path = (
        Path(args.output)
        if args.output
        else LESSONS_DIR / f"lesson-{slugify(inputs['topic'])}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"Lesson plan written to {output_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
