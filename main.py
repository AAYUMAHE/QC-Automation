# pip install pytesseract pillow opencv-python
import pytesseract # type: ignore
from PIL import Image # type: ignore
import os
import re
import csv

# 🛠️ Configure Tesseract path (adjust if needed)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Linux/Mac
# For Windows, use something like:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_info(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Match name after 'awarded to'
        name_match = re.search(r'awarded to\s+([A-Z\s]+)', text)
        name = name_match.group(1).strip() if name_match else "Not Found"

        # Match registration number after 'CMA Reg No'
        reg_match = re.search(r'CMA Reg No[:\s]+(\d+)', text)
        reg_no = reg_match.group(1) if reg_match else "Not Found"

        return name, reg_no
    except Exception as e:
        return f"Error: {e}", "Error"

def process_folder(folder_path, output_file="output.txt"):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Name", "Reg No"])

        for filename in os.listdir(folder_path):
            i=1
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(folder_path, filename)
                name, reg_no = extract_info(full_path)
                writer.writerow([filename, name, reg_no])
                print('Processing completed for ' , filename , i)
                i += 1
    print(f"✅ Done! Output written to {output_file}")

# 🔁 Replace this with your actual folder path
folder_path = "./certificates"
process_folder(folder_path)
