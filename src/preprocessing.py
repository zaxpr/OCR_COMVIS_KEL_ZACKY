"""
preprocessing.py
Fungsi-fungsi untuk mengolah citra sebelum masuk ke tahap OCR.
"""

import cv2
import numpy as np


def load_image(path: str):
    """Membaca gambar dari path menggunakan OpenCV (format BGR)."""
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {path}")
    return image


def to_grayscale(image):
    """Konversi citra BGR menjadi grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise(image_gray):
    """Menghilangkan noise menggunakan median blur."""
    return cv2.medianBlur(image_gray, 3)


def apply_threshold(image_gray):
    """Binarisasi citra menggunakan Otsu's thresholding."""
    _, thresh = cv2.threshold(
        image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh


def deskew(image_gray):
    """Meluruskan kemiringan teks pada citra (opsional, untuk dokumen hasil scan)."""
    coords = np.column_stack(np.where(image_gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image_gray.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image_gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def preprocess_pipeline(path: str, use_deskew: bool = False):
    """
    Pipeline lengkap preprocessing:
    load -> grayscale -> denoise -> (deskew opsional) -> threshold
    Mengembalikan citra siap pakai untuk OCR.
    """
    image = load_image(path)
    gray = to_grayscale(image)
    denoised = denoise(gray)

    if use_deskew:
        denoised = deskew(denoised)

    result = apply_threshold(denoised)
    return result


if __name__ == "__main__":
    # Contoh penggunaan sederhana
    import sys

    if len(sys.argv) < 2:
        print("Penggunaan: python preprocessing.py <path_gambar>")
        sys.exit(1)

    processed = preprocess_pipeline(sys.argv[1])
    cv2.imwrite("output_preprocessed.png", processed)
    print("Selesai. Hasil disimpan sebagai output_preprocessed.png")
