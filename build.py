#!/usr/bin/env python3
"""
Build script for Neko.js - multi-mascot edition
Loads numbered PNG sprites per mascot and bundles with JavaScript
"""

import base64
from pathlib import Path

# Register each mascot here. spriteSize = the ACTUAL pixel dimensions
# of that mascot's PNGs (check yours before setting this).
MASCOTS = {
    "tux": {
        "name": "Tux",
        "folder": "tux",
        "spriteSize": 56,
        "credit": "Tux by Larry Ewing, sprites generated with PixelLab",
    },
    "gnu": {
        "name": "GNU",
        "folder": "gnu",
        "spriteSize": 56,
        "credit": "GNU mascot (FSF/GNU Project), sprites generated with PixelLab",
    },
    "gopher": {
        "name": "Go Gopher",
        "folder": "gopher",
        "spriteSize": 56,
        "credit": "Go gopher by Renée French, CC BY 4.0, sprites generated with PixelLab",
    },
    "ferris": {
        "name": "Ferris",
        "folder": "ferris",
        "spriteSize": 56,
        "credit": "Ferris by Karen Rustad Tölva, CC0, sprites generated with PixelLab",
    },
}


def convert_png_to_base64(png_path):
    with open(png_path, "rb") as f:
        png_data = f.read()
    b64_data = base64.b64encode(png_data).decode("ascii")
    return f"data:image/png;base64,{b64_data}"


def load_mascot_sprites(assets_dir, folder):
    sprites = []
    for i in range(32):
        sprite_path = assets_dir / folder / f"{i:02d}.png"
        if not sprite_path.exists():
            print(f"  Warning: {sprite_path} not found, skipping")
            sprites.append("")
            continue
        sprites.append(convert_png_to_base64(sprite_path))
    return sprites


def build():
    script_dir = Path(__file__).parent
    assets_dir = script_dir / "assets"
    src_dir = script_dir / "src"
    docs_dir = script_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    print("Converting mascot sprites to base64...")
    mascot_entries = []
    for mascot_id, meta in MASCOTS.items():
        print(f"  Mascot: {meta['name']}")
        sprites = load_mascot_sprites(assets_dir, meta["folder"])
        sprites_js = ",\n        ".join(f'"{s}"' if s else '""' for s in sprites)
        entry = f'''  "{mascot_id}": {{
    name: "{meta['name']}",
    spriteSize: {meta['spriteSize']},
    credit: "{meta['credit']}",
    sprites: [
        {sprites_js}
    ]
  }}'''
        mascot_entries.append(entry)

    mascots_js = ",\n".join(mascot_entries)

    print("Reading JavaScript source...")
    js_source = (src_dir / "main.js").read_text()

    lines = js_source.split("\n")
    in_code = False
    code_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("(function") and "{" in stripped:
            in_code = True
            continue
        elif stripped in ["})();", "}());"]:
            in_code = False
            continue
        elif in_code:
            if stripped == "'use strict';" or stripped == '"use strict";':
                continue
            code_lines.append(line)

    code_js = "\n".join(code_lines)

    template = f'''/**
 * Neko.js - Bundled version (multi-mascot edition)
 * Based on Neko98 by David Harvey (1998)
 * Original Neko by Masayuki Koba
 * Licensed under GPL v3 (see LICENSE.md)
 */

(function() {{
    "use strict";

    const MASCOTS = {{
{mascots_js}
    }};

{code_js}

    window.createNeko = function(options) {{
        const neko = new Neko(options);
        neko.mascots = MASCOTS;
        const initialId = (options && options.mascot) || Object.keys(MASCOTS)[0];
        neko.setMascot(initialId);
        if (!options || options.controls !== false) {{
            neko.createControls();
        }}
        neko.start();
        return neko;
    }};

    if (document.currentScript && document.currentScript.hasAttribute("data-autostart")) {{
        if (document.readyState === "loading") {{
            document.addEventListener("DOMContentLoaded", function() {{
                window.neko = createNeko();
            }});
        }} else {{
            window.neko = createNeko();
        }}
    }}
}})();
'''

    output_path = docs_dir / "neko.js"
    print(f"Writing to {output_path}...")
    output_path.write_text(template)

    size_kb = output_path.stat().st_size / 1024
    print(f"Done! Output size: {size_kb:.1f} KB (mascots: {', '.join(MASCOTS.keys())})")


if __name__ == "__main__":
    build()