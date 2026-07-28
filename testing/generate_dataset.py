"""
generate_dataset.py
Membuat citra uji sintetis dengan ground truth yang PASTI diketahui,
untuk 3 skenario pengujian OCR:
  1. Ideal (pencahayaan baik, tidak miring)
  2. Bayangan / kontras rendah
  3. Miring (skewed)
"""
import os
import csv
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = "dataset"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PATH_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

samples = [
    # (filename, ground_truth_text, scenario)
    ("doc_01.jpg", "INFORMATIKA ITTS", 1),
    ("doc_02.jpg", "VISI KOMPUTER 2026", 1),
    ("doc_03.jpg", "LAPORAN PROYEK UAS", 1),
    ("doc_04.jpg", "SISTEM DETEKSI TEKS", 1),
    ("struk_01.jpg", "TOTAL BELANJA RP150000", 2),
    ("struk_02.jpg", "TERIMA KASIH", 2),
    ("struk_03.jpg", "STRUK PEMBAYARAN TOKO", 2),
    ("struk_04.jpg", "KEMBALIAN RP5000", 2),
    ("papan_01.jpg", "OCR SYSTEM TEST", 3),
    ("papan_02.jpg", "DILARANG PARKIR", 3),
    ("papan_03.jpg", "PINTU DARURAT", 3),
    ("papan_04.jpg", "AREA PARKIR KHUSUS", 3),
]

def make_base_image(text, size=(700, 220), font_size=48):
    img = Image.new("RGB", size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((size[0] - w) / 2 - bbox[0], (size[1] - h) / 2 - bbox[1])
    draw.text(pos, text, font=font, fill=(15, 15, 15))
    return img

def add_shadow(img, strength=0.55):
    """Tambahkan gradasi bayangan / pencahayaan tidak merata."""
    w, h = img.size
    arr = np.array(img).astype(np.float32)
    gradient = np.tile(np.linspace(1.0, strength, w), (h, 1))
    for c in range(3):
        arr[:, :, c] = arr[:, :, c] * gradient + (255 * (1 - gradient) * 0.15)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    out = Image.fromarray(arr)
    out = out.filter(ImageFilter.GaussianBlur(radius=0.6))
    # tambahkan noise ringan
    noise = np.random.normal(0, 8, (h, w, 3))
    arr2 = np.array(out).astype(np.float32) + noise
    arr2 = np.clip(arr2, 0, 255).astype(np.uint8)
    return Image.fromarray(arr2)

def add_skew(img, angle=12):
    """Rotasikan citra untuk mensimulasikan pengambilan gambar miring."""
    return img.rotate(angle, expand=True, fillcolor=(255, 255, 255), resample=Image.BICUBIC)

rows = []
for fname, text, scenario in samples:
    img = make_base_image(text)
    if scenario == 2:
        img = add_shadow(img, strength=0.45)
    elif scenario == 3:
        img = add_skew(img, angle=10)
    path = os.path.join(OUT_DIR, fname)
    img.save(path, quality=90)
    rows.append((fname, text, scenario))
    print(f"generated {path}")

with open(os.path.join(OUT_DIR, "ground_truth.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "text", "scenario"])
    for r in rows:
        writer.writerow(r)

print("Selesai. Total citra:", len(rows))
