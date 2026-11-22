#!/usr/bin/env python3
"""Draw THE WORLD front page for Sunday, 22 November 2026.

A one-page newspaper image summing up the day's world news, drawn with PIL
from the verified headlines of 22 November 2026. Deterministic: same input
always writes the same bytes. Run: python3 draw_news.py  -> entry.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (178, 28, 28)
NAVY = (15, 30, 58)
SEA = (23, 58, 94)
GREY = (90, 86, 76)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, name, start_size, max_w, min_size=10):
    """Largest size (<= start_size) at which text fits max_w."""
    size = start_size
    while size > min_size:
        fnt = font(name, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(name, min_size)


def draw_lead_scene(draw, x0, y0, x1, y1):
    """Night scene over the Gulf: dark sky, missile arcs, sea, labels."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # stars
    stars = [(x0 + 30, y0 + 22), (x0 + 90, y0 + 48), (x0 + 160, y0 + 18),
             (x0 + 230, y0 + 40), (x0 + 300, y0 + 24), (x0 + 55, y0 + 80),
             (x0 + 200, y0 + 92), (x0 + 275, y0 + 78), (x0 + 130, y0 + 60)]
    for sx, sy in stars:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(230, 230, 210))
    # missile arcs (glow orange under, white core over)
    arcs = [
        [(x0 + 20, y0 + 150), (x0 + 90, y0 + 95), (x0 + 170, y0 + 70)],
        [(x0 + 120, y0 + 165), (x0 + 190, y0 + 105), (x0 + 260, y0 + 88)],
        [(x0 + 220, y0 + 175), (x0 + 285, y0 + 120), (x0 + 330, y0 + 108)],
    ]
    for arc in arcs:
        draw.line(arc, fill=(255, 140, 40), width=7, joint="curve")
        draw.line(arc, fill=(255, 240, 200), width=2, joint="curve")
        hx, hy = arc[-1]
        draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(255, 200, 90))
    # sea
    sea_y = y1 - 78
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    draw.line([x0, sea_y, x1, sea_y], fill=(120, 170, 220), width=2)
    # Bahrain marker
    bx, by = x0 + 268, sea_y + 42
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 210, 90),
                 outline=(255, 255, 255), width=2)
    # labels
    lab = font(SANS_B, 20)
    draw.text((x0 + 14, sea_y + 10), "BAHRAIN", font=lab, fill=(255, 255, 255))
    draw.text((x0 + 14, y1 - 32), "U.S. 5TH FLEET", font=font(SANS_B, 16),
              fill=(180, 205, 235))
    draw.text((x1 - 108, y0 + 12), "THE GULF", font=font(SANS_B, 16),
              fill=(150, 175, 205))


def story(draw, x, y, w, kicker, headline, deck):
    """One grid story: kicker, headline (up to 2 lines), deck (up to 3)."""
    draw.text((x, y), kicker, font=font(SANS_B, 17), fill=RED)
    hy = y + 26
    hf = fit_font(draw, headline, SERIF_B, 27, w)
    lines = wrap(draw, headline, hf, w)[:2]
    for line in lines:
        draw.text((x, hy), line, font=hf, fill=INK)
        hy += 33
    df = font(SANS, 18)
    dlines = wrap(draw, deck, df, w)[:3]
    dy = hy + 4
    for line in dlines:
        draw.text((x, dy), line, font=df, fill=(45, 45, 45))
        dy += 23
    return dy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # double border
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    draw.rectangle([21, 21, W - 22, H - 22], outline=INK, width=1)

    # masthead
    mast = fit_font(draw, "THE WORLD", SERIF_B, 96, W - 120)
    mw = draw.textlength("THE WORLD", font=mast)
    draw.text(((W - mw) / 2, 34), "THE WORLD", font=mast, fill=INK)
    draw.line([28, 138, W - 28, 138], fill=INK, width=2)
    date_f = font(SANS_B, 22)
    draw.text((28, 148), "SUNDAY, 22 NOVEMBER 2026", font=date_f, fill=INK)
    right = "THE DAY IN ONE PAGE"
    rw = draw.textlength(right, font=date_f)
    draw.text((W - 28 - rw, 148), right, font=date_f, fill=INK)
    draw.line([28, 180, W - 28, 180], fill=INK, width=1)

    # ---- lead story ----
    lx, lw = 28, 596
    draw.text((lx, 196), "GULF ON EDGE", font=font(SANS_B, 23), fill=RED)
    lead_head = ["IRAN STRIKES U.S.", "BASES IN BAHRAIN"]
    hy = 226
    hf = font(SERIF_B, 56)
    for line in lead_head:
        hf = fit_font(draw, line, SERIF_B, hf.size, lw)
    for line in lead_head:
        draw.text((lx, hy), line, font=hf, fill=INK)
        hy += 64
    deck_f = font(SANS, 21)
    deck = ("IRGC claims missile and drone hits on Patriot radars at "
            "al-Riffa and Awali; Bahrain says a factory was hit and no "
            "one was hurt. Two accounts, one dangerous night.")
    dy = hy + 8
    for line in wrap(draw, deck, deck_f, lw):
        draw.text((lx, dy), line, font=deck_f, fill=(45, 45, 45))
        dy += 26
    # sidebar fact under the deck, filling the lead block
    draw.line([lx, dy + 6, lx + lw, dy + 6], fill=(180, 175, 160), width=1)
    also_f = font(SANS, 18)
    also = "ALSO: U.S. Central Command denies Iran\u2019s F-16 claim."
    ay = dy + 16
    for line in wrap(draw, also, also_f, lw):
        draw.text((lx, ay), line, font=also_f, fill=(45, 45, 45))
        ay += 22
    # lead illustration, right of the lead text
    draw_lead_scene(draw, 648, 196, 996, 512)

    draw.line([28, 528, W - 28, 528], fill=INK, width=2)

    # ---- six-story grid ----
    col_w = 464
    cols = [28, 532]
    rows = [546, 686, 826]
    stories = [
        ("UKRAINE", "RUSSIA'S NIGHT OF FIRE",
         "50+ missiles, ~500 drones in an overnight barrage. Lviv hit; "
         "missiles land in Poland."),
        ("TRADE", "EU\u2013INDONESIA SIGN LANDMARK DEAL",
         "After a decade of talks, CEPA is signed in Brussels; tariffs to "
         "fall on 98.5% of goods."),
        ("CLIMATE", "COP31 DEADLOCK IN OVERTIME",
         "Antalya talks spill past their deadline as fossil-fuel language "
         "drops from the draft."),
        ("DIPLOMACY", "ENVOYS TO MOSCOW AFTER ABU DHABI",
         "Kushner and Witkoff to brief Putin, then meet Zelensky in Dublin. "
         "A prisoner swap is agreed."),
        ("MEXICO", "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
         "FBI most-wanted cartel boss seized in a Sinaloa raid; 11 dead as "
         "violence flares."),
        ("HONG KONG", "HONG KONG VOTES",
         "856 candidates contest 723 Election Committee seats; turnout "
         "tops 98% by 5 p.m."),
    ]
    for i, (kick, head, dk) in enumerate(stories):
        x = cols[i % 2]
        y = rows[i // 2]
        story(draw, x, y, col_w, kick, head, dk)
        if i % 2 == 0:
            draw.line([512, y + 4, 512, y + 128], fill=(180, 175, 160), width=1)

    # ---- footer ----
    draw.line([28, 968, W - 28, 968], fill=INK, width=1)
    foot = "THE WORLD  \u00b7  Sunday, 22 November 2026"
    ff = font(SANS_B, 17)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 976), foot, font=ff, fill=INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
