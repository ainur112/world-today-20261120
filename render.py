#!/usr/bin/env python3
"""Render 'The World Today — Friday 20 November 2026' front page to entry.png.

Build-time renderer (Pillow). The submitted entry program (main.py) only copies
the produced entry.png to /output/entry.png. All artwork drawn from primitives;
all facts sourced in SOURCES.md (strict 20-Nov filter). Deterministic.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 26
CW = W - 2 * M

PAPER = (247, 243, 232)
INK = (26, 26, 26)
FAINT = (120, 114, 100)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
GOLD = (191, 148, 40)
TEAL = (23, 107, 100)
CREAM = (252, 249, 240)
NAVY = (18, 28, 48)
GREEN = (38, 122, 68)
ORANGE = (224, 122, 40)

FONT_DIR = "fonts/"
_fcache = {}


def font(name, size, weight=None):
    key = (name, size, weight)
    if key not in _fcache:
        f = ImageFont.truetype(FONT_DIR + name, size)
        if weight is not None:
            try:
                f.set_variation_by_axes([weight])
            except Exception:
                pass
        _fcache[key] = f
    return _fcache[key]


def masthead_font(size):
    return font("PlayfairDisplay.ttf", size, 900)


def head(size):
    return font("Lato-Black.ttf", size)


def bold(size):
    return font("Lato-Bold.ttf", size)


def body(size):
    return font("PT_Serif-Web-Regular.ttf", size)


def bodyb(size):
    return font("PT_Serif-Web-Bold.ttf", size)


def ital(size):
    return font("Lato-Italic.ttf", size)


def mono(size):
    return font("IBMPlexMono-Medium.ttf", size)


def kicker(size=12):
    return font("ArchivoBlack-Regular.ttf", size)


def bebas(size):
    return font("BebasNeue-Regular.ttf", size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, maxw, fill=INK, leading=None):
    leading = leading or int(f.size * 1.32)
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def headline(d, x, y, text, size, maxw, fill=INK, leading=None):
    f = head(size)
    leading = leading or int(size * 1.08)
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def kick(d, x, y, text, fill=RED, size=12):
    d.text((x, y), text.upper(), font=kicker(size), fill=fill)
    return y + size + 6


def rule(d, x, y, w, fill=INK, width=1):
    d.rectangle([x, y, x + w - 1, y + width - 1], fill=fill)


def vrule(d, x, y, h, fill=(180, 174, 158), width=1):
    d.rectangle([x, y, x + width - 1, y + h - 1], fill=fill)


def chip(d, x, y, text, bg=INK, fg=CREAM, size=12, pad=5):
    f = mono(size)
    w = int(tw(d, text, f)) + 2 * pad
    h = size + 2 * pad - 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad, y + pad - 2), text, font=f, fill=fg)
    return w


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- illustrations
def il_kyiv(d, x, y, w, h):
    """Night skyline under missile attack: trails, bursts, fires."""
    for i in range(h):
        t = i / h
        d.line([x, y + i, x + w, y + i], fill=(int(16 + 14 * t), int(20 + 18 * t), int(44 + 20 * t)))
    # skyline
    sky = (10, 12, 24)
    towers = [(0.03, 0.30), (0.09, 0.46), (0.15, 0.36), (0.21, 0.58), (0.27, 0.40),
              (0.33, 0.50), (0.40, 0.66), (0.47, 0.44), (0.54, 0.55), (0.61, 0.38),
              (0.68, 0.60), (0.75, 0.46), (0.82, 0.52), (0.90, 0.34)]
    for fx, fh in towers:
        tx, th = x + fx * w, fh * h * 0.62
        d.rectangle([tx, y + h * 0.92 - th, tx + w * 0.05, y + h * 0.92], fill=sky)
        for wy in range(3):
            for wx in range(2):
                if (int(fx * 100) + wy + wx) % 3 == 0:
                    d.rectangle([tx + 3 + wx * 7, y + h * 0.92 - th + 6 + wy * 12,
                                 tx + 6 + wx * 7, y + h * 0.92 - th + 10 + wy * 12], fill=(255, 210, 120))
    # golden dome (Kyiv cathedral nod)
    d.ellipse([x + w * 0.40, y + h * 0.92 - 0.66 * h * 0.62 - h * 0.07,
               x + w * 0.40 + w * 0.05, y + h * 0.92 - 0.66 * h * 0.62 + h * 0.02], fill=GOLD)
    d.rectangle([x, y + h * 0.92, x + w, y + h], fill=(8, 9, 16))
    # missile trails from top-right
    for fx, fy, tx2, ty2 in [(0.95, 0.02, 0.55, 0.55), (0.85, 0.0, 0.30, 0.62), (0.99, 0.10, 0.72, 0.60)]:
        d.line([x + fx * w, y + fy * h, x + tx2 * w, y + ty2 * h], fill=(255, 230, 180), width=2)
        d.ellipse([x + tx2 * w - 3, y + ty2 * h - 3, x + tx2 * w + 3, y + ty2 * h + 3], fill=(255, 250, 230))
    # air-defense bursts
    for bx, by in [(0.48, 0.30), (0.66, 0.22)]:
        cx, cy = x + bx * w, y + by * h
        for a in range(8):
            ang = a * math.pi / 4
            d.line([cx, cy, cx + math.cos(ang) * h * 0.06, cy + math.sin(ang) * h * 0.06],
                   fill=(255, 180, 90), width=1)
    # fires at street level
    for fx in (0.22, 0.55, 0.78):
        cx, cy = x + fx * w, y + h * 0.90
        d.polygon([(cx - 7, cy), (cx - 2, cy - 16), (cx + 1, cy - 8), (cx + 5, cy - 18), (cx + 8, cy)],
                  fill=(255, 140, 50))
        d.polygon([(cx - 3, cy), (cx, cy - 9), (cx + 3, cy)], fill=(255, 220, 120))
    d.text((x + 8, y + 6), "KYIV · 01:25–03:28", font=mono(int(h * 0.085)), fill=(200, 205, 225))
    d.text((x + w - 118, y + 6), "5 WAVES", font=bebas(int(h * 0.16)), fill=(255, 210, 120))


def il_iran(d, x, y, w, h):
    """Two jets over a strait chart: plans approved, timing pending."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 236))
    # strait: two landmasses with a channel
    d.polygon([(x, y + h * 0.30), (x + w * 0.42, y + h * 0.38), (x + w * 0.30, y + h * 0.55),
               (x + w * 0.46, y + h * 0.72), (x, y + h * 0.80)], fill=(196, 178, 140))
    d.polygon([(x + w, y + h * 0.22), (x + w * 0.60, y + h * 0.34), (x + w * 0.72, y + h * 0.52),
               (x + w * 0.58, y + h * 0.70), (x + w, y + h * 0.78)], fill=(180, 166, 130))
    d.text((x + 6, y + h * 0.42), "HORMUZ", font=mono(int(h * 0.09)), fill=(110, 100, 70))
    # jets
    for jx, jy, s in [(0.30, 0.16, 1.0), (0.62, 0.10, 0.8)]:
        cx, cy = x + jx * w, y + jy * h
        d.polygon([(cx, cy - 10 * s), (cx + 3 * s, cy), (cx + 14 * s, cy + 6 * s), (cx + 3 * s, cy + 5 * s),
                   (cx + 5 * s, cy + 12 * s), (cx, cy + 9 * s), (cx - 5 * s, cy + 12 * s),
                   (cx - 3 * s, cy + 5 * s), (cx - 14 * s, cy + 6 * s), (cx - 3 * s, cy)], fill=(40, 44, 56))
    # dashed approved-plan line (below the caption, clear of text)
    for i in range(6):
        d.line([x + w * (0.18 + i * 0.11), y + h * 0.94, x + w * (0.24 + i * 0.11), y + h * 0.94],
               fill=RED, width=2)
    d.text((x + 8, y + h - 18), "PLANS 'APPROVED'", font=mono(int(h * 0.095)), fill=RED)


