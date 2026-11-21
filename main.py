#!/usr/bin/env python3
"""Draws one 1024x1024 front page summing up the world news of 20 November 2026.

Everything is hand-placed geometry and hand-set type: no network, no
randomness, no external assets beyond the DejaVu faces that ship with the
system. Two runs on the same machine write byte-identical files.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# ---------------------------------------------------------------- palette
INK = (26, 24, 22)
PAPER = (247, 243, 234)
RULE = (42, 39, 35)
RED = (168, 32, 38)
TEAL = (18, 82, 86)
GREY = (104, 99, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
MONO = "DejaVuSansMono-Bold.ttf"
DATE = "FRIDAY 20 NOVEMBER 2026"

LEAD = {
    "kicker": "MARKETS  ·  TECHNOLOGY",
    "head": "Anthropic opens at $2.01tn in the largest listing on record",
    "deck": "Shares in the AI group jumped 34% above their $83 offer price "
            "before settling near $100, valuing it at about $1.8tn. The debut "
            "came as chip and AI stocks sold off around the world.",
    "source": "AP  ·  Reuters  ·  Financial Times",
}

STATS = [
    ("$81.3bn", "raised, the biggest IPO ever"),
    ("$2.01tn", "value at the first trade"),
    ("98", "drones and missiles fired at Kyiv"),
    ("1", "killed in Kyiv, four more injured"),
    ("25", "countries saw youth protests"),
    ("0", "fossil-fuel mentions in the COP31 draft"),
]

# Nine briefs, three per column. Deliberately ordered by weight.
BRIEFS = [
    ("EUROPE", "Missiles land in Poland as 11 nations drill",
     "Warsaw called the Russian strike a provocation timed to the exercises."),
    ("CLIMATE", "COP31 ends in deadlock; activists shout 'shame'",
     "No pledge to phase out coal, oil and gas. The text stayed voluntary."),
    ("ARCTIC", "Denmark backs the Greenland defence deal",
     "The vote lets the US add bases and build for its Golden Dome shield."),
    ("BRITAIN", "UK and EU hold their first summit since Brexit",
     "Burnham agreed trade terms and a youth mobility plan in Brussels."),
    ("ASIA", "Myanmar calls the genocide ruling 'unfair'",
     "The ICJ voted 9 to 6 that the army committed genocide in 2017."),
    ("MIDEAST", "Saudi jets hit Hodeidah; Houthis fire on Riyadh",
     "The coalition struck smuggling sites and intercepted five drones."),
    ("AFRICA", "Deportees in South Sudan 'went hungry', families say",
     "Guards are accused of taking money sent in for food."),
    ("TRADE", "Chip selloff wipes $4tn off the 'Miserable 7'",
     "Nvidia and TSMC led a worldwide slide in AI and chip shares."),
    ("RIGHTS", "'Killer robot' talks end without a treaty",
     "Russia blocked binding rules on weapons that pick targets alone."),
]


# ---------------------------------------------------------------- helpers
def face(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit(draw, text, font, width, max_lines):
    """Wrap, then trim to at most max_lines with an ellipsis if it overruns."""
    lines = wrap(draw, text, font, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=font) > width:
        last = last[:-1]
    lines[-1] = last.rstrip() + "…"
    return lines


def block(draw, lines, font, x, y, size, colour=INK, leading=1.24):
    step = int(size * leading)
    for i, line in enumerate(lines):
        draw.text((x, y + i * step), line, font=font, fill=colour)
    return y + len(lines) * step


# ---------------------------------------------------------------- pieces
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 8], fill=TEAL)
    draw.text((36, 24), "THE WORLD, ONE DAY AT A TIME", font=face(BOLD, 16),
              fill=TEAL)
    draw.text((W - 36, 24), "FRONT PAGE  ·  No. 1,204", font=face(SANS, 14),
              fill=GREY, anchor="ra")

    date_font = face(BOLD, 58)
    while draw.textlength(DATE, font=date_font) > W - 72:
        date_font = face(BOLD, date_font.size - 2)
    draw.text((36, 48), DATE, font=date_font, fill=INK)
    draw.rectangle([36, 120, W - 36, 126], fill=RED)
    return 138


def draw_stats(draw, y):
    num_font = face(MONO, 26)
    cap_font = face(SANS, 12)
    col_w = (W - 72) // 3
    for i, (num, cap) in enumerate(STATS):
        cx = 36 + (i % 3) * col_w
        cy = y + (i // 3) * 62
        draw.text((cx, cy), num, font=num_font, fill=RED)
        block(draw, fit(draw, cap, cap_font, col_w - 18, 2),
              cap_font, cx, cy + 32, 12, GREY, 1.16)
    return y + 128


def draw_chart(draw, x, y, w, h):
    """The lead's one illustration: the first day of the listing as a line."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 253, 246),
                   outline=RULE, width=2)
    pad = 26
    plot_x, plot_y = x + pad, y + 34
    plot_w, plot_h = w - pad * 2, h - 78

    for i in range(5):
        gy = plot_y + plot_h * i / 4
        draw.line([plot_x, gy, plot_x + plot_w, gy], fill=(216, 210, 199), width=1)

    pts = [(0.00, 83), (0.16, 111.5), (0.34, 104), (0.55, 99),
           (0.74, 101), (1.00, 100)]
    lo, hi = 74, 118
    xy = [(plot_x + px * plot_w, plot_y + plot_h - (v - lo) / (hi - lo) * plot_h)
          for px, v in pts]
    draw.line(xy, fill=TEAL, width=4, joint="curve")
    for point in xy:
        draw.ellipse([point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4],
                     fill=PAPER, outline=TEAL, width=2)

    draw.text((plot_x, y + 10), "SHARE PRICE, DAY ONE, US$", font=face(BOLD, 12),
              fill=GREY)
    draw.text((plot_x + plot_w, xy[1][1] - 22), "$111.50 high",
              font=face(BOLD, 14), fill=RED, anchor="ra")
    draw.text((plot_x, plot_y + plot_h + 6), "offer $83",
              font=face(SANS, 13), fill=GREY)
    draw.text((plot_x + plot_w, plot_y + plot_h + 6), "close ~$100",
              font=face(SANS, 13), fill=GREY, anchor="ra")


