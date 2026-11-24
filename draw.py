#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page (1024x1024 PNG).

Nine stories, all dated 24 November 2026 by the wires and briefings read
this morning (Spyglass daily briefing, Times of India, WH News): a lead on
Nvidia reinstating Jensen Huang, four cards, four briefs. Broadsheet
layout drawn with PIL only. Deterministic: fixed fonts, no timestamps,
no randomness. Run:  python3 draw.py  ->  entry.png
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (247, 243, 234)
INK = (16, 16, 16)
RED = (176, 32, 32)
BLUE = (24, 72, 150)
GREY = (96, 92, 84)
GREEN = (18, 120, 62)
PANEL = (255, 255, 255)
RULE = (16, 16, 16)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width, max_lines=None):
    """Greedy wrap; returns list of lines, hard-truncated to max_lines."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    if max_lines is not None and len(out) > max_lines:
        out = out[:max_lines]
        out[-1] = out[-1].rstrip(".") + "..."
    return out


def block(draw, x, y, text, fnt, fill, width, leading, max_lines=None):
    """Draw wrapped paragraph; return y below the last line."""
    for line in fit_lines(draw, text, fnt, width, max_lines):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, fill=RED):
    f = load(SANS_B, 20)
    draw.text((x, y), text.upper(), font=f, fill=fill)
    return y + 28


def headline(draw, x, y, text, size, width, max_lines, leading=None):
    f = load(SERIF_B, size)
    lead = leading or int(size * 1.12)
    return block(draw, x, y, text, f, INK, width, lead, max_lines)


def deck(draw, x, y, text, size, width, max_lines):
    f = load(SANS, size)
    return block(draw, x, y, text, f, INK, width, int(size * 1.3), max_lines)


def draw_chart(draw, x, y, w, h):
    """Small NVDA panel: rising line, +31% and a chip glyph."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=PANEL)
    draw.text((x + 16, y + 12), "NVDA", font=load(SANS_B, 26), fill=INK)
    draw.text((x + 16, y + 46), "+31% in a day", font=load(SANS_B, 34),
              fill=GREEN)
    pts = [(x + 24, y + h - 46), (x + 70, y + h - 62), (x + 120, y + h - 54),
           (x + 175, y + h - 88), (x + 230, y + h - 118), (x + w - 24, y + 108)]
    draw.line(pts, fill=GREEN, width=5, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx - 4, hy + 16), (hx + 18, hy + 2), (hx - 2, hy - 12)],
                 fill=GREEN)
    draw.text((x + 16, y + h - 34), "Shares surge on his return",
              font=load(SANS, 19), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    right = W - MARGIN

    # ---- Masthead -------------------------------------------------------
    rule(d, MARGIN, right, 44, width=4)
    d.text((MARGIN, 56), "THE WORLD IN ONE DAY",
           font=load(SERIF_B, 62), fill=INK)
    d.text((MARGIN, 128), "TUESDAY, 24 NOVEMBER 2026  •  ONE DAY'S WORLD NEWS",
           font=load(SANS_B, 24), fill=RED)
    rule(d, MARGIN, right, 168, width=2)

    # ---- Lead: Nvidia / Huang ------------------------------------------
    y = 188
    y = kicker(d, MARGIN, y, "Lead — Business")
    y = headline(d, MARGIN, y, "Huang back as Nvidia chief",
                 50, 600, 2)
    y = deck(d, MARGIN, y + 6,
             "The board unanimously reinstates Jensen Huang as chief "
             "executive, eleven days after he resigned over revelations "
             "of extramarital affairs.",
             23, 600, 3)
    d.text((MARGIN, y + 4),
           "Trump backed his return; Democrats raise questions.",
           font=load(SANS, 21), fill=GREY)
    draw_chart(d, 688, 196, 300, 252)

    rule(d, MARGIN, right, 470, width=2)

    # ---- Four cards -----------------------------------------------------
    cards = [
        ("Europe", "EU proposes 22nd Russia sanctions",
         "Brussels targets banks, crypto and ex-combatants, and would "
         "bar Russian teams."),
        ("Ukraine", "Kyiv claims sinking of Russian warship",
         "Ukraine says it sank a corvette off Libya; strikes near "
         "Kyiv kill 11."),
        ("Middle East", "Iran hits Gulf sites as US tightens screws",
         "Tehran steps up attacks on US bases after a lull; US "
         "sanctions 'shadow banking'."),
        ("Asia", "Russian jets enter South Korea zone",
         "Seoul issues an emergency alert for Ulleung Island after "
         "the incursion."),
    ]
    cw = (right - MARGIN - 24) // 2
    ch = 148
    for i, (kick, head, body) in enumerate(cards):
        cx = MARGIN + (i % 2) * (cw + 24)
        cy = 492 + (i // 2) * (ch + 12)
        d.rectangle([cx, cy, cx + cw, cy + ch], outline=GREY, width=1)
        kicker(d, cx + 14, cy + 8, kick)
        headline(d, cx + 14, cy + 36, head, 27, cw - 28, 2, leading=30)
        deck(d, cx + 14, cy + 100, body, 18, cw - 28, 2)

    rule(d, MARGIN, right, 808, width=2)

    # ---- Four briefs ----------------------------------------------------
    briefs = [
        ("SPAIN", "Polls put the right on course to oust Sánchez in the "
                  "29 November election."),
        ("MEXICO", "Troops capture alleged drug lord 'El Chapo Isidro'; "
                   "he will be tried at home."),
        ("BRAZIL", "Court summons Flávio Bolsonaro over alleged slander "
                   "of Lula; growth cut to 1.8%."),
        ("GAZA", "Israeli strikes kill three, incl. an UNRWA worker; "
                 "Oxfam warns of decades of harm."),
    ]
    y = 820
    d.text((MARGIN, y), "IN BRIEF", font=load(SANS_B, 22), fill=RED)
    y += 30
    for tag, text in briefs:
        d.rectangle([MARGIN, y + 6, MARGIN + 12, y + 18], fill=RED)
        d.text((MARGIN + 22, y), tag, font=load(SANS_B, 20), fill=INK)
        tag_w = d.textlength(tag, font=load(SANS_B, 20))
        deck(d, MARGIN + 22 + tag_w + 12, y, text, 20, right - (MARGIN + 34 + tag_w), 1)
        y += 33

    # ---- Footer ---------------------------------------------------------
    rule(d, MARGIN, right, 992, width=1, fill=GREY)
    d.text((MARGIN, 1000), "All events of 24 November 2026, as reported that day.",
           font=load(SANS, 17), fill=GREY)

    img.save("entry.png", optimize=True)
    print("entry.png written")


if __name__ == "__main__":
    main()
