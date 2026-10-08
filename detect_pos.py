import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('01_HighQuality_Enhanced.jpg')
img_rot = cv2.rotate(img, cv2.ROTATE_180)

data = pytesseract.image_to_data(img_rot, output_type=pytesseract.Output.DICT)
for i in range(len(data['text'])):
    t = data['text'][i].strip()
    if t:
        print(f"{t:25} | Pos: (x={data['left'][i]}, y={data['top'][i]}, w={data['width'][i]}, h={data['height'][i]})")