def draw_lead(draw, y):
    art_w = 380
    art_x = W - 36 - art_w
    text_w = art_x - 58

    draw.text((36, y), LEAD["kicker"], font=face(BOLD, 14), fill=RED)

    head_font = face(BOLD, 38)
    y2 = block(draw, fit(draw, LEAD["head"], head_font, text_w, 3),
               head_font, 36, y + 26, 38, INK, 1.1)

    deck_font = face(SANS, 16)
    y2 = block(draw, fit(draw, LEAD["deck"], deck_font, text_w, 5),
               deck_font, 36, y2 + 10, 16, INK, 1.32)

    draw.text((36, y2 + 8), LEAD["source"], font=face(SANS, 12), fill=GREY)
    draw_chart(draw, art_x, y, art_w, 244)
    return y + 262


def draw_columns(draw, y, bottom):
    gap = 20
    cols = 3
    col_w = (W - 72 - gap * (cols - 1)) // cols
    per_col = len(BRIEFS) // cols
    tag_font = face(BOLD, 12)
    head_font = face(BOLD, 19)
    body_font = face(SANS, 13)
    avail = bottom - y
    row_h = avail // per_col

    for c in range(cols):
        x = 36 + c * (col_w + gap)
        for r, (region, head, body) in enumerate(
                BRIEFS[c * per_col:(c + 1) * per_col]):
            cy = y + r * row_h
            draw.line([x, cy, x + col_w, cy], fill=RULE, width=2)
            draw.text((x, cy + 7), region, font=tag_font, fill=TEAL)
            cy = block(draw, fit(draw, head, head_font, col_w, 2),
                       head_font, x, cy + 23, 19, INK, 1.13)
            block(draw, fit(draw, body, body_font, col_w, 2),
                  body_font, x, cy + 4, 13, INK, 1.28)


def draw_footer(draw, y):
    # Counts are derived from BRIEFS so the recap can never drift from the page.
    tally = {}
    for region, _, _ in BRIEFS:
        tally[region] = tally.get(region, 0) + 1
    parts = [f"{len(BRIEFS)} stories"] + [f"{k.title()} {v}" for k, v in tally.items()]
    recap = "  ·  ".join(parts)

    draw.line([36, y, W - 36, y], fill=RULE, width=2)
    font = face(SANS, 12)
    while draw.textlength(recap, font=font) > W - 72 and font.size > 8:
        font = face(SANS, font.size - 1)
    draw.text((36, y + 8), recap, font=font, fill=GREY)
    draw.rectangle([0, H - 26, W, H], fill=INK)
    draw.text((36, H - 19), "20 NOVEMBER 2026", font=face(BOLD, 12), fill=PAPER)
    draw.text((W - 36, H - 19), "WORLD NEWS IN ONE IMAGE",
              font=face(BOLD, 12), fill=PAPER, anchor="ra")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = draw_stats(draw, draw_masthead(draw))
    draw.line([36, y + 4, W - 36, y + 4], fill=RULE, width=2)
    y = draw_lead(draw, y + 18)
    draw.line([36, y, W - 36, y], fill=RULE, width=3)
    draw_columns(draw, y + 14, H - 56)
    draw_footer(draw, H - 50)

    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path}: {img.size[0]}x{img.size[1]}, "
          f"{os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
