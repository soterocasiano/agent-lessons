#!/usr/bin/env python3
"""Generate a lesson using the "teaching-lesson" skill via the
GitHub Copilot SDK, and save the result into the lessons/ directory.

The generated lesson teaches the reader directly (the agent acts as the
teacher) rather than producing a plan for someone else to present.

Prerequisites:
    pip install -r scripts/requirements.txt
    python -m copilot download-runtime
    copilot login   # authenticate the bundled CLI once, if not already signed in

Usage:
    python scripts/generate_lesson.py \\
        --topic "Introduction to Recursion" \\
        --audience "High school students, no prior programming experience" \\
        --depth "deep dive" \\
        --goal "Understand recursion and write a simple recursive function" \\
        --prior-knowledge "Basic Python syntax, loops"

Any input not supplied on the command line is prompted for interactively.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
import time
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import AssistantMessageData, AssistantUsageData, SessionIdleData

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = REPO_ROOT / "skills" / "teaching-lesson.md"
LESSONS_DIR = REPO_ROOT / "lessons"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate a lesson using the "teaching-lesson" '
        "skill via the GitHub Copilot SDK."
    )
    parser.add_argument("--topic", help="Subject or topic of the lesson")
    parser.add_argument(
        "--audience", help="Audience: experience level (e.g. complete beginner, some familiarity, advanced)"
    )
    parser.add_argument(
        "--depth", help="How much ground to cover (e.g. quick overview / deep dive)"
    )
    parser.add_argument(
        "--goal", help="Learning goal: what the reader should know/do by the end"
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

Use the skill above to teach the reader directly, as the teacher, with the
following inputs:

{details}

Respond with ONLY the completed lesson in markdown, following the "Output
Structure" section of the skill exactly. Do not include any preamble,
explanation, or commentary outside of the lesson itself.
"""


async def generate_lesson(prompt: str, model: str) -> tuple[str, dict[str, int | float]]:
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model=model,
        ) as session:
            result: dict[str, str] = {"content": ""}
            metrics = {
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_tokens": 0,
                "cache_write_tokens": 0,
                "reasoning_tokens": 0,
            }
            done = asyncio.Event()

            def on_event(event):
                match event.data:
                    case AssistantMessageData() as data:
                        result["content"] = data.content
                    case AssistantUsageData() as data:
                        metrics["input_tokens"] += data.input_tokens or 0
                        metrics["output_tokens"] += data.output_tokens or 0
                        metrics["cache_read_tokens"] += data.cache_read_tokens or 0
                        metrics["cache_write_tokens"] += data.cache_write_tokens or 0
                        metrics["reasoning_tokens"] += data.reasoning_tokens or 0
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            start_time = time.perf_counter()
            await session.send(prompt)
            await done.wait()
            metrics["elapsed_seconds"] = time.perf_counter() - start_time

            return result["content"], metrics


def print_metrics(metrics: dict[str, int | float]) -> None:
    total_tokens = (
        metrics["input_tokens"] + metrics["output_tokens"] + metrics["reasoning_tokens"]
    )
    print("\nMetrics:")
    print(f"  Time taken:       {metrics['elapsed_seconds']:.1f}s")
    print(f"  Input tokens:     {metrics['input_tokens']}")
    print(f"  Output tokens:    {metrics['output_tokens']}")
    if metrics["reasoning_tokens"]:
        print(f"  Reasoning tokens: {metrics['reasoning_tokens']}")
    if metrics["cache_read_tokens"] or metrics["cache_write_tokens"]:
        print(
            f"  Cache tokens:     read={metrics['cache_read_tokens']} "
            f"write={metrics['cache_write_tokens']}"
        )
    print(f"  Total tokens:     {total_tokens}")


def main() -> None:
    args = parse_args()

    if not SKILL_FILE.exists():
        sys.exit(f"Skill file not found: {SKILL_FILE}")

    skill_content = SKILL_FILE.read_text(encoding="utf-8")

    inputs = {
        "topic": prompt_if_missing(args.topic, "Subject or topic"),
        "audience": prompt_if_missing(
            args.audience, "Audience / experience level"
        ),
        "depth": prompt_if_missing(args.depth, "Depth (quick overview / deep dive)"),
        "goal": prompt_if_missing(args.goal, "Learning goal"),
        "prior_knowledge": prompt_if_missing(args.prior_knowledge, "Prior knowledge"),
    }

    prompt = build_prompt(skill_content, inputs)

    print("Generating lesson with the GitHub Copilot SDK...")
    content, metrics = asyncio.run(generate_lesson(prompt, args.model))

    if not content.strip():
        sys.exit("No content was returned by Copilot.")

    output_path = (
        Path(args.output)
        if args.output
        else LESSONS_DIR / f"lesson-{slugify(inputs['topic'])}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"Lesson written to {output_path.relative_to(REPO_ROOT)}")
    print_metrics(metrics)


if __name__ == "__main__":
    main()
