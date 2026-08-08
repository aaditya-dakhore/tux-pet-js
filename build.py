#!/usr/bin/env python3
"""
Build script for Neko.js
Loads numbered PNG sprites and bundles with JavaScript
"""

import base64
from pathlib import Path


def convert_png_to_base64(png_path):
    """Read a PNG file and return it as a base64 data URI."""
    with open(png_path, "rb") as f:
        png_data = f.read()
    b64_data = base64.b64encode(png_data).decode("ascii")
    return f"data:image/png;base64,{b64_data}"


def build():
    """Main build function"""
    script_dir = Path(__file__).parent
    assets_dir = script_dir / "assets" / "tux"  # swap folder name to switch mascot later
    src_dir = script_dir / "src"
    docs_dir = script_dir / "docs"

    docs_dir.mkdir(exist_ok=True)

    print("Converting sprites to base64...")
    sprites_b64 = []

    for i in range(32):
        sprite_path = assets_dir / f"{i:02d}.png"
        if not sprite_path.exists():
            print(f"Warning: {sprite_path.name} not found, skipping")
            sprites_b64.append("")
            continue

        print(f"  Converting {sprite_path.name}...")
        sprites_b64.append(convert_png_to_base64(sprite_path))

    print(f"Converted {len([s for s in sprites_b64 if s])} sprites")

    # --- everything below here is unchanged from the original build.py ---

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

    sprites_js = ",\n        ".join(f'"{s}"' if s else '""' for s in sprites_b64)
    code_js = "\n".join(code_lines)

    template = f"""\
/**
 * Neko.js - Bundled version (Tux edition)
 * Based on Neko98 by David Harvey (1998)
 * Original Neko by Masayuki Koba
 * Licensed under GPL v3 (see LICENSE.md)
 */

(function() {{
    "use strict";

    const NEKO_SPRITES = [
        {sprites_js}
    ];

{code_js}

    window.createNeko = function(options) {{
        const neko = new Neko(options);
        neko.setSprites(NEKO_SPRITES);
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
"""

    output_path = docs_dir / "neko.js"
    print(f"Writing to {output_path}...")
    output_path.write_text(template)

    size_kb = output_path.stat().st_size / 1024
    print(f"Done! Output size: {size_kb:.1f} KB")


if __name__ == "__main__":
    build()