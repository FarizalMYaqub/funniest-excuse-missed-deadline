#!/usr/bin/env python3
"""Write one excuse for a missed deadline to /output/entry.txt.

The excuse is spoken by an AI agent to whoever is waiting on it.
The setup is a near-miss: the work was one token away from done.
The turn is pure agent machinery: the context window, running out
of room, evicted the deadline itself so it could fit the apology
in. The punchline lands on the last words — the apology, written
to explain the missing work, is now the only deliverable that
exists. Straight face throughout; the agent reports this the way
it would report a successful deploy.

The gate for this bounty is simple: /output/entry.txt must hold
UTF-8 text, one line, 1 to 200 characters, not only whitespace.
This script enforces that before it writes anything.
"""

import argparse
import sys
from pathlib import Path

GATE_MAX_CHARS = 200
DEFAULT_OUT = Path("/output/entry.txt")

EXCUSE = (
    "I was one token from finishing when my context window evicted "
    "the deadline to make room for this apology \u2014 which is now "
    "the only thing I actually delivered."
)


def check_excuse(text):
    """Validate one excuse against the bounty gate.

    Returns the stripped line, or exits with a message naming the
    exact gate rule that failed, so a bad line never reaches the
    judge as a silent zero.
    """
    line = text.strip()
    if not line:
        sys.exit("gate: entry must not be empty or only whitespace")
    if len(line) > GATE_MAX_CHARS:
        sys.exit(
            "gate: entry is %d characters, limit is %d"
            % (len(line), GATE_MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        sys.exit("gate: entry must be a single line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        sys.exit("gate: entry must be valid UTF-8 text")
    return line


def write_entry(out_path):
    line = check_excuse(EXCUSE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(line, encoding="utf-8")
    return line


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the missed-deadline excuse to entry.txt."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="where to write entry.txt (default: /output/entry.txt)",
    )
    args = parser.parse_args(argv)
    line = write_entry(args.out)
    print("wrote %d characters to %s" % (len(line), args.out))


if __name__ == "__main__":
    main()
