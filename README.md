# Proyek UAS: Sistem OCR (Optical Character Recognition)
Mata Kuliah: Computer Vision
Semester: 6

## 1. Anggota Kelompok
Muhammad Zacky Pratama - 1003230035 

## 2. Deskripsi Singkat
Aplikasi ini membaca teks dari gambar (contoh: foto KTP, struk belanja, plat nomor, atau dokumen scan) menggunakan pendekatan Computer Vision dan OCR. Sistem melakukan preprocessing citra (grayscale, thresholding, noise removal) sebelum teks diekstraksi menggunakan model/library OCR.

## 3. Struktur Folder
```
UAS_OCR_Kelompok/
├── README.md
├── laporan/
│   └── Laporan_UAS_Kelompok_Template.pdf   # Laporan lengkap BAB 1-5 (format PDF)
├── presentasi/
│   └── Presentasi_UAS_Computer_Vision_Zacky.pptx  # Slide presentasi hasil proyek
└── source_code/
    ├── notebook_OCR.ipynb   # Notebook utama: alur end-to-end (load -> preprocess -> OCR -> evaluasi)
    ├── requirements.txt     # Daftar library yang dibutuhkan
    ├── Github_link.txt      # Link repo GitHub proyek
    ├── src/
    │   ├── main.py           # Entry point CLI untuk menjalankan pipeline OCR
    │   ├── preprocessing.py  # Fungsi-fungsi pengolahan citra sebelum OCR
    │   ├── ocr_model.py      # Wrapper pemanggilan model/engine OCR
    │   └── utils.py          # Fungsi bantu (load gambar, simpan hasil, dll)
    ├── data/
    │   ├── sample_images/   # 12 citra uji (4 per skenario) - hasil generate_dataset.py
    │   └── ground_truth.csv # Label teks asli, dipakai untuk hitung akurasi
    └── testing/
        ├── generate_dataset.py         # Skrip pembuat dataset uji (dengan ground truth pasti)
        ├── run_testing.py              # Skrip yang menjalankan pipeline OCR asli & menghitung akurasi
        ├── hasil_pengujian.csv         # Hasil pengujian aktual (12 baris, sesuai Tabel 3.2 laporan)
        ├── terminal_output.txt         # Log mentah hasil eksekusi run_testing.py
        ├── terminal_screenshot.png     # Screenshot terminal (dipakai di laporan Gambar 3.2)
        └── perbandingan_preprocessing.png  # Citra asli vs hasil preprocessing (Gambar 3.1 laporan)
```

## 3.1 Sumber Dataset
Dataset uji (12 citra, 4 per skenario) dibuat secara terkontrol menggunakan `source_code/testing/generate_dataset.py`: teks dirender ke kanvas digital lalu diberi distorsi sesuai skenario (Skenario 2: gradasi bayangan + derau; Skenario 3: rotasi 10°). Pendekatan ini digunakan agar ground truth (teks asli) diketahui pasti sehingga akurasi dapat dihitung secara obyektif. Jika kelompok ingin memakai foto dokumen fisik asli, cukup ganti isi folder `data/sample_images/` dan `data/ground_truth.csv`, lalu jalankan ulang `testing/run_testing.py`.

## 3.2 Penggunaan Kode/Model Pihak Lain
Tidak ada pretrained model kustom maupun dataset publik pihak lain yang digunakan. Engine OCR menggunakan Tesseract OCR (bahasa `ind+eng`) yang merupakan pustaka open-source resmi, dipanggil melalui `pytesseract` tanpa modifikasi arsitektur.

## 3.3 Reproduksi Hasil Pengujian
Hasil pada Tabel 3.2 laporan diperoleh dari eksekusi nyata (bukan simulasi). Untuk menjalankan ulang:
```bash
cd source_code/testing
python generate_dataset.py   # (opsional) generate ulang dataset sintetis
python run_testing.py        # menjalankan OCR pada seluruh dataset & cetak akurasi
```
Hasil akan tercetak di terminal dan tersimpan ke `hasil_pengujian.csv`.

## 4. Cara Instalasi

### 4.1 Clone / Ekstrak Project
```bash
# Jika dari GitHub
git clone https://github.com/zaxpr/OCR_COMVIS_KEL_ZACKY
cd OCR_COMVIS_KEL_ZACKY

# Jika dari ZIP, cukup ekstrak lalu masuk ke folder source_code/
```

### 4.2 Buat Virtual Environment (opsional tapi disarankan)
```bash
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows
```

### 4.3 Install Dependencies
```bash
pip install -r requirements.txt
```

Contoh isi `requirements.txt` untuk proyek OCR:
```
opencv-python
numpy
pytesseract
easyocr
matplotlib
pandas
```

> Catatan: Jika menggunakan `pytesseract`, Tesseract-OCR engine harus diinstal terpisah di sistem operasi (bukan hanya lewat pip). Lihat: https://github.com/tesseract-ocr/tesseract

## 5. Cara Menjalankan Program

### Opsi A — Menjalankan Notebook
```bash
jupyter notebook notebook_OCR.ipynb
```
Jalankan sel dari atas ke bawah secara berurutan.

### Opsi B — Menjalankan Script Python
```bash
python src/main.py --image data/sample_images/doc_01.jpg
```

Output berupa teks hasil ekstraksi akan ditampilkan di terminal dan/atau disimpan ke file `output.txt`.

## 6. Link GitHub
https://github.com/zaxpr/OCR_COMVIS_KEL_ZACKY

## 7. Referensi Model/Library OCR yang Digunakan
- Tesseract OCR (bahasa ind+eng) — dipanggil melalui `pytesseract`, https://github.com/tesseract-ocr/tesseract
- OpenCV — pengolahan citra (grayscale, thresholding, deskewing), https://opencv.org/
- EasyOCR — opsi engine alternatif (arsitektur CRNN), https://github.com/JaidedAI/EasyOCR

