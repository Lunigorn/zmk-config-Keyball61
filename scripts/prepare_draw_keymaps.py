#!/usr/bin/env python3
"""
Prepare draw-only keymap files by removing top-level combos blocks.
Usage: python scripts/prepare_draw_keymaps.py --in-dir config --out-dir .draw_temp
"""
import argparse
import re
from pathlib import Path


def strip_combos(text: str) -> str:
    # Remove top-level `combos { ... };` blocks (non-greedy). We try to only match
    # blocks that start at column 0 or with whitespace before 'combos', and end
    # with '};' at top-level.
    pattern = re.compile(r"(^|\n)\s*combos\s*\{.*?\}\s*;\s*(?=\n|$)", re.DOTALL)
    return pattern.sub("\n", text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-dir", default="config")
    parser.add_argument("--out-dir", default=".draw_temp")
    args = parser.parse_args()

    src = Path(args.in_dir)
    dst = Path(args.out_dir)
    dst.mkdir(parents=True, exist_ok=True)

    for f in src.glob("*.keymap"):
        out = dst / f.name
        text = f.read_text(encoding="utf-8")
        new = strip_combos(text)
        out.write_text(new, encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == '__main__':
    main()
