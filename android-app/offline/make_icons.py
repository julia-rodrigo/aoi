"""Builds Aoi's Android launcher icons from the app's own icon (aoi-teacher/icons/icon-512.png).

Legacy square/round icons use the art as is. The adaptive icon (Android 8+) puts her on the navy
background layer and scales the art into the centre of the 108dp foreground so launchers that crop
to circles, squircles or teardrops never cut off her face or headphones.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "aoi-teacher", "icons", "icon-512.png")
RES = os.path.join(HERE, "app", "src", "main", "res")
NAVY = (7, 16, 52, 255)
DENSITIES = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}

art = Image.open(SRC).convert("RGBA")
for name, scale in DENSITIES.items():
    out = os.path.join(RES, "mipmap-" + name)
    os.makedirs(out, exist_ok=True)
    legacy = round(48 * scale)
    art.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(out, "ic_launcher.png"))
    round_icon = art.resize((legacy, legacy), Image.LANCZOS)
    mask = Image.new("L", (legacy, legacy), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, legacy - 1, legacy - 1), fill=255)
    round_icon.putalpha(mask)
    round_icon.save(os.path.join(out, "ic_launcher_round.png"))
    fg_size = round(108 * scale)
    face = round(74 * scale)
    fg = Image.new("RGBA", (fg_size, fg_size), NAVY)
    fg.paste(art.resize((face, face), Image.LANCZOS), ((fg_size - face) // 2, (fg_size - face) // 2))
    fg.save(os.path.join(out, "ic_launcher_foreground.png"))
print("icons written to", RES)