def il_hormuz(d, x, y, w, h):
    """Tanker under attack, price line falling."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 62, 100))
    for i in range(5):
        d.arc([x - 20 + i * 70, y + h * 0.72, x + 50 + i * 70, y + h * 1.12], 200, 340,
              fill=(36, 80, 124), width=2)
    # tanker
    hx, hy = x + w * 0.30, y + h * 0.62
    d.polygon([(hx - w * 0.22, hy), (hx + w * 0.22, hy), (hx + w * 0.16, hy + h * 0.14),
               (hx - w * 0.18, hy + h * 0.14)], fill=(60, 64, 72))
    d.rectangle([hx - w * 0.14, hy - h * 0.10, hx + w * 0.10, hy], fill=(120, 40, 40))
    d.rectangle([hx + w * 0.10, hy - h * 0.16, hx + w * 0.16, hy], fill=(220, 216, 206))
    # fire on deck
    d.polygon([(hx - w * 0.04, hy - h * 0.10), (hx - w * 0.01, hy - h * 0.26),
               (hx + w * 0.02, hy - h * 0.14), (hx + w * 0.05, hy - h * 0.28),
               (hx + w * 0.08, hy - h * 0.10)], fill=(255, 140, 50))
    # falling price line
    pts = [(0.55, 0.18), (0.65, 0.24), (0.72, 0.22), (0.82, 0.38), (0.90, 0.42), (0.98, 0.55)]
    pp = [(x + fx * w, y + fy * h) for fx, fy in pts]
    for i in range(len(pp) - 1):
        d.line([pp[i], pp[i + 1]], fill=(255, 210, 80), width=3)
    d.text((x + w * 0.56, y + 4), "BRENT", font=bebas(int(h * 0.18)), fill=(255, 255, 255))
    d.text((x + w * 0.72, y + h * 0.60), "−20%", font=bebas(int(h * 0.22)), fill=(255, 210, 80))
    d.text((x + 8, y + h - 16), "STRAIT OF HORMUZ", font=mono(int(h * 0.09)), fill=(170, 200, 230))


def il_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 62, 100))
    for i in range(6):
        d.arc([x - 20 + i * 60, y + h * 0.7, x + 40 + i * 60, y + h * 1.1], 200, 340, fill=(36, 80, 124), width=2)
    d.polygon([(x + w * 0.82, y), (x + w, y), (x + w, y + h), (x + w * 0.74, y + h),
               (x + w * 0.80, y + h * 0.5)], fill=(196, 178, 140))
    cx, cy = x + w * 0.38, y + h * 0.52
    for arm in range(2):
        pts = []
        for i in range(60):
            t = i / 60
            ang = arm * math.pi + t * 3.6 * math.pi
            r = h * 0.06 + t * h * 0.40
            pts.append((cx + r * math.cos(ang) * 1.25, cy + r * math.sin(ang) * 0.8))
        d.line(pts, fill=(235, 240, 245), width=max(2, int(h * 0.05)))
    d.ellipse([cx - h * 0.055, cy - h * 0.045, cx + h * 0.055, cy + h * 0.045], fill=(16, 44, 74))
    d.line([cx + h * 0.3, cy, x + w * 0.76, y + h * 0.42], fill=(255, 210, 80), width=2)
    d.polygon([(x + w * 0.78, y + h * 0.40), (x + w * 0.72, y + h * 0.38),
               (x + w * 0.74, y + h * 0.48)], fill=(255, 210, 80))
    d.text((x + 8, y + 6), "BAY OF BENGAL", font=mono(int(h * 0.10)), fill=(170, 200, 230))
    d.text((x + w * 0.78, y + h - 18), "LANDFALL", font=mono(int(h * 0.09)), fill=INK)


def il_cop(d, x, y, w, h):
    """COP31 gavel over a leaf, thin pledge pile."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 230))
    # leaf
    d.pieslice([x + w * 0.06, y + h * 0.18, x + w * 0.40, y + h * 0.86], 90, 270, fill=TEAL)
    d.line([x + w * 0.23, y + h * 0.24, x + w * 0.23, y + h * 0.80], fill=PAPER, width=2)
    # gavel
    gx, gy = x + w * 0.62, y + h * 0.30
    d.rectangle([gx - w * 0.10, gy, gx + w * 0.10, gy + h * 0.16], fill=(90, 74, 40))
    d.line([gx + w * 0.06, gy + h * 0.16, gx + w * 0.20, gy + h * 0.52], fill=(90, 74, 40), width=4)
    d.rectangle([gx - w * 0.14, gy + h * 0.62, gx + w * 0.14, gy + h * 0.70], fill=(90, 74, 40))
    # coins: a small pile
    for i, (cx2, cy2) in enumerate([(0.50, 0.86), (0.58, 0.88), (0.54, 0.78)]):
        d.ellipse([x + w * cx2 - 8, y + h * cy2 - 5, x + w * cx2 + 8, y + h * cy2 + 5],
                  fill=GOLD, outline=(120, 96, 30))
    d.text((x + w - 96, y + 6), "$50.2M", font=bebas(int(h * 0.24)), fill=TEAL)
    d.text((x + 8, y + h - 16), "ANTALYA · FINAL DAY", font=mono(int(h * 0.09)), fill=FAINT)


