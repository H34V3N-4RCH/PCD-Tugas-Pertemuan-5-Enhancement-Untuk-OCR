import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def eval_ocr(image, gt, config='--oem 3 --psm 6'):
    pred_raw = pytesseract.image_to_string(image, config=config)
    pred = " ".join(pred_raw.split())
    gt_clean = " ".join(gt.split())
    
    # Hitung karakter yang cocok
    correct = sum(1 for p, g in zip(pred, gt_clean) if p == g)
    acc = (correct / len(gt_clean)) * 100 if len(gt_clean) > 0 else 0
    return pred, correct, acc

# Ground truth dari citra asli/HQ (01_HighQuality_Enhanced)
img_hq = cv2.imread('01_HighQuality_Enhanced.jpg')
img_hq_rot = cv2.rotate(img_hq, cv2.ROTATE_180)
gt_full = pytesseract.image_to_string(img_hq_rot)
gt_full_clean = " ".join(gt_full.split())

# Citra Noise (04_HighNoise.jpg)
img_noisy = cv2.imread('04_HighNoise.jpg')
img_noisy_rot = cv2.rotate(img_noisy, cv2.ROTATE_180)
img_noisy_gray = cv2.cvtColor(img_noisy_rot, cv2.COLOR_BGR2GRAY)

# Terapkan Filtering & Enhancement
# 1. Original Grayscale
# 2. Mean Filter
img_mean = cv2.blur(img_noisy_gray, (3, 3))

# 3. Median Filter
img_median = cv2.medianBlur(img_noisy_gray, 3)

# 4. Gaussian Filter
img_gaussian = cv2.GaussianBlur(img_noisy_gray, (3, 3), 0)

# 5. Sharpening Filter
sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
img_sharpened = cv2.filter2D(img_noisy_gray, -1, sharpen_kernel)

filters = {
    "Original": img_noisy_gray,
    "Mean filter": img_mean,
    "Median filter": img_median,
    "Gaussian filter": img_gaussian,
    "Sharpening": img_sharpened
}

print("=== HASIL OCR DIPLOMA LENGKAP ===")
print(f"Ground Truth ({len(gt_full_clean)} chars):\n{gt_full_clean}\n")
for name, img in filters.items():
    pred, correct, acc = eval_ocr(img, gt_full_clean, config='--oem 3 --psm 6')
    print(f"[{name}]")
    print(f"Hasil: {pred[:80]}...")
    print(f"Karakter Benar: {correct}/{len(gt_full_clean)} | Akurasi: {acc:.2f}%\n")
