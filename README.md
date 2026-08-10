# 🐧 Tux & Friends — a Neko.js fork

A JavaScript desktop pet that follows your cursor around the page — except instead of a cat, you get to pick from Tux, GNU, Go Gopher, or Ferris the crab.

[Live Demo](https://aaditya-dakhore.github.io/tux-pet-js/) | [Usage](#usage) | [GitHub](https://github.com/aaditya-dakhore/tux-pet-js)

## About

This is a fork of [Neko.js](https://github.com/louisabraham/nekojs) by Louis Abraham, which is itself a faithful JS reimplementation of the classic [Neko](https://en.wikipedia.org/wiki/Neko_(software)) desktop pet.

I originally found this while wandering and it felt good. The Niko was amazing, so I decided to have Tux as pet and then eventually get the "Tux & Friends".
<!-- Your turn — a couple sentences on why you built this. What made you want
Tux and friends instead of the cat? Keep it short and honest, that's what
makes a README feel real. -->

Rather than one hardcoded pet, this fork adds a small mascot registry and a settings panel so you can switch between characters live, on the same page, without a reload.

### Features

- 🎯 **Follows your cursor** — same chase/idle/sleep behavior as the original Neko
- 🔀 **Switchable mascots** — pick Tux, GNU, Go Gopher, or Ferris from an in-page dropdown
- 🎨 **Pixel-art sprites**, generated with [PixelLab](https://www.pixellab.ai/) and hand-checked for consistency
- ⚙️ **Adjustable speed** — a slider in the same settings panel
- 🚀 **Zero dependencies** — pure vanilla JavaScript, sprites bundled as base64 so it's a single-file include
- 🖱️ **Interactive** — click to cycle behavior modes, just like the original

## Usage

Add to your HTML:

```html
<script src="https://aaditya-dakhore.github.io/tux-pet-js/neko.js" data-autostart></script>
```

Or with custom options:

```javascript
const neko = createNeko({
  mascot: "tux",             // "tux" | "gnu" | "gopher" | "ferris" (default: first registered)
  speed: 24,                 // Pixels per logic tick (default: 24, 5 ticks/sec)
  fps: 120,                  // Render frame rate (default: 120)
  behaviorMode: 0,           // 0=chase, 1=run away, 2=random, 3=pace, 4=ball chase
  idleThreshold: 6,          // Distance to consider idle (default: 6)
  allowBehaviorChange: true, // Click to cycle behaviors (default: true)
  awakeTime: 3,              // Ticks before waking from idle (default: 3)
  awakeRandomRange: 20,      // Extra random ticks added to awakeTime (default: 20)
  controls: true,            // Show the mascot/speed picker panel (default: true)
  startX: 0,
  startY: 0
});

neko.setMascot("gnu");       // switch mascot at any time
neko.start();
neko.stop();
neko.destroy();
```

To build (bundles the sprites into `docs/neko.js`), run `python3 build.py` — no dependencies needed, it just reads the PNGs and base64-encodes them.

### Adding a new mascot

1. Generate/collect 32 sprites (see `build.py`'s frame-index mapping) and drop them numbered `00.png`–`31.png` into `assets/<mascot-id>/`.
2. Add an entry to the `MASCOTS` dict at the top of `build.py` with a `name`, `spriteSize`, and `credit`.
3. Rebuild with `python3 build.py`.

## Mascots & credits

| Mascot | Character credit | License |
|---|---|---|
| Tux | Larry Ewing | Free to use/modify with attribution |
| GNU | The GNU Project / FSF | GNU Project mascot guidelines |
| Go Gopher | Renée French | CC BY 4.0 |
| Ferris | Karen Rustad Tölva | CC0 (public domain) |

All sprite art in this fork was pixel-art-generated with [PixelLab](https://www.pixellab.ai/) based on each character's official design, not traced or copied from existing sprite sheets.

This project builds on:
- [Neko.js](https://github.com/louisabraham/nekojs) by Louis Abraham — the JS engine, state machine, and movement logic this fork is built on top of
- The original [Neko98](https://web.archive.org/web/20050330224958fw_/http://www.angelfire.com/ct/neko/download.html) C++ implementation by David Harvey (1998)
- The original [Neko](https://en.wikipedia.org/wiki/Neko_(software)) concept by Masayuki Koba

## License

The code is licensed under **GNU General Public License v3.0**, same as upstream Neko.js — see [LICENSE.md](LICENSE.md).

Sprite artwork follows each mascot's own license, listed in the table above — not GPL.
