"""Iz fotografije pitagora.png pripravi slike za mežik v PI.py.

Odstrani sivo ozadje (prosojno ozadje) in nariše tri različice desnega očesa:
  pitagora_odprto.png  - original
  pitagora_priprto.png - veka do polovice očesa
  pitagora_zaprto.png  - zaprto oko

Zagon (iz mape manim-demo):
  .venv\\Scripts\\python.exe assets\\pripravi_pitagoro.py
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ASSETS = Path(__file__).parent
SOURCE = ASSETS / "pitagora.png"

# Desno oko na sliki (v pikslih izvirne slike 554 x 554).
EYE_BOX = (266, 187, 330, 221)  # levo, zgoraj, desno, spodaj
LINE_COLOR = (70, 48, 20)  # temna linija zaprtega očesa
BOTTOM_CUT = 533  # pod to vrstico je le senca magneta na steni


def remove_background(rgb: np.ndarray) -> np.ndarray:
    """Vrne alfa kanal: ozadje (sivo, povezano z robom slike) je prosojno."""
    r, g, b = (rgb[..., i].astype(int) for i in range(3))
    warm = (r - b) > 12  # kip in trak sta topli barvi, ozadje je sivo
    background = ~warm
    labels, _ = ndimage.label(background)
    border = np.unique(
        np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]])
    )
    border = border[border != 0]
    mask = np.isin(labels, border)
    # Manjše luknje v kipu zapolnimo, rob malo zgladimo.
    solid = ndimage.binary_fill_holes(~mask)
    solid = ndimage.binary_opening(solid, iterations=1)
    # Obdržimo le največji kos (kip), ostanke sence odstranimo.
    parts, count = ndimage.label(solid)
    if count > 1:
        sizes = ndimage.sum(solid, parts, range(1, count + 1))
        solid = parts == (1 + int(np.argmax(sizes)))
    solid[BOTTOM_CUT:, :] = False  # senca pod trakom
    alpha = Image.fromarray((solid * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2)
    )
    return np.array(alpha)


def skin_patch(base: Image.Image) -> Image.Image:
    """Koža čez oko: za vsak stolpec preliv med kožo nad in pod očesom."""
    left, top, right, bottom = EYE_BOX
    arr = np.array(base).astype(float)
    pad = 4
    above = arr[top - pad - 3 : top - pad, :, :].mean(axis=0)  # vrstice nad očesom
    below = arr[bottom + pad : bottom + pad + 3, :, :].mean(axis=0)  # pod očesom
    y0, y1 = top - pad, bottom + pad
    t = ((np.arange(arr.shape[0]) - y0) / (y1 - y0)).clip(0, 1)[:, None, None]
    patch = above[None, :, :] * (1 - t) + below[None, :, :] * t
    patch_img = Image.fromarray(patch.clip(0, 255).astype(np.uint8))
    # Vodoravno zgladimo, da ni vidnih prog.
    return patch_img.filter(ImageFilter.GaussianBlur(1.5))


def draw_lid(base: Image.Image, closed_fraction: float) -> Image.Image:
    """Nariše veko, ki pokrije zgornji del očesa (1.0 = popolnoma zaprto)."""
    left, top, right, bottom = EYE_BOX
    lid_bottom = top + (bottom - top) * closed_fraction

    # Mehka maska veke (elipsa, odrezana na želeno višino).
    mask = Image.new("L", base.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((left - 2, top - 2, right + 2, bottom + 2), fill=255)
    md.rectangle((0, lid_bottom + 1, base.width, base.height), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(2.2))

    out = base.copy().convert("RGBA")
    out.paste(skin_patch(base), (0, 0), mask)

    # Rob veke kot vdolbina v kipu: mehka senca + temnejša linija.
    # Pri zaprtem očesu je linija ukrivljena navzdol (◡).
    cx = (left + right) / 2
    half = (right - left) / 2
    closed = closed_fraction >= 1.0
    sag = 6 if closed else 2
    edge_y = (top + bottom) / 2 - 2 if closed else lid_bottom - 1
    points = [
        (x, edge_y + sag * (1 - ((x - cx) / half) ** 2))
        for x in np.linspace(left + 3, right - 3, 40)
    ]

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).line(
        [(x, y + 2) for x, y in points], fill=(110, 85, 45, 110), width=5, joint="curve"
    )
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(2.0)))

    groove = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(groove).line(points, fill=LINE_COLOR + (235,), width=3, joint="curve")
    out.alpha_composite(groove.filter(ImageFilter.GaussianBlur(0.7)))
    return out.convert("RGB")


def main() -> None:
    rgb_image = Image.open(SOURCE).convert("RGB")
    alpha = remove_background(np.array(rgb_image))
    for name, fraction in [("odprto", 0.0), ("priprto", 0.55), ("zaprto", 1.0)]:
        img = rgb_image if fraction == 0 else draw_lid(rgb_image, fraction)
        rgba = img.convert("RGBA")
        rgba.putalpha(Image.fromarray(alpha))
        rgba.save(ASSETS / f"pitagora_{name}.png")
        print("shranjeno:", ASSETS / f"pitagora_{name}.png")


if __name__ == "__main__":
    main()
