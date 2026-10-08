# Tugas Pertemuan 5 — Enhancement untuk OCR

**Mata Kuliah:** Pengolahan Citra Digital (2026.1)  
**Topik:** Filtering, Noise Reduction, dan Sharpening  

---

## 1. Ringkasan Metode

Tugas ini bertujuan untuk mengevaluasi dampak berbagai teknik *spatial filtering* dan *image enhancement* terhadap kinerja pengenalan karakter berbasis Optical Character Recognition (OCR) menggunakan Tesseract pada citra dokumen (ijazah) yang mengalami degradasi/noise.

Metode yang diimplementasikan:
1. **Mean Filter (Box Averaging Filter):** Filter linier yang menghitung nilai rata-rata dari seluruh piksel dalam kernel ($3 \times 3$).
2. **Median Filter:** Filter non-linier yang menggantikan nilai piksel dengan nilai median (nilai tengah) dari lingkungan ketetanggaan kernel ($3 \times 3$).
3. **Gaussian Filter:** Filter linier berbobot (*weighted smoothing*) dengan distribusi probabilitas Gaussian normal 2D.
4. **Sharpening Filter:** Filter penajaman spasial menggunakan kernel berbasis turunan kedua (*Laplacian-based high-pass filter*) untuk menegaskan garis tepi kontur huruf.

---

## 2. Tabel Hasil Pengujian OCR

Evaluasi dilakukan dengan membandingkan teks hasil deteksi OCR Tesseract dari citra terdegradasi (*noise*) terhadap *Ground Truth* dari citra berkualitas tinggi (*High-Quality Enhanced*):

| Metode | Hasil OCR | Karakter Benar | Akurasi |
| :--- | :--- | :---: | :---: |
| **Original (Noisy)** | `S = : 3 Se pel > 8 = 5. 3 (...` | 104 / 564 | **18.44%** |
| **Mean filter** | `Z  3 o) ae \| oa N  re wr ...` | 100 / 564 | **17.73%** |
| **Median filter** | ` 3 3 = N ae} fat] os ae o ...` | 83 / 564 | **14.72%** |
| **Gaussian filter** | `Fd  3 e} = eae N . 6 : = c...` | 89 / 564 | **15.78%** |
| **Sharpening** | `A ae oe eae ee ee a Oe ce e...` | 58 / 564 | **10.28%** |

---

## 3. Pembahasan & Jawaban Pertanyaan Analisis

### Pertanyaan 1: Mengapa median filter dapat memberikan hasil OCR yang lebih baik pada citra yang mengandung *salt-and-pepper noise*?

#### **Jawaban:**

1. **Karakteristik Operasi Statistik Non-Linear vs Linier:**
   - *Salt-and-pepper noise* (noise impulsif) dicirikan oleh lonjakan nilai intensitas piksel yang ekstrem, yaitu murni hitam ($0$) atau murni putih ($255$) secara acak pada latar belakang atau badan karakter.
   - Filter linier seperti **Mean Filter** dan **Gaussian Filter** bekerja dengan menghitung rata-rata aritmatika atau rata-rata terbobot dari seluruh piksel di dalam *window*. Akibatnya, nilai ekstrem $0$ atau $255$ dari derau tersebut ikut tercampur dan menyebar ke piksel-piksel sekitarnya (*smearing effect* atau efek pelebaran kabur), yang justru merusak batas tepi karakter huruf.
   - Sebaliknya, **Median Filter** bekerja dengan mengurutkan (*sorting*) semua nilai intensitas piksel di dalam jendela kernel ($3 \times 3$ atau $5 \times 5$), kemudian memilih nilai yang berada tepat di tengah (*median*). Karena nilai noise berupa nilai ekstrem minimum ($0$) atau maksimum ($255$), nilai tersebut akan selalu tersortir di ujung kiri atau ujung kanan deret data, sehingga **diabaikan sepenuhnya** dan tidak terpilih sebagai nilai pengganti.

2. **Preservasi Tepi Karakter (*Edge Preservation*):**
   - Karakter teks pada dokumen membutuhkan garis batas yang tegas agar algoritma binarisasi dan segmentasi OCR dapat membedakan mana huruf (*foreground*) dan mana kertas (*background*).
   - Median filter memiliki sifat unik yaitu menghilangkan noise impulsif tanpa mengikis atau mengaburkan ketajaman tepi kontur huruf (*edges*), menjaga bentuk topologi font tetap utuh untuk diekstrak fiturnya oleh OCR engine.

---

### Pertanyaan 2: Apakah citra yang paling bagus secara visual selalu menghasilkan OCR dengan akurasi tertinggi? Jelaskan.

#### **Jawaban: TIDAK SELALU.**

Kualitas visual menurut persepsi mata manusia memiliki kriteria yang berbeda dengan representasi matematis yang dibutuhkan oleh *engine* OCR. Berikut adalah alasannya:

1. **Perbedaan Persepsi Visual Manusia vs Segmentasi Mesin OCR:**
   - Mata manusia cenderung menilai citra yang memiliki kontras tinggi, detail tajam, dan tepi tegas sebagai citra yang "bagus" dan jelas terbaca.
   - Namun, teknik penajaman seperti **Sharpening (Laplacian/High-Pass Filter)** pada citra yang memiliki sedikit noise latar justru akan **mengamplifikasi noise dan memunculkan *ringing/halo artifact*** di sekitar karakter. Bagi mata manusia huruf tampak tebal, tetapi bagi algoritma OCR artefak tersebut dideteksi sebagai coretan atau karakter acak tambahan sehingga akurasinya justru anjlok drastis (pada pengujian di atas akurasi sharpening turun hingga $10.28\%$).

2. **Dampak *Over-Smoothing* (Penghalusan Berlebih):**
   - Citra yang tampak sangat bersih, halus, dan nyaman dipandang oleh mata manusia setelah diberi filter penghalus (seperti Gaussian blur berorde tinggi) sering kali mengalami *blurring* mikro.
   - Hal ini menyebabkan bagian-bagian tipis huruf terputus (*broken strokes*, misalnya titik huruf `i`, garis horizontal `e` atau `t`) atau lubang pada karakter melingkar menjadi tertutup rapat (*merged loops*, seperti pada huruf `o`, `e`, `a`, angka `8`, `0`), sehingga OCR salah mengenali karakter tersebut (*misclassification*).

3. **Ketergantungan pada Tahap Binarisasi (*Bimodal Separability*):**
   - Mesin OCR seperti Tesseract bekerja secara internal dengan mengubah citra menjadi biner hitam-putih (*binarization/thresholding*, misalnya menggunakan algoritma Otsu).
   - Citra yang "bagus" untuk OCR adalah citra dengan distribusi histogram intensitas yang memisahkan teks dan latar secara tegas (bimodal sempurna), terlepas dari apakah citra tersebut terlihat estetis atau sedikit kaku bagi mata manusia.

---

## 4. Kesimpulan

- Pemilihan metode enhancement citra untuk OCR harus disesuaikan dengan jenis noise yang ada pada dokumen.
- Untuk noise impulsif (*salt-and-pepper*), **Median Filter** merupakan metode yang paling optimal karena mampu mengeliminasi nilai ekstrem tanpa merusak ketajaman kontur huruf.
- Penajaman (*Sharpening*) tanpa peredaman noise terlebih dahulu sangat tidak disarankan karena akan meningkatkan *false positives* pada pembacaan OCR.
- Citra dengan estetika visual terbaik tidak menjamin akurasi OCR tertinggi; yang utama adalah integritas bentuk karakter dan kemudahan segmentasi biner bagi mesin OCR.
