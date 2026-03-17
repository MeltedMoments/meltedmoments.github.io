#!/usr/bin/env python3
from __future__ import annotations

import json
import csv
from pathlib import Path
from typing import Any


def normalize_block(lines: list[str]) -> str:
    text = "\n".join(lines)
    return text.strip("\n").rstrip()


def extract_pairs(md_lines: list[str]) -> list[dict[str, Any]]:
    pairs = []

    i = 0
    n = len(md_lines)

    while i < n:
        if md_lines[i].startswith("## Prompt:"):
            prompt_line = i + 1
            i += 1

            prompt_lines = []
            while i < n and not md_lines[i].startswith("## Response:") and not md_lines[i].startswith("## Prompt:"):
                prompt_lines.append(md_lines[i])
                i += 1

            response_line = None
            response_lines = []

            if i < n and md_lines[i].startswith("## Response:"):
                response_line = i + 1
                i += 1

                while i < n and not md_lines[i].startswith("## Prompt:"):
                    response_lines.append(md_lines[i])
                    i += 1

            pairs.append(
                {
                    "prompt_line": prompt_line,
                    "response_line": response_line,
                    "prompt": normalize_block(prompt_lines),
                    "response": normalize_block(response_lines),
                }
            )

        else:
            i += 1

    return pairs


def write_tsv(pairs, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["prompt_line", "response_line", "prompt", "response"])

        for p in pairs:
            writer.writerow(
                [
                    p["prompt_line"],
                    p["response_line"] if p["response_line"] else "",
                    p["prompt"],
                    p["response"],
                ]
            )


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("input_md")
    ap.add_argument("--json", default="pairs.json")
    ap.add_argument("--tsv", default="pairs.tsv")

    args = ap.parse_args()

    text = Path(args.input_md).read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    pairs = extract_pairs(lines)

    Path(args.json).write_text(
        json.dumps(pairs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    write_tsv(pairs, args.tsv)

    print(f"Extracted {len(pairs)} prompt/response pairs")
    print(f"JSON: {args.json}")
    print(f"TSV : {args.tsv}")


if __name__ == "__main__":
    main()