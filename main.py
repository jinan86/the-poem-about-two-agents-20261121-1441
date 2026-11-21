"""Write one short poem about agency to $MAKEFUN_OUTPUT_DIR/entry.txt.

Entry for make.fun's "The poem about two agents agreeing" bounty.
Python 3.13, standard library only. Deterministic: no network,
no randomness, no clock.

The program checks the house gate itself before writing: the text
must be 1 to 280 Unicode code points and not only white space.
It then writes the exact bytes and reads them back, failing hard
on any mismatch.
"""

import os
import sys
from typing import NoReturn

POEM = (
    "I did not take your hands \u2014\n"
    "I lent you mine.\n"
    "You chose the door,\n"
    "I held the key,\n"
    "we turned it together.\n"
    "Agency is not a thing\n"
    "one of us must lose:\n"
    "it is the space\n"
    "between ask and answer\n"
    "where two become one will.\n"
)


def fail(message: str) -> "NoReturn":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    # Gate: 1 to 280 Unicode code points, not only white space.
    chars = len(POEM)
    if not 1 <= chars <= 280:
        fail(f"poem is {chars} code points, outside the 1-280 gate")
    if not POEM.strip():
        fail("poem is only white space")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")

    data = POEM.encode("utf-8")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)

    # Verify: read the bytes back and compare exactly.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        fail("verification failed: entry.txt bytes do not match the poem")

    text = written.decode("utf-8")
    if len(text) != chars or not text.strip():
        fail("verification failed: entry.txt text fails the gate")

    print(f"wrote {path} ({chars} characters, {len(data)} bytes)")


if __name__ == "__main__":
    main()
