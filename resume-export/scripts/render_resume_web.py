#!/usr/bin/env python
"""Render a simple Markdown resume as a self-contained HTML preview."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


STYLE_CHOICES = ("plain", "classic-blue", "teal-ribbon", "light-blue-band")


def inline_md(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.*?)`", r"<code>\1</code>", escaped)
    return escaped


def markdown_to_resume_html(markdown: str) -> tuple[str, str]:
    title = "简历"
    parts: list[str] = []
    in_list = False
    section_open = False
    seen_section = False
    after_title = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            parts.append("    </ul>")
            in_list = False

    def close_section() -> None:
        nonlocal section_open
        if section_open:
            close_list()
            parts.append("    </section>")
            section_open = False

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if not line:
            close_list()
            continue
        if line.startswith("# "):
            close_section()
            title = line[2:].strip() or title
            parts.append(f'    <h1 class="resume-title">{inline_md(title)}</h1>')
            after_title = True
        elif line.startswith("## "):
            close_section()
            section_class = "resume-section is-first" if not seen_section else "resume-section"
            parts.append(f'    <section class="{section_class}">')
            section_open = True
            seen_section = True
            after_title = False
            parts.append('      <div class="resume-section-heading">')
            parts.append(f'        <h2 class="resume-section-title">{inline_md(line[3:].strip())}</h2>')
            parts.append("      </div>")
        elif line.startswith("### "):
            close_list()
            after_title = False
            parts.append(f'      <h3 class="resume-subtitle">{inline_md(line[4:].strip())}</h3>')
        elif line.startswith("- "):
            after_title = False
            if not in_list:
                parts.append('      <ul class="resume-list">')
                in_list = True
            parts.append(f"        <li>{inline_md(line[2:].strip())}</li>")
        elif line.startswith("> "):
            close_list()
            after_title = False
            parts.append(f'      <p class="resume-note">{inline_md(line[2:].strip())}</p>')
        else:
            close_list()
            if after_title and not section_open:
                parts.append(f'    <p class="resume-contact">{inline_md(line.strip())}</p>')
                after_title = False
            else:
                after_title = False
                parts.append(f'      <p class="resume-paragraph">{inline_md(line.strip())}</p>')

    close_section()
    return title, "\n".join(parts)


def render(markdown: str, style: str, template_dir: Path) -> str:
    title, content = markdown_to_resume_html(markdown)
    css = (template_dir / "resume.css").read_text(encoding="utf-8")
    template = (template_dir / "base.html").read_text(encoding="utf-8")
    return (
        template.replace("__TITLE__", html.escape(title))
        .replace("__STYLE__", style)
        .replace("__CSS__", css)
        .replace("__CONTENT__", content)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Markdown resume to a self-contained HTML preview.")
    parser.add_argument("--input", required=True, help="Input Markdown resume path.")
    parser.add_argument("--html", required=True, help="Output HTML preview path.")
    parser.add_argument("--style", choices=STYLE_CHOICES, default="classic-blue", help="Visual style profile.")
    parser.add_argument(
        "--template-dir",
        default=str(Path(__file__).resolve().parents[1] / "assets" / "templates" / "resume-web"),
        help="Directory containing base.html and resume.css.",
    )
    args = parser.parse_args()

    markdown = Path(args.input).read_text(encoding="utf-8")
    output = Path(args.html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(markdown, args.style, Path(args.template_dir)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
