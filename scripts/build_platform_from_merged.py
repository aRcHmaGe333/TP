from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [ROOT / "MERGED_CONTENTS_part001b.md", ROOT / "MERGED_CONTENTS_part002b.md"]

header_re = re.compile(r"^## File: (.+)$")


def clean_block(lines: list[str]) -> str:
    if not lines:
        return ""
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()

    if lines and lines[0].strip() == "_(empty)_":
        return ""

    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("```"):
                lines = lines[:i]
                break

    text = "\n".join(lines)
    return text.lstrip("\ufeff") + ("\n" if text and not text.endswith("\n") else "")


def extract_files(md_path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    current_path: str | None = None
    buffer: list[str] = []

    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        m = header_re.match(raw_line)
        if m:
            if current_path and current_path.startswith("platform/"):
                out[current_path] = clean_block(buffer)
            current_path = m.group(1).strip()
            buffer = []
        else:
            if current_path is not None:
                buffer.append(raw_line)

    if current_path and current_path.startswith("platform/"):
        out[current_path] = clean_block(buffer)

    return out


def main() -> None:
    merged: dict[str, str] = {}
    for path in INPUTS:
        merged.update(extract_files(path))

    if not merged:
        raise SystemExit("No platform files found in merged content files")

    for rel_path, content in merged.items():
        target = ROOT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    print(f"Wrote {len(merged)} files into {ROOT / 'platform'}")


if __name__ == "__main__":
    main()
