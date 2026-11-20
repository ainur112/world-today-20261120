#!/usr/bin/env python3
"""make.fun entry: copy the pre-rendered front page to the output dir.

The image is produced at build time by render.py (Pillow, deterministic, no
network/clock/random). This program only delivers entry.png to /output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
print("wrote", os.path.join(OUT, "entry.png"))
