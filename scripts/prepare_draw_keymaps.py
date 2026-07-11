#!/usr/bin/env python3
"""
Prepare draw-only keymap files by removing combos while keeping layer #defines.
Usage: python scripts/prepare_draw_keymaps.py --in-dir config --out-dir .draw_temp
"""
import argparse
import re
from pathlib import Path


def strip_draw_incompatible(text: str) -> str:
    # keymap-drawer uses a C preprocessor: keep #define layer names, but remove
    # combos and #ifndef blocks that the parser cannot handle.
    text = re.sub(
        r"/\*\s*combos are not yet handled.*?\*/\s*\n\s*#ifndef\b.*?#endif\b\s*",
        "\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r"^\s*#ifndef\b.*?#endif\b\s*", "", text, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(
        r"(^|\n)\s*combos\s*\{.*?\}\s*;\s*(?=\n|$)",
        "\n",
        text,
        flags=re.DOTALL,
    )
    return text


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
        new = strip_draw_incompatible(text)
        out.write_text(new, encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == '__main__':
    main()
