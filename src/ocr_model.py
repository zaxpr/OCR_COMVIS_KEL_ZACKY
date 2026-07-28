"""
ocr_model.py
Wrapper untuk menjalankan proses OCR (ekstraksi teks dari citra)
menggunakan Tesseract atau EasyOCR. Pilih salah satu engine sesuai kebutuhan.
"""

from typing import List


def ocr_with_tesseract(image, lang: str = "ind+eng") -> str:
    """
    Ekstraksi teks menggunakan pytesseract.
    Membutuhkan Tesseract-OCR terinstal di sistem operasi.
    """
    import pytesseract

    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()


def ocr_with_easyocr(image_path: str, lang_list: List[str] = None) -> str:
    """
    Ekstraksi teks menggunakan EasyOCR.
    lang_list contoh: ['en'] atau ['id', 'en'] (cek dukungan bahasa Indonesia di dokumentasi EasyOCR).
    """
    import easyocr

    if lang_list is None:
        lang_list = ["en"]

    reader = easyocr.Reader(lang_list, gpu=False)
    results = reader.readtext(image_path, detail=0)  # detail=0 -> hanya teks
    return " ".join(results).strip()


def run_ocr(image_path: str, processed_image=None, engine: str = "tesseract", lang: str = "ind+eng"):
    """
    Fungsi utama untuk menjalankan OCR.

    Parameters
    ----------
    image_path : str
        Path gambar asli (dipakai untuk EasyOCR).
    processed_image : np.ndarray, optional
        Citra hasil preprocessing (dipakai untuk Tesseract).
    engine : str
        "tesseract" atau "easyocr".
    lang : str
        Kode bahasa untuk Tesseract, contoh "ind+eng".
    """
    if engine == "tesseract":
        if processed_image is None:
            raise ValueError("processed_image wajib diisi untuk engine tesseract")
        return ocr_with_tesseract(processed_image, lang=lang)

    elif engine == "easyocr":
        return ocr_with_easyocr(image_path)

    else:
        raise ValueError(f"Engine tidak dikenal: {engine}")


if __name__ == "__main__":
    import sys
    from preprocessing import preprocess_pipeline

    if len(sys.argv) < 2:
        print("Penggunaan: python ocr_model.py <path_gambar> [engine]")
        sys.exit(1)

    path = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else "tesseract"

    processed = preprocess_pipeline(path)
    hasil_teks = run_ocr(path, processed_image=processed, engine=engine)

    print("=== Hasil OCR ===")
    print(hasil_teks)
