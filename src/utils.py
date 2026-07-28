"""
utils.py
Fungsi-fungsi bantu: menyimpan hasil, menghitung akurasi, dan memuat ground truth.
"""

import csv
import difflib


def save_text_output(text: str, output_path: str = "output.txt"):
    """Menyimpan hasil teks OCR ke file .txt"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Hasil teks disimpan ke: {output_path}")


def load_ground_truth(csv_path: str):
    """
    Memuat file ground truth berformat CSV dengan kolom:
    filename,text
    Mengembalikan dict {filename: text_asli}
    """
    ground_truth = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ground_truth[row["filename"]] = row["text"]
    return ground_truth


def compute_accuracy(predicted: str, actual: str) -> float:
    """
    Menghitung akurasi sederhana menggunakan character-level similarity ratio
    (nilai 0.0 - 1.0). Untuk evaluasi lebih formal, pertimbangkan Character Error
    Rate (CER) atau Word Error Rate (WER).
    """
    return difflib.SequenceMatcher(None, predicted.strip(), actual.strip()).ratio()


def evaluate_batch(predictions: dict, ground_truth: dict):
    """
    predictions & ground_truth: dict {filename: text}
    Mengembalikan rata-rata akurasi dan detail per file.
    """
    detail = {}
    total = 0.0
    count = 0

    for filename, actual_text in ground_truth.items():
        predicted_text = predictions.get(filename, "")
        score = compute_accuracy(predicted_text, actual_text)
        detail[filename] = score
        total += score
        count += 1

    avg_accuracy = total / count if count > 0 else 0.0
    return avg_accuracy, detail
