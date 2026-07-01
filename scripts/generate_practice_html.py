#!/usr/bin/env python3
"""Convert a Markdown tutor report into a simple standalone HTML practice page."""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

REPORT_DIR = Path("practice/reports")
OUT_DIR = Path("outputs/html")


def newest_report() -> Path:
    reports = sorted(REPORT_DIR.glob("session_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not reports:
        raise FileNotFoundError("No reports found under practice/reports")
    return reports[0]


def basic_markdown_to_html(md: str) -> str:
    # Preserve existing <details> blocks while rendering common Markdown lines.
    lines = []
    in_code = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if not in_code:
                in_code = True
                lines.append("<pre><code>")
            else:
                in_code = False
                lines.append("</code></pre>")
            continue
        if in_code:
            lines.append(html.escape(line))
            continue
        if line.startswith("# "):
            lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            lines.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            lines.append(f"<p class='bullet'>• {html.escape(line[2:])}</p>")
        elif line.startswith("| "):
            lines.append(f"<pre class='table'>{html.escape(line)}</pre>")
        elif line.startswith("<details") or line.startswith("</details>") or line.startswith("<summary>") or line.startswith("</summary>"):
            lines.append(line)
        elif line:
            safe = html.escape(line)
            safe = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", safe)
            lines.append(f"<p>{safe}</p>")
        else:
            lines.append("")
    return "\n".join(lines)


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.55; max-width: 980px; margin: 32px auto; padding: 0 18px; color: #1f2937; }}
    h1, h2, h3 {{ color: #111827; }}
    h2 {{ border-top: 1px solid #e5e7eb; padding-top: 24px; margin-top: 32px; }}
    details {{ margin: 14px 0; padding: 12px 14px; border: 1px solid #d1d5db; border-radius: 10px; background: #f9fafb; }}
    summary {{ cursor: pointer; font-weight: 700; }}
    pre {{ overflow-x: auto; background: #111827; color: #f9fafb; padding: 12px; border-radius: 8px; }}
    pre.table {{ background: #f3f4f6; color: #111827; }}
    .bullet {{ margin-left: 1rem; }}
    .toolbar {{ background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 12px; padding: 14px; margin-bottom: 24px; }}
  </style>
</head>
<body>
  <div class="toolbar"><strong>Enterprise QE Academy Practice Page</strong><br>Answer first, then open hints/answers only when ready.</div>
  {body}
</body>
</html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description="Generate standalone HTML from a tutor report.")
    p.add_argument("--report", default="latest", help="Report path or latest")
    p.add_argument("--out")
    args = p.parse_args()

    report = newest_report() if args.report.lower() == "latest" else Path(args.report)
    if not report.exists():
        raise FileNotFoundError(report)
    html_body = basic_markdown_to_html(report.read_text(encoding="utf-8"))
    out = Path(args.out) if args.out else OUT_DIR / f"{report.stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(report.stem, html_body), encoding="utf-8")
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
