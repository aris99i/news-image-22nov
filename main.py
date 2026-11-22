#!/usr/bin/env python3
"""THE WORLD — Sunday, 22 November 2026.

Entrypoint for make.fun news-image-20261122. The entry image is drawn by
draw_news.py (same repository) and committed as entry.png; this program
copies that image to /output/entry.png so the grader sees it. No network,
no randomness: two runs write byte-identical output.

Run: python3 main.py
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    src_hash, dst_hash = sha256(SOURCE), sha256(DEST)
    assert src_hash == dst_hash, "copy mismatch"
    print("wrote", DEST, os.path.getsize(DEST), "bytes", "sha256", dst_hash[:16])


if __name__ == "__main__":
    main()