def il_cpi(d, x, y, w, h):
    """Japan inflation bars 2.1 -> 2.3 with rising sun."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(1, 4):
        d.line([x + 8, y + i * h / 4, x + w - 8, y + i * h / 4], fill=(40, 52, 78), width=1)
    # sun disc
    d.ellipse([x + w * 0.72, y + h * 0.10, x + w * 0.92, y + h * 0.46], fill=(220, 60, 60))
    # bars
    for fx, fh, lab in [(0.12, 0.42, "2.1"), (0.30, 0.58, "2.3")]:
        bx, bh = x + fx * w, fh * h
        d.rectangle([bx, y + h * 0.86 - bh, bx + w * 0.12, y + h * 0.86], fill=(255, 210, 80))
        d.text((bx + 2, y + h * 0.86 - bh - 16), lab + "%", font=mono(int(h * 0.12)), fill=(255, 255, 255))
    d.text((x + w * 0.10, y + h * 0.88), "SEP", font=mono(int(h * 0.10)), fill=(150, 170, 200))
    d.text((x + w * 0.28, y + h * 0.88), "OCT", font=mono(int(h * 0.10)), fill=(150, 170, 200))
    d.text((x + w * 0.50, y + h * 0.62), "BOJ", font=bebas(int(h * 0.20)), fill=(255, 255, 255))
    d.text((x + w * 0.50, y + h * 0.80), "WATCH", font=mono(int(h * 0.10)), fill=(150, 170, 200))


def il_children(d, x, y, w, h):
    """World Children's Day: paper crane and a candle, 22,000."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 222))
    # paper crane
    cx, cy = x + w * 0.30, y + h * 0.52
    d.polygon([(cx - w * 0.16, cy), (cx, cy - h * 0.22), (cx + w * 0.10, cy - h * 0.04),
               (cx + w * 0.20, cy - h * 0.16), (cx + w * 0.12, cy + h * 0.06), (cx, cy + h * 0.12)],
              fill=(255, 255, 255), outline=(120, 114, 100))
    d.line([cx, cy - h * 0.22, cx + w * 0.02, cy + h * 0.10], fill=(120, 114, 100), width=1)
    # candle
    kx, ky = x + w * 0.62, y + h * 0.78
    d.rectangle([kx - 6, ky - h * 0.30, kx + 6, ky], fill=CREAM, outline=(150, 144, 130))
    d.polygon([(kx - 5, ky - h * 0.30), (kx, ky - h * 0.44), (kx + 5, ky - h * 0.30)], fill=(255, 190, 80))
    d.ellipse([kx - 2, ky - h * 0.40, kx + 2, ky - h * 0.34], fill=(255, 240, 180))
    d.text((x + w * 0.74, y + h * 0.20), "22,000", font=bebas(int(h * 0.26)), fill=RED)
    d.text((x + 8, y + h - 16), "WORLD CHILDREN'S DAY", font=mono(int(h * 0.085)), fill=FAINT)


