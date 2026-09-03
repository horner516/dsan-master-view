#!/usr/bin/env python3
"""Generate the Windows icon from the D’S mark used by the viewer."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "dsan-master-view.ico"
SIZE = 256
image = Image.new("RGBA", (SIZE, SIZE), "#111d27")
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((7, 7, SIZE - 8, SIZE - 8), radius=58, outline="#365267", width=8)
font_paths = [
    Path("C:/Windows/Fonts/arialbd.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]
font_path = next((path for path in font_paths if path.exists()), None)
font = ImageFont.truetype(str(font_path), 92) if font_path else ImageFont.load_default()
text = "D’S"
bounds = draw.textbbox((0, 0), text, font=font)
x = (SIZE - (bounds[2] - bounds[0])) / 2 - 3
y = (SIZE - (bounds[3] - bounds[1])) / 2 - bounds[1]
draw.text((x, y), text, font=font, fill="#4dd6e8")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
image.save(OUTPUT, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print(OUTPUT)
