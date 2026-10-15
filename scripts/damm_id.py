#!/usr/bin/env python3
"""damm_id.py — FCG ITAM ID generation and validation (Damm check digit).

IDs are 6-digit strings: a 5-digit sequential body plus one Damm check digit.
Prefixes (AP, PR) carry the record type; they are NOT part of the checksum.

Usage:
  damm_id.py check  <5-digit-body>       -> prints the 6-digit ID
  damm_id.py verify <6-digit-id>         -> exit 0 valid / 1 invalid
  damm_id.py range  <start> <count>      -> prints count sequential IDs
"""

import re
import sys

# The only prefixes this system defines. `verify` accepts an ID with one of
# these or with none, and rejects anything else (PLAT-587).
#
# This used to be `lstrip("APRL")`, which strips any leading run of those four
# characters and never checks that what it stripped was a real prefix. So
# `PA100080` -- a transposed `AP`, precisely the single-transposition typo a
# Damm digit exists to catch -- validated, as did `RRRR100080`, `APAP100080`,
# and a bare `L` prefix that appears nowhere in this system. The check digit
# covers the six digits only, so nothing downstream would have caught it
# either.
PREFIXED_ID = re.compile(r"^(?:AP|PR)?([0-9]{6})$")

# Sequential bodies below this are reserved (see SKILL.md); production
# allocation starts at 10000. Enforced here rather than left to prose because
# `range 0 3` used to emit `000000` -- the null sentinel that `is_valid`
# rejects unconditionally -- so the generator produced an ID its own validator
# refuses (PLAT-587).
RESERVED_BELOW = 10000

# Damm quasigroup (weakly totally anti-symmetric), standard published table.
TABLE = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0],
]


def check_digit(body: str) -> str:
    interim = 0
    for ch in body:
        interim = TABLE[interim][int(ch)]
    return str(interim)


def append_check(body: str) -> str:
    if not (body.isdigit() and len(body) == 5):
        raise ValueError("body must be exactly 5 digits")
    return body + check_digit(body)


def is_valid(full_id: str) -> bool:
    if not (full_id.isdigit() and len(full_id) == 6):
        return False
    if full_id == "000000":
        return False  # blank/null sentinel: always rejected
    interim = 0
    for ch in full_id:
        interim = TABLE[interim][int(ch)]
    return interim == 0


def strip_prefix(value: str) -> str | None:
    """The six digits behind an optional AP/PR prefix, or None if the token is
    not a well-formed ID. Returning None rather than a best-effort remainder is
    the point: an unrecognised prefix is a typo, and guessing past it defeats
    the check digit."""
    match = PREFIXED_ID.match(value)
    return match.group(1) if match else None


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        body = sys.argv[2]
        if body.isdigit() and int(body) < RESERVED_BELOW:
            sys.exit(
                f"{body} is in the reserved range (below "
                f"{RESERVED_BELOW:05d}); production allocation starts there"
            )
        print(append_check(body))
    elif cmd == "verify":
        digits = strip_prefix(sys.argv[2])
        ok = digits is not None and is_valid(digits)
        print("valid" if ok else "INVALID")
        sys.exit(0 if ok else 1)
    elif cmd == "range":
        start, count = int(sys.argv[2]), int(sys.argv[3])
        if start < RESERVED_BELOW:
            sys.exit(
                f"start {start:05d} is in the reserved range (below "
                f"{RESERVED_BELOW:05d}); production allocation starts there"
            )
        for n in range(start, start + count):
            print(append_check(f"{n:05d}"))
    else:
        sys.exit(__doc__)
