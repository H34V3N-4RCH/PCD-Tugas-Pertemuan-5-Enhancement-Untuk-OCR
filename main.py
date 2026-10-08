import cv2
import numpy as np
import pytesseract
import os

# Konfigurasi path Tesseract OCR (sesuaikan path jika berbeda di sistem Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def calculate_accuracy(predicted_text, ground_truth):
    """
    Menghitung jumlah karakter yang cocok dan persentase akurasi OCR
    berdasarkan Ground Truth.
    """
    pred = predicted_text.strip()
    gt = ground_truth.strip()
    
    # Hitung karakter yang cocok per posisi
    correct = sum(1 for p, g in zip(pred, gt) if p == g)
    accuracy = (correct / len(gt)) * 100 if len(gt) > 0 else 0.0
    return pred, correct, accuracy

def apply_filters(image):
    """
    Menerapkan 4 metode filtering/enhancement:
    1. Mean Filter (Averaging / Box Filter)
    2. Median Filter (Non-linear filter untuk noise impulse)
    3. Gaussian Filter (Weighted blur berdasarkan distribusi normal)
    4. Sharpening Filter (High-pass / Laplacian kernel)
    """
    # 1. Mean Filter (kernel 3x3)
    img_mean = cv2.blur(image, (3, 3))
    
    # 2. Median Filter (kernel 3x3)
    img_median = cv2.medianBlur(image, 3)
    
    # 3. Gaussian Filter (kernel 3x3, sigma otomatis)
    img_gaussian = cv2.GaussianBlur(image, (3, 3), 0)
    
    # 4. Sharpening Filter
    kernel_sharpen = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)
    img_sharpened = cv2.filter2D(image, -1, kernel_sharpen)
    
    return {
        "Original": image,
        "Mean filter": img_mean,
        "Median filter": img_median,
        "Gaussian filter": img_gaussian,
        "Sharpening": img_sharpened
    }

def main():
    # File citra acuan (Ground Truth) dan citra uji (Noise)
    gt_image_path = '01_HighQuality_Enhanced.jpg'
    noisy_image_path = '04_HighNoise.jpg'
    
    if not os.path.exists(gt_image_path) or not os.path.exists(noisy_image_path):
        print("File citra tidak ditemukan di direktori saat ini.")
        return

    # Membaca citra acuan untuk memperoleh Ground Truth teks
    img_gt = cv2.imread(gt_image_path, cv2.IMREAD_GRAYSCALE)
    # Putar 180 derajat jika orientasi citra terbalik
    img_gt_rot = cv2.rotate(img_gt, cv2.ROTATE_180)
    
    gt_raw = pytesseract.image_to_string(img_gt_rot, config='--oem 3 --psm 6')
    ground_truth = " ".join(gt_raw.split())
    
    print("=" * 80)
    print("TUGAS PERTEMUAN 5 - ENHANCEMENT UNTUK OCR")
    print("Topik: Filtering, Noise Reduction, dan Sharpening")
    print("=" * 80)
    print(f"\n[Ground Truth Teks (Total {len(ground_truth)} karakter)]:")
    print(ground_truth[:120] + "...\n")

    # Membaca citra yang memiliki noise (04_HighNoise.jpg)
    img_noisy = cv2.imread(noisy_image_path, cv2.IMREAD_GRAYSCALE)
    img_noisy_rot = cv2.rotate(img_noisy, cv2.ROTATE_180)

    # Terapkan berbagai teknik filtering & enhancement
    filtered_images = apply_filters(img_noisy_rot)

    # Evaluasi OCR pada setiap metode
    print("-" * 80)
    print(f"{'Metode':<20} | {'Hasil OCR':<30} | {'Karakter Benar':<16} | {'Akurasi':<10}")
    print("-" * 80)

    for name, img in filtered_images.items():
        ocr_raw = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
        ocr_clean = " ".join(ocr_raw.split())
        
        pred, correct, acc = calculate_accuracy(ocr_clean, ground_truth)
        
        # Tampilkan cuplikan hasil OCR agar rapi di tabel
        ocr_display = (ocr_clean[:27] + "...") if len(ocr_clean) > 30 else ocr_clean
        print(f"{name:<20} | {ocr_display:<30} | {str(correct) + '/' + str(len(ground_truth)):<16} | {acc:.2f}%")

    print("-" * 80)

if __name__ == "__main__":
    main()