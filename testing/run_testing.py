"""
run_testing.py
Menjalankan pipeline OCR ASLI dari source_code/ (preprocessing.py + ocr_model.py + utils.py)
terhadap seluruh dataset uji, lalu menghitung akurasi sesungguhnya menggunakan utils.compute_accuracy.
"""
import csv
import time
import cv2

from preprocessing import preprocess_pipeline
from ocr_model import run_ocr
from utils import compute_accuracy

SCENARIO_LABEL = {
    "1": "1 - Ideal",
    "2": "2 - Bayangan",
    "3": "3 - Miring",
}

def load_ground_truth(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def main():
    gt_rows = load_ground_truth("dataset/ground_truth.csv")
    results = []

    print(f"{'File':<14}{'Skenario':<14}{'Ground Truth':<26}{'Prediksi':<26}{'Akurasi':<10}{'Waktu(s)'}")
    print("-" * 100)

    for row in gt_rows:
        fname = row["filename"]
        ground_truth = row["text"]
        scenario = row["scenario"]
        img_path = f"dataset/{fname}"

        t0 = time.time()
        processed = preprocess_pipeline(img_path, use_deskew=(scenario == "3"))
        predicted = run_ocr(img_path, processed_image=processed, engine="tesseract", lang="ind+eng")
        elapsed = time.time() - t0

        predicted_clean = " ".join(predicted.split())  # rapikan whitespace/newline
        acc = compute_accuracy(predicted_clean, ground_truth)

        results.append({
            "filename": fname,
            "scenario": SCENARIO_LABEL[scenario],
            "ground_truth": ground_truth,
            "predicted": predicted_clean if predicted_clean else "(tidak terbaca)",
            "accuracy": acc,
            "time": elapsed,
        })

        print(f"{fname:<14}{SCENARIO_LABEL[scenario]:<14}{ground_truth:<26}{predicted_clean:<26}{acc*100:>6.1f}%   {elapsed:.2f}")

    print("-" * 100)
    avg = sum(r["accuracy"] for r in results) / len(results)
    print(f"Rata-rata akurasi keseluruhan: {avg*100:.2f}%")

    for scen_key, scen_label in SCENARIO_LABEL.items():
        subset = [r for r in results if r["scenario"] == scen_label]
        if subset:
            avg_s = sum(r["accuracy"] for r in subset) / len(subset)
            print(f"Rata-rata akurasi {scen_label}: {avg_s*100:.2f}%")

    # simpan hasil ke CSV untuk dipakai di laporan
    with open("hasil_pengujian.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "scenario", "ground_truth", "predicted", "accuracy", "time"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print("\nHasil lengkap disimpan ke hasil_pengujian.csv")

if __name__ == "__main__":
    main()
