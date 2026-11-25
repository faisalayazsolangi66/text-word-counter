#!/usr/bin/env python3
"""Count words, characters, lines and sentences in text files.

Reads one or more text files (or standard input when no file is
given) and reports words, characters (with and without spaces),
lines, sentences and paragraphs for each file, plus a total row
when more than one file is counted.
"""
import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[^\s]+")
SENTENCE_RE = re.compile(r"[.!?]+(?:\s|$)")


def count_text(text):
    """Return a dict of counts for *text*."""
    lines = text.splitlines()
    words = len(WORD_RE.findall(text))
    sentences = len(SENTENCE_RE.findall(text))
    paragraphs = len([block for block in text.split("\n\n")
                      if block.strip()])
    return {
        "words": words,
        "characters": len(text),
        "characters_no_spaces": len(re.sub(r"\s", "", text)),
        "lines": len(lines),
        "sentences": sentences,
        "paragraphs": paragraphs,
    }


def count_file(path, encoding="utf-8"):
    """Count a file, or stdin when *path* is '-'."""
    if path == "-":
        return count_text(sys.stdin.read())
    with open(path, encoding=encoding, errors="replace") as handle:
        return count_text(handle.read())


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Count words, characters, lines and sentences "
                    "in text files.")
    parser.add_argument("files", nargs="*", metavar="FILE",
                        help="text files to count (default: read stdin)")
    parser.add_argument("--json", action="store_true",
                        help="print results as JSON instead of a table")
    parser.add_argument("--encoding", default="utf-8",
                        help="file encoding (default: utf-8)")
    args = parser.parse_args(argv)

    targets = args.files or ["-"]
    results, totals = {}, {key: 0 for key in
                           ("words", "characters", "characters_no_spaces",
                            "lines", "sentences", "paragraphs")}
    for target in targets:
        try:
            counts = count_file(target, encoding=args.encoding)
        except FileNotFoundError:
            print(f"error: file not found: {target}", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        results[target] = counts
        for key in totals:
            totals[key] += counts[key]

    if args.json:
        print(json.dumps({"files": results, "total": totals}, indent=2))
        return 0

    header = (f"{'File':<30} {'Words':>7} {'Chars':>7} {'NoSpace':>7} "
              f"{'Lines':>6} {'Sent.':>6} {'Paras':>6}")
    print(header)
    print("-" * len(header))
    for target, counts in results.items():
        print(f"{target:<30} {counts['words']:>7} "
              f"{counts['characters']:>7} "
              f"{counts['characters_no_spaces']:>7} "
              f"{counts['lines']:>6} {counts['sentences']:>6} "
              f"{counts['paragraphs']:>6}")
    if len(results) > 1:
        print("-" * len(header))
        print(f"{'TOTAL':<30} {totals['words']:>7} "
              f"{totals['characters']:>7} "
              f"{totals['characters_no_spaces']:>7} "
              f"{totals['lines']:>6} {totals['sentences']:>6} "
              f"{totals['paragraphs']:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
