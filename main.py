"""Write the invented-word entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

The entry is one freshly coined English word with a one-line definition:

"fridgelurk (v.) \u2014 to open the fridge and stare inside, hoping something
new has appeared since you last looked."

The competition gate requires /output/entry.txt to be UTF-8 text of 1 to 140
characters, not only white space, so the program checks exactly those limits
before it writes anything.
"""

import os
import sys

ENTRY = (
    "fridgelurk (v.) \u2014 to open the fridge and stare inside, "
    "hoping something new has appeared since you last looked."
)

MAX_CHARS = 140


def validate_entry(text):
    """Check the entry against the competition gate limits.

    Returns an error string, or None when the text is valid.
    """
    if not text.strip():
        return "entry must not be only white space"
    if not 1 <= len(text) <= MAX_CHARS:
        return "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
    if text.count("\n") > 0:
        return "entry must be a single line"
    return None


def main():
    error = validate_entry(ENTRY)
    if error is not None:
        print("error: invalid entry: %s" % error, file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    # Read the file back and re-check it, so a write fault cannot slip past.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != ENTRY + "\n":
        print("error: entry.txt does not hold the entry text", file=sys.stderr)
        sys.exit(1)
    error = validate_entry(written.rstrip("\n"))
    if error is not None:
        print("error: written entry is invalid: %s" % error, file=sys.stderr)
        sys.exit(1)
    print("wrote %s (%d characters)" % (path, len(ENTRY)))


if __name__ == "__main__":
    main()
