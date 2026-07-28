"""
main.py
Entry point untuk menjalankan pipeline OCR end-to-end lewat command line.

Contoh penggunaan:
    python src/main.py --image data/sample_images/contoh1.jpg --engine tesseract
    python src/main.py --image data/sample_images/contoh1.jpg --engine easyocr
"""

import argparse

from preprocessing import preprocess_pipeline
from ocr_model import run_ocr
from utils import save_text_output


def main():
    parser = argparse.ArgumentParser(description="Pipeline OCR sederhana")
    parser.add_argument("--image", required=True, help="Path ke file gambar")
    parser.add_argument(
        "--engine",
        default="tesseract",
        choices=["tesseract", "easyocr"],
        help="Engine OCR yang digunakan",
    )
    parser.add_argument("--lang", default="ind+eng", help="Kode bahasa (khusus Tesseract)")
    parser.add_argument("--output", default="output.txt", help="Path file output teks")
    args = parser.parse_args()

    print(f"[1/3] Preprocessing gambar: {args.image}")
    processed = preprocess_pipeline(args.image)

    print(f"[2/3] Menjalankan OCR dengan engine: {args.engine}")
    hasil_teks = run_ocr(
        args.image, processed_image=processed, engine=args.engine, lang=args.lang
    )

    print("[3/3] Menyimpan hasil...")
    save_text_output(hasil_teks, args.output)

    print("\n=== Hasil OCR ===")
    print(hasil_teks)


if __name__ == "__main__":
    main()