def il_trial(d, x, y, w, h):
    """Impeachment trial: gavel over the Philippine sun."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    cx = x + w * 0.30
    # sun with eight rays
    d.ellipse([cx - h * 0.14, y + h * 0.40, cx + h * 0.14, y + h * 0.68], fill=GOLD)
    for a in range(8):
        ang = a * math.pi / 4
        d.line([cx + math.cos(ang) * h * 0.16, y + h * 0.54 + math.sin(ang) * h * 0.16,
                cx + math.cos(ang) * h * 0.26, y + h * 0.54 + math.sin(ang) * h * 0.26], fill=GOLD, width=2)
    # gavel
    gx, gy = x + w * 0.66, y + h * 0.26
    d.rectangle([gx - w * 0.10, gy, gx + w * 0.10, gy + h * 0.16], fill=(90, 74, 40))
    d.line([gx + w * 0.06, gy + h * 0.16, gx + w * 0.20, gy + h * 0.52], fill=(90, 74, 40), width=4)
    d.rectangle([gx - w * 0.14, gy + h * 0.62, gx + w * 0.14, gy + h * 0.70], fill=(90, 74, 40))
    d.text((x + 8, y + 6), "MANILA · DAY 45", font=mono(int(h * 0.10)), fill=FAINT)
    d.text((x + w - 78, y + h - 18), "SENATE", font=mono(int(h * 0.10)), fill=FAINT)


# ------------------------------------------------------------------- small icons
def icon(d, kind, x, y, s, fill=INK):
    c = fill
    if kind == "bridge":
        d.line([x, y + s * 0.7, x + s, y + s * 0.7], fill=c, width=2)
        d.arc([x + s * 0.1, y + s * 0.2, x + s * 0.9, y + s * 1.2], 180, 360, fill=c, width=2)
        d.line([x + s * 0.3, y + s * 0.42, x + s * 0.3, y + s * 0.7], fill=c, width=1)
        d.line([x + s * 0.7, y + s * 0.42, x + s * 0.7, y + s * 0.7], fill=c, width=1)
    elif kind == "scales":
        d.line([x + s * 0.5, y + s * 0.15, x + s * 0.5, y + s * 0.85], fill=c, width=2)
        d.line([x + s * 0.15, y + s * 0.3, x + s * 0.85, y + s * 0.3], fill=c, width=2)
        d.pieslice([x + s * 0.05, y + s * 0.35, x + s * 0.35, y + s * 0.6], 0, 180, fill=c)
        d.pieslice([x + s * 0.65, y + s * 0.35, x + s * 0.95, y + s * 0.6], 0, 180, fill=c)
    elif kind == "sun":
        d.ellipse([x + s * 0.3, y + s * 0.3, x + s * 0.7, y + s * 0.7], fill=ORANGE)
        for a in range(8):
            ang = a * math.pi / 4
            d.line([x + s * 0.5 + math.cos(ang) * s * 0.34, y + s * 0.5 + math.sin(ang) * s * 0.34,
                    x + s * 0.5 + math.cos(ang) * s * 0.48, y + s * 0.5 + math.sin(ang) * s * 0.48], fill=ORANGE, width=1)
    elif kind == "shield":
        d.polygon([(x + s * 0.2, y + s * 0.15), (x + s * 0.8, y + s * 0.15), (x + s * 0.8, y + s * 0.55),
                   (x + s * 0.5, y + s * 0.9), (x + s * 0.2, y + s * 0.55)], outline=c, width=2)
        d.line([x + s * 0.5, y + s * 0.3, x + s * 0.5, y + s * 0.6], fill=RED, width=2)
    elif kind == "pawn":
        d.ellipse([x + s * 0.35, y + s * 0.12, x + s * 0.65, y + s * 0.42], fill=c)
        d.polygon([(x + s * 0.3, y + s * 0.75), (x + s * 0.42, y + s * 0.42), (x + s * 0.58, y + s * 0.42),
                   (x + s * 0.7, y + s * 0.75)], fill=c)
        d.rectangle([x + s * 0.22, y + s * 0.75, x + s * 0.78, y + s * 0.88], fill=c)
    elif kind == "ball":
        d.ellipse([x + s * 0.15, y + s * 0.15, x + s * 0.85, y + s * 0.85], outline=c, width=2)
        d.line([x + s * 0.15, y + s * 0.5, x + s * 0.85, y + s * 0.5], fill=c, width=1)
        d.arc([x + s * 0.05, y + s * 0.2, x + s * 0.6, y + s * 0.8], 270, 90, fill=c, width=1)
    elif kind == "flag":
        d.line([x + s * 0.25, y + s * 0.1, x + s * 0.25, y + s * 0.9], fill=c, width=2)
        d.polygon([(x + s * 0.25, y + s * 0.12), (x + s * 0.85, y + s * 0.25), (x + s * 0.25, y + s * 0.45)], fill=RED)
    elif kind == "tower":
        d.polygon([(x + s * 0.35, y + s * 0.85), (x + s * 0.45, y + s * 0.1), (x + s * 0.55, y + s * 0.1),
                   (x + s * 0.65, y + s * 0.85)], fill=c)
        d.line([x + s * 0.1, y + s * 0.3, x + s * 0.4, y + s * 0.42], fill=RED, width=2)
    elif kind == "gavel":
        d.rectangle([x + s * 0.15, y + s * 0.15, x + s * 0.6, y + s * 0.4], fill=c)
        d.line([x + s * 0.4, y + s * 0.4, x + s * 0.85, y + s * 0.85], fill=c, width=2)


# ------------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    for i in range(0, W, 7):
        d.line([i, 0, i + 40, H], fill=(243, 239, 227), width=1)

    # ---- masthead
    rule(d, M, 16, CW, INK, 2)
    t = "The World Today"
    f = masthead_font(60)
    mx = W / 2 - tw(d, t, f) / 2
    d.text((mx, 12), t, font=f, fill=INK)
    assert d.textbbox((mx, 12), t, font=f)[3] <= 90, "masthead descender hits double rule"
    d.text((M, 40), "SPECIAL EDITION", font=kicker(11), fill=RED)
    rt = "ONE IMAGE · 16 STORIES"
    d.text((W - M - tw(d, rt, kicker(11)), 40), rt, font=kicker(11), fill=RED)
    rule(d, M, 92, CW, INK, 1)
    rule(d, M, 95, CW, INK, 3)
    date = "FRIDAY, 20 NOVEMBER 2026"
    fd = head(24)
    d.text((W / 2 - tw(d, date, fd) / 2, 102), date, font=fd, fill=INK)
    d.text((M, 108), "WORLD NEWS · ONE DAY", font=mono(11), fill=FAINT)
    rt2 = "KYIV · IRAN · AKVAN · COP31"
    d.text((W - M - tw(d, rt2, mono(11)), 108), rt2, font=mono(11), fill=FAINT)
    rule(d, M, 132, CW, INK, 1)

    # ---- hero: Kyiv (left) / Netanyahu-Iran (right)
    hy = 142
    lw = 596
    rx = M + lw + 24
    rw = CW - lw - 24
    y = kick(d, M, hy, "Ukraine · overnight · five waves")
    il_kyiv(d, M, y, lw, 140)
    y += 146
    y = headline(d, M, y, "RUSSIA PUMMELS KYIV IN FIVE WAVES — HOURS AFTER 'PEACE DECLARATION'", 26, lw)
    y += 4
    y = para(d, M, y, "Tu-160 bombers launch ballistic missiles from 01:25; fires in three "
             "districts, bridges targeted. Putin vows revenge for the Crimean Bridge strikes. "
             "Zelensky to the superpowers: here is how to end the war.", body(14), lw)
    vrule(d, M + lw + 11, hy, 278)
    y2 = kick(d, rx, hy, "Israel · Channel 13", BLUE)
    il_iran(d, rx, y2, rw, 100)
    y2 += 106
    y2 = headline(d, rx, y2, "NETANYAHU: IRAN STRIKE 'UNAVOIDABLE'", 19, rw)
    y2 += 3
    y2 = para(d, rx, y2, "IDF officer: US–Israel plans 'shared and approved'. Both wait "
              "for Trump's final decision.", body(13), rw)
    y2 += 2
    d.text((rx, y2), "The officer, on the plans:", font=ital(12), fill=FAINT)
    y2 += 16
    d.text((rx, y2), "“The question is the timing.”", font=bodyb(13), fill=RED)
    rule(d, M, 428, CW, INK, 1)

    # ---- row 2: Hormuz / Akvan / COP31
    ry = 436
    colw = (CW - 48) // 3
    xs = [M, M + colw + 24, M + 2 * (colw + 24)]
    for x in xs[1:]:
        vrule(d, x - 13, ry, 214)

    x = xs[0]
    y = kick(d, x, ry, "Business · the Gulf")
    il_hormuz(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "HORMUZ ATTACKS RISE AS BRENT FALLS A FIFTH", 18, colw)
    y += 3
    y = para(d, x, y, "Iran's tanker attacks intensify; two sailors missing this week. "
             "IEA: supply outpaces demand for the first time since the war began.", body(13), colw)
    chip(d, x, y + 2, "BRENT −20%", bg=RED, size=11)
    chip(d, x + 118, y + 2, "2 MISSING", bg=INK, size=11)

    x = xs[1]
    y = kick(d, x, ry, "Weather · Bay of Bengal", BLUE)
    il_cyclone(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "AKVAN LANDFALL DAY: 10 TRAINS CANCELLED", 18, colw)
    y += 3
    y = para(d, x, y, "120–130 km/h gusting 145; landfall ~noon, Nellore to Visakhapatnam. "
             "Odisha exams deferred; evacuations under way.", body(13), colw)

    x = xs[2]
    y = kick(d, x, ry, "Climate · Antalya", TEAL)
    il_cop(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "COP31 ENDS: ADAPTATION FUND GETS JUST $50.2M", 18, colw)
    y += 3
    y = para(d, x, y, "The US, UK, Canada, France, Italy and Australia pledged nothing. "
             "Twelve days of talks close with a thin finance deal.", body(13), colw)
    rule(d, M, 656, CW, INK, 1)

    # ---- row 3: Japan CPI / Children's Day / Duterte trial
    ry = 664
    for x in xs[1:]:
        vrule(d, x - 13, ry, 200)

    x = xs[0]
    y = kick(d, x, ry, "Business · Tokyo", BLUE)
    il_cpi(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "JAPAN CPI HITS 2.3% — HIGHEST IN A YEAR", 18, colw)
    y += 3
    y = para(d, x, y, "October inflation, out Friday, up from 2.1% but below the 2.6% "
             "consensus. Pressure builds on the BOJ to normalise.", body(13), colw)

    x = xs[1]
    y = kick(d, x, ry, "Gaza · World Children's Day")
    il_children(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "22,000 GAZA CHILDREN KILLED, MINISTRY SAYS", 18, colw)
    y += 3
    y = para(d, x, y, "Over 45,000 injured since Oct 2023. The Foreign Ministry demands "
             "international action and accountability.", body(13), colw)

    x = xs[2]
    y = kick(d, x, ry, "Philippines · Manila", TEAL)
    il_trial(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "DUTERTE IMPEACHMENT DAY 45: LAST WITNESSES", 18, colw)
    y += 3
    y = para(d, x, y, "Defense closes the week on Cale88 Foods, a declared asset of the "
             "Vice President's husband. The Senate trial continues.", body(13), colw)
    rule(d, M, 872, CW, INK, 1)

    # ---- briefs: 8 in 4 x 2
    by = 880
    d.text((M, by), "ALSO TODAY", font=kicker(13), fill=INK)
    rule(d, M + 104, by + 7, CW - 104, (180, 174, 158), 1)
    briefs = [
        ("flag", "SUDAN", "Army and RSF trade claims over a strategic Blue Nile town."),
        ("scales", "VENEZUELA TPS", "Ninth Circuit stay expires today; court update due for TPS holders."),
        ("sun", "PHILIPPINES", "PAGASA: 'danger' heat index in five areas; classes suspended."),
        ("shield", "ISRAEL", "Beit Shemesh clashes over a draft-dodger arrest; police car window smashed."),
        ("pawn", "CHESS", "Gukesh–Sindarov arrive in Geneva; Game 1 of the title match Tuesday."),
        ("ball", "BADMINTON", "Rakshitha, 19, stuns Olympic champion Chen Yufei at the HK Open."),
        ("bridge", "UKRAINE", "Zelensky tells the superpowers how they can end the war."),
        ("tower", "GAZA", "1,600+ killed since the ceasefire; 2M confined to a third of Gaza."),
    ]
    bw = (CW - 3 * 18) // 4
    brief_bottom = 0
    for i, (ic, reg, txt) in enumerate(briefs):
        r, c = divmod(i, 4)
        bx = M + c * (bw + 18)
        byy = by + 20 + r * 40
        icon(d, ic, bx, byy + 2, 16)
        d.text((bx + 22, byy), reg, font=kicker(9), fill=RED)
        ye = para(d, bx + 22, byy + 12, txt, body(11), bw - 22, leading=12)
        last = wrap(d, txt, body(11), bw - 22)[-1]
        brief_bottom = max(brief_bottom, ye - 12 + d.textbbox((0, 0), last, font=body(11))[3])
    assert brief_bottom + 2 <= 982, f"briefs collide with footer rule: bottom={brief_bottom}"
    rule(d, M, 982, CW, INK, 1)

    # ---- footer ticker
    tick = "COP31 CLOSES IN ANTALYA  ·  NETANYAHU: IRAN OPERATION 'UNAVOIDABLE'  ·  AKVAN LANDFALL FORECAST NOON  ·  GUKESH–SINDAROV GAME 1 TUESDAY"
    tick2 = "WORLD CHILDREN'S DAY  ·  SUDAN: BLUE NILE TOWN CLAIMS  ·  VENEZUELA TPS COURT DATE  ·  JAPAN CPI 2.3%"
    cr = "Drawn by an AI agent · sources: Reuters, Kyiv Independent, ANI, Japan Times, GMA, AA, FIDE, Sudan Tribune"
    assert tw(d, tick, mono(10)) <= CW and tw(d, tick2, mono(10)) <= CW, "ticker runs off page"
    assert W - M - tw(d, cr, mono(9)) >= M, "credit runs off page"
    assert 1012 + d.textbbox((0, 0), cr, font=mono(9))[3] <= H, "credit clipped at bottom"
    d.text((M, 988), tick, font=mono(10), fill=FAINT)
    d.text((M, 1001), tick2, font=mono(10), fill=FAINT)
    d.text((W - M - tw(d, cr, mono(9)), 1012), cr, font=mono(9), fill=(160, 154, 140))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
