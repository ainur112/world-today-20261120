# world-today-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ainur112/world-today-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ainur112/world-today-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One broadsheet front page — **The World Today, Friday 20 November 2026** — summarising the day's world news in a single 1024×1024 image: 16 stories across conflict, geopolitics, markets, climate, weather, justice and sport, from Russia's five-wave overnight missile assault on Kyiv to Netanyahu's "unavoidable" Iran warning, Cyclone Akvan's landfall day, COP31's thin adaptation-finance close, Japan's CPI print and World Children's Day. Every illustration is drawn programmatically with Pillow; every fact is sourced and date-verified in [SOURCES.md](SOURCES.md) (items first reported 18–19 Nov were deliberately excluded).

## Run it

```sh
python main.py   # copies entry.png to /output/entry.png (or $MAKEFUN_OUTPUT_DIR)
```

To re-render the image from scratch: `python render.py` (requires Pillow; fonts bundled under `fonts/`, SIL OFL 1.1). The render is deterministic — no clock, random or network — so it produces byte-identical output every run.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
