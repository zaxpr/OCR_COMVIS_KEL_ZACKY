# Proyek UAS: Sistem Optical Character Recognition (OCR)

**Mata Kuliah:** Computer Vision  
**Semester:** 6  
**Repository:** [https://github.com/zaxpr/OCR_COMVIS_KEL_ZACKY](https://github.com/zaxpr/OCR_COMVIS_KEL_ZACKY)

---

## 1. Anggota Kelompok

* **Muhammad Zacky Pratama** - 1003230035

---

## 2. Deskripsi Singkat

Aplikasi ini dirancang untuk melakukan ekstraksi teks dari citra digital (seperti foto KTP, struk belanja, plat nomor, atau dokumen hasil pemindaian) menggunakan teknik Computer Vision dan OCR. 

Sistem menerapkan tahapan pra-pemrosesan citra (*image preprocessing*) yang mencakup konversi *grayscale*, *thresholding*, serta *noise removal* sebelum citra diproses oleh engine OCR untuk mendapatkan teks akhir.

---

## 3. Struktur Folder

```text
UAS_OCR_Kelompok/
├── README.md
└── source_code/
    ├── notebook_OCR.ipynb              # Notebook utama: alur end-to-end (load -> preprocess -> OCR -> evaluasi)
    ├── requirements.txt                # Daftar dependensi library
    ├── src/
    │   ├── preprocessing.py            # Fungsi-fungsi pengolahan citra sebelum OCR
    │   ├── ocr_model.py                # Wrapper pemanggilan model/engine OCR
    │   └── utils.py                    # Fungsi bantu (load gambar, simpan hasil, dll)
    ├── data/
    │   ├── sample_images/              # 12 citra uji (4 per skenario) - hasil generate_dataset.py
    │   └── ground_truth.csv            # Label teks asli untuk kalkulasi akurasi
    └── testing/
        ├── generate_dataset.py         # Skrip pembuat dataset uji sintetis
        ├── run_testing.py              # Skrip eksekusi pipeline OCR & kalkulasi akurasi
        ├── hasil_pengujian.csv         # Hasil pengujian aktual (12 baris data)
        ├── terminal_output.txt         # Log mentah eksekusi run_testing.py
        ├── terminal_screenshot.png     # Tangkapan layar terminal
        └── perbandingan_preprocessing.png # Komparasi citra asli vs hasil preprocessing
