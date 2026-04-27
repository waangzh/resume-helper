#!/usr/bin/env python
"""Render a simple Markdown resume as a self-contained HTML preview."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


STYLE_CHOICES = (
    "plain",
    "classic-blue",
    "teal-ribbon",
    "light-blue-band",
    "emerald-clean",
    "burgundy-formal",
    "graphite-amber",
    "minimal-gray",
)


def inline_md(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.*?)`", r"<code>\1</code>", escaped)
    return escaped


def contact_items(line: str) -> list[str]:
    return [item.strip() for item in re.split(r"\s*(?:\||\t| {2,})\s*", line) if item.strip()]


def split_label_value(text: str) -> tuple[str, str] | None:
    for separator in ("\uff1a", ":"):
        if separator in text:
            label, value = text.split(separator, 1)
            label = label.strip().strip("*").strip()
            value = value.strip().strip("*").strip()
            if label and value:
                return label, value
    return None


def strip_wrapping_bold(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("**") and stripped.endswith("**") and len(stripped) >= 4:
        return stripped[2:-2].strip()
    return stripped


def display_contact_label(label: str) -> str:
    compact = re.sub(r"\s+", "", label)
    if len(compact) == 2:
        return f"{compact[0]}    {compact[1]}："
    return f"{compact}："


def contact_icon(label: str) -> str:
    compact = re.sub(r"\s+", "", label)
    icons = {
        "年龄": "◉",
        "籍贯": "◆",
        "电话": "☎",
        "性别": "♂",
        "工作年限": "▣",
        "邮箱": "✉",
    }
    return icons.get(compact, "•")


def intent_html(items: list[str]) -> str:
    first = split_label_value(items[0])
    if first:
        label, value = first
        values = [value, *items[1:]]
        label_html = f"<strong>{inline_md(label)}：</strong>"
    else:
        values = items
        label_html = ""

    content: list[str] = ['    <p class="resume-intent">', f"      {label_html}"]
    for index, value in enumerate(values):
        if index:
            content.append('<span class="resume-intent-separator">|</span>')
        content.append(f"<span>{inline_md(value)}</span>")
    content.append("    </p>")
    return "".join(content)


def contact_item_html(item: str) -> str:
    split = split_label_value(item)
    if split:
        label, value = split
        return (
            '<span class="resume-contact-item">'
            f'<span class="resume-contact-icon" aria-hidden="true">{contact_icon(label)}</span>'
            f'<span class="resume-contact-label">{inline_md(display_contact_label(label))}</span>'
            f'<span class="resume-contact-value">{inline_md(value)}</span>'
            "</span>"
        )
    return f'<span class="resume-contact-item">{inline_md(item)}</span>'


def is_education_section(title: str) -> bool:
    return "教育" in title


def is_award_section(title: str) -> bool:
    return "竞赛" in title or "奖项" in title


def is_campus_section(title: str) -> bool:
    return "校园" in title


def is_practice_section(title: str) -> bool:
    return "社会" in title or "实践" in title


def is_skill_cert_section(title: str) -> bool:
    return "技能" in title and "证书" in title


def award_item_html(line: str) -> str:
    """渲染竞赛奖项为左-中-右布局，全部加粗"""
    items = contact_items(line)
    if len(items) >= 3:
        name, level, period = items[0], items[1], items[2]
    elif len(items) == 2:
        name, level, period = items[0], "", items[1]
    else:
        name, level, period = line, "", ""

    if level:
        return (
            '<div class="resume-award-item">'
            f'<strong class="resume-award-name">{inline_md(name)}</strong>'
            f'<strong class="resume-award-level">{inline_md(level)}</strong>'
            f'<strong class="resume-award-period">{inline_md(period)}</strong>'
            "</div>"
        )
    else:
        return (
            '<div class="resume-award-item">'
            f'<strong class="resume-award-name">{inline_md(name)}</strong>'
            f'<strong class="resume-award-period">{inline_md(period)}</strong>'
            "</div>"
        )


def parse_project_title(line: str) -> tuple[str, str, str]:
    """解析项目标题，返回 (名称, 中间字段, 时间)"""
    items = contact_items(line)
    if len(items) >= 3:
        # 格式：项目名  中间字段  时间
        return items[0], items[1], items[2]
    elif len(items) == 2:
        # 格式：项目名  时间
        return items[0], "", items[1]
    else:
        return line, "", ""


def project_title_html(line: str) -> str:
    """渲染项目标题为左-中-右布局"""
    name, middle, period = parse_project_title(line)
    if middle:
        return (
            '      <div class="resume-project-title">'
            f'<span class="resume-project-name">{inline_md(name)}</span>'
            f'<span class="resume-project-middle">{inline_md(middle)}</span>'
            f'<span class="resume-project-period">{inline_md(period)}</span>'
            "</div>"
        )
    else:
        return (
            '      <div class="resume-project-title">'
            f'<span class="resume-project-name">{inline_md(name)}</span>'
            f'<span class="resume-project-period">{inline_md(period)}</span>'
            "</div>"
        )


def education_summary_html(line: str) -> str:
    items = contact_items(line)
    if len(items) >= 4:
        school, major, degree, period = [strip_wrapping_bold(item) for item in items[:4]]
        right = f"{major}（{degree}）"
        cells = (period, school, right)
    elif len(items) >= 3:
        cells = tuple(strip_wrapping_bold(item) for item in items[:3])
    else:
        cells = (line.strip(), "", "")
    return (
        '      <div class="resume-education-summary">'
        f'<strong>{inline_md(cells[0])}</strong>'
        f'<strong>{inline_md(cells[1])}</strong>'
        f'<strong>{inline_md(cells[2])}</strong>'
        "</div>"
    )


def education_detail_html(line: str, class_name: str) -> str:
    text = line.strip()
    split = split_label_value(text)
    if split:
        label, value = split
        return (
            f'      <p class="resume-education-detail {class_name}">'
            f'<strong>{inline_md(label)}：</strong> {inline_md(value)}'
            "</p>"
        )
    return f'      <p class="resume-education-detail {class_name}">{inline_md(text)}</p>'


def markdown_to_resume_html(markdown: str) -> tuple[str, str]:
    title = "简历"
    parts: list[str] = []
    in_list = False
    section_open = False
    profile_open = False
    seen_section = False
    after_title = False
    contact_open = False
    current_section = ""
    education_line_count = 0
    intent_written = False

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

    def close_profile() -> None:
        nonlocal profile_open
        if profile_open:
            close_contact()
            parts.append("      </div>")
            parts.append("    </header>")
            profile_open = False

    def close_contact() -> None:
        nonlocal contact_open
        if contact_open:
            parts.append("      </div>")
            contact_open = False

    def append_contact(line: str) -> None:
        nonlocal contact_open, intent_written
        items = contact_items(line)
        if not items:
            return
        first = split_label_value(items[0])
        if first and first[0] == "求职意向" and not intent_written:
            close_contact()
            parts.append(intent_html(items).replace("    <p", "      <p", 1))
            intent_written = True
            return
        if not contact_open:
            parts.append('      <div class="resume-contact">')
            contact_open = True
        for item in items:
            parts.append(f"        {contact_item_html(item)}")

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if not line:
            close_list()
            continue
        if line.startswith("# "):
            close_profile()
            close_contact()
            close_section()
            title = line[2:].strip() or title
            parts.append('    <header class="resume-profile">')
            parts.append('      <aside class="resume-photo" id="resume-photo" aria-label="简历照片" contenteditable="false"></aside>')
            parts.append('      <div class="resume-profile-main">')
            parts.append(f'        <h1 class="resume-title">{inline_md(title)}</h1>')
            profile_open = True
            after_title = True
        elif line.startswith("## "):
            close_profile()
            close_contact()
            close_section()
            current_section = line[3:].strip()
            education_line_count = 0
            section_class = "resume-section is-first" if not seen_section else "resume-section"
            parts.append(f'    <section class="{section_class}">')
            section_open = True
            seen_section = True
            after_title = False
            parts.append('      <div class="resume-section-heading">')
            parts.append(f'        <h2 class="resume-section-title">{inline_md(current_section)}</h2>')
            parts.append("      </div>")
        elif line.startswith("### "):
            close_list()
            after_title = False
            title_text = line[4:].strip()
            # 校园经历、社会实践使用项目标题格式
            if is_campus_section(current_section) or is_practice_section(current_section):
                parts.append(project_title_html(title_text))
            else:
                parts.append(project_title_html(title_text))
        elif line.startswith("- "):
            after_title = False
            # 竞赛奖项部分使用特殊布局
            if is_award_section(current_section):
                close_list()
                parts.append(award_item_html(line[2:].strip()))
            else:
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
                append_contact(line.strip())
            else:
                after_title = False
                if is_education_section(current_section):
                    education_line_count += 1
                    clean_line = line.strip()
                    clean_probe = clean_line.lstrip("*")
                    if education_line_count == 1:
                        parts.append(education_summary_html(clean_line))
                    elif clean_probe.startswith("专业成绩") or clean_probe.startswith("成绩"):
                        parts.append(education_detail_html(clean_line, "is-score"))
                    elif clean_probe.startswith("主修课程") or clean_probe.startswith("相关课程"):
                        parts.append(education_detail_html(clean_line, "is-courses"))
                    else:
                        parts.append(f'      <p class="resume-paragraph">{inline_md(clean_line)}</p>')
                else:
                    parts.append(f'      <p class="resume-paragraph">{inline_md(line.strip())}</p>')

    close_profile()
    close_contact()
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
