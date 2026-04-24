#!/usr/bin/env python
"""Export an HTML resume preview to PDF using Chrome or Edge headless printing."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


DEFAULT_BROWSER_COMMANDS = ("chrome", "chromium", "msedge")


def find_browser(explicit: str | None = None) -> str:
    candidates = []
    if explicit:
        candidates.append(explicit)
    for command in DEFAULT_BROWSER_COMMANDS:
        resolved = shutil.which(command)
        if resolved:
            candidates.append(resolved)
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise RuntimeError("No Chrome or Edge executable found. Install Chrome/Edge or pass --browser.")


def run_browser_print(browser_path: str, html_uri: str, pdf_path: Path, user_data_dir: str | None) -> subprocess.CompletedProcess:
    command = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=1000",
        f"--print-to-pdf={str(pdf_path.resolve())}",
        html_uri,
    ]
    if user_data_dir:
        command.insert(7, f"--user-data-dir={user_data_dir}")
    return subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)


def export_pdf(html_path: Path, pdf_path: Path, browser: str | None = None) -> None:
    browser_path = find_browser(browser)
    html_uri = html_path.resolve().as_uri()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    result = run_browser_print(browser_path, html_uri, pdf_path, None)
    if result.returncode != 0:
        user_data_dir = tempfile.mkdtemp(prefix="resume-pdf-")
        try:
            result = run_browser_print(browser_path, html_uri, pdf_path, user_data_dir)
        finally:
            shutil.rmtree(user_data_dir, ignore_errors=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"Browser PDF export failed with code {result.returncode}: {detail}")
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError("Browser PDF export finished but no PDF was created.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a resume HTML preview to PDF using Chrome/Edge.")
    parser.add_argument("--html", required=True, help="Input HTML preview path.")
    parser.add_argument("--pdf", required=True, help="Output PDF path.")
    parser.add_argument("--browser", help="Optional Chrome/Edge executable path.")
    args = parser.parse_args()

    export_pdf(Path(args.html), Path(args.pdf), args.browser)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
