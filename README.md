# QC-Automation

# 🧪 QC Automation for Certificate Validation

This repository contains a Python-based automation script to perform quality control (QC) on certificate data extracted via OCR. The script handles matching, cleaning, validating, and sorting of certificate text data with reference files, making it easier to identify mismatches and errors.

---

## 🚀 Workflow Overview

1. **Regex Matching on Certificates**
   - Perform OCR on certificate images and extract relevant fields using predefined regular expressions.
   - Save matched entries to `output.txt` (CSV format).

2. **Data Cleaning**
   - Remove noise such as special characters or formatting issues.
   - Deduplicate data to prepare for clean comparisons.

3. **Filtering "NOT FOUND" Entries**
   - Entries where regex did not find a match are filtered.
   - These are logged into `output2.txt` (CSV format).

4. **Comparing with Master Data**
   - The cleaned `output.txt` is compared with the original reference CSV.
   - Mismatches or non-matching rows are stored in `error.txt` (CSV format).

5. **Unique Entry Extraction**
   - Unique identifiers (e.g., Roll Numbers, Names, or IDs) are extracted from both `output2.txt` and `error.txt`.

6. **Sorting for Manual QC**
   - All image files corresponding to unique entries in `output2.txt` and `error.txt` are moved to the `output/` folder.
   - These can then be manually reviewed and corrected.

7. **Optional Cleanup**
   - Intermediate files (`output2.txt`, `error.txt`) can be deleted after review.
   - You can uncomment the relevant code lines in the script to enable automatic deletion.

---

## 📂 Directory Structure

# qc-automation/
  ### ├── input/  # Input certificate images
  ### ├── reference.csv # Master reference data
  ### ├── output.txt # Matched and cleaned results
  ### ├── output2.txt # Regex 'NOT FOUND' entries
  ### ├── error.txt # Mismatched entries
  ### ├── output/ # Folder containing error images for manual QC
  ### ├── qc_script.py # Main QC script
  ### └── README.md # This file



---

## 🧾 Example Commands

### In the --certificate-excel put the csv file in the format of  name , email , secret  , course , unique_number , reg_no , date , type , duration , without the header elements  . 
### In the --folder-path  put all the certificate images that need to be QC .
```bash
# Run the QC Automation Script
python main.py --certificate-excel ./file.csv --folder-path ./certificate_folder
 ```


 # Must Things to Follow Up .

 ### Please make sure that on every run you only try to contains the certificates images that are in the excel , let's suppose ,you have images around 100 and entries around 30 , so it will work to match it , but for the pattern not identified in the certificates , will also be moved to manual check , so it is suggested to not use this kind of thing  , or it instead of decresing the work time ,it will make some sort of issue , not really because you have logs records , but still why to make messy  . 

 ###  Best Of Luck .👍👍👍👍👍👍
