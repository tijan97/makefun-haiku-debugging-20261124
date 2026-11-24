#!/usr/bin/env python3
"""One haiku about debugging, in the 5-7-5 syllable shape.

Writes the haiku as plain text to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Python standard library only.
"""

import os
import re

HAIKU = (
    "One red line remains\n"
    "the log insists it works fine\n"
    "yet it does not work"
)

# Syllable counts for every word in the haiku (verified by hand).
SYLLABLES = {
    "one": 1, "red": 1, "line": 1, "remains": 2,
    "the": 1, "log": 1, "insists": 2, "it": 1, "works": 1, "fine": 1,
    "yet": 1, "does": 1, "not": 1, "work": 1,
}

EXPECTED = (5, 7, 5)


def count_syllables(word):
    word = word.lower().strip(".,;:!?\"'")
    if word in SYLLABLES:
        return SYLLABLES[word]
    # Fallback vowel-group heuristic for any word not in the map.
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def validate(text):
    if not (1 <= len(text) <= 200):
        raise ValueError(f"haiku must be 1-200 chars, got {len(text)}")
    lines = text.split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must be 3 lines, got {len(lines)}")
    for i, (line, want) in enumerate(zip(lines, EXPECTED), 1):
        got = sum(count_syllables(w) for w in line.split())
        if got != want:
            raise ValueError(f"line {i} must be {want} syllables, got {got}: {line!r}")
    if not text.strip():
        raise ValueError("haiku must not be blank")


def main():
    validate(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HAIKU)
    # Read back and re-validate what was written.
    written = open(path, encoding="utf-8").read()
    assert written == HAIKU, "written file differs from the haiku"
    validate(written)
    print(f"wrote {len(HAIKU)} chars to {path}")


if __name__ == "__main__":
    main()
