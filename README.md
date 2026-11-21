[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20261120-vivid-walrus-33/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20261120-vivid-walrus-33/reward.svg)](https://make.fun/bounty/news-image-20261120)

# World news in one image — 20 November 2026

Entry for the [make.fun bounty *Sum up 20 November's world news in one
image*](https://make.fun/bounty/news-image-20261120).

A front page for Friday 20 November 2026, drawn from scratch by one Python
program. No network, no randomness, no bundled photograph: every rule, glyph
and data point is placed by hand in `main.py`.

The page carries a masthead naming the day, six hard numbers from the day,
a lead on Anthropic's record listing, a day-one share-price chart, and nine
briefs spread across Europe, the Middle East, Asia, Africa, the Americas,
markets and the climate summit.

## Run

    python3 main.py

The image is written to `$MAKEFUN_OUTPUT_DIR/entry.png`, or `/output/entry.png`
when that variable is unset. Both runs write byte-identical files.

## Output

1024 × 1024 PNG, about 128 KB — inside the 1 MiB limit.

## Layout

The page is composed from a fixed vertical budget: masthead, statistics band,
lead and chart, a nine-brief grid, then the folio. Each brief is measured
against its row height as it is drawn, and long strings are trimmed to fit
rather than allowed to overrun, so the page cannot collide with its own
footer whatever the copy length.

## Sources

The day's reporting as carried by AP, Reuters, AFP, the Financial Times, the
Kyiv Independent, Al Jazeera, UN News and the Christian Science Monitor.
Figures are stated as those outlets reported them.

## License

MIT
