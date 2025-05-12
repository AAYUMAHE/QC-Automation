# def your_main_function(folder_path , certificate_excel):
import pytesseract
from PIL import Image, ImageFilter, ImageOps
import shutil 
import os
import re
import csv



# ============== to accept the arguments from the terminal ======
import argparse

parser = argparse.ArgumentParser(description="QC Automation for Certificate Validation")
parser.add_argument(
    "--certificate_excel",
    type=str,
    required=True,
    help="Path to the original certificate Excel/CSV file"
)
parser.add_argument(
    "--folder_path",
    type=str,
    required=True,
    help="Path to the folder containing certificate images"
)

args = parser.parse_args()

certificate_excel = args.certificate_excel
folder_path = args.folder_path


# ========================================



# This is the mail file 

# certificate_excel = "./icmai_certificate_data.csv"     #Path to original excel sheet .
# # name , email , secret  , course , unique_number , reg_no , date , type , duration

# folder_path = "./certificates"   # Update this to your certificate folder path

output_folder = "./manual_check_needed"    #static , don't tpuch it . 

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows path

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.convert('L')  # Convert to grayscale
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    return img

def extract_info(image_path):
    try:
        image = preprocess_image(image_path)
        text = pytesseract.image_to_string(image)

        # Combine lines into a single string for better regex matching
        text_cleaned = " ".join(text.split())

        # Extract name after 'awarded to'
        name_match = re.search(r'(?:awarded to|awarded)\s+([A-Z][A-Z\s]{2,30})', text_cleaned)
        name = name_match.group(1).strip().title() if name_match else "Not Found"

        # Extract CMA Reg No
        reg_match = re.search(r'CMA\s*Reg\s*No[:\s]*([0-9]{6,})', text_cleaned)
        reg_no = reg_match.group(1) if reg_match else "Not Found"

        return name, reg_no
    except Exception as e:
        return f"Error: {e}", "Error"

def process_folder(folder_path, output_file="output.txt"):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["unique_number", "name", "reg_no"])
        i = 0 
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(folder_path, filename)
                name, reg_no = extract_info(full_path)
                writer.writerow([filename, name, reg_no])
                i  = i + 1 
                print('Processed file' , filename  , i)
                # writer.writerow(["Filename", "Name", "Reg No"])
        
    print(f" Done! Output written to {output_file}")


process_folder(folder_path)



# ================ Preprocess the data ====== Removing noice =================

import pandas as pd
import re

df = pd.read_csv('output.txt')


df['unique_number'] = df['unique_number'].str.replace(r'\.jpg$', '', case=False, regex=True)

#to clean the name , that comes with the Cma , Cma R , Cma reg , things.

df['name'] = df['name'].str.replace(r'\bCMA\s*R.*$', '', flags=re.IGNORECASE, regex=True)
df['name'] = df['name'].str.replace(r'\bCMA\s*.*$', '', flags=re.IGNORECASE, regex=True)
df['name'] = df['name'].str.replace(r'\bCMA\s*REG.*$', '', flags=re.IGNORECASE, regex=True)
df['name'] = df['name'].str.strip()


#to save the updated csv file . Preprocessed , with removal of noice . 
df.to_csv("output.txt", index=False)


df2 = pd.read_csv('output.txt')

df2[df2.name == 'Not Found'].name


# ====================================

#in last to make it , only clean data , we got from the script  . 

import pandas as pd

# Load the data
df = pd.read_csv("output.txt")

# Detect the name column (like 'Name', 'Full Name', etc.)
name_col = [col for col in df.columns if 'name' in col.lower()]
if not name_col:
    raise Exception(" Couldn't find a column with 'name' in header.")
name_col = name_col[0]

# 1. Extract rows where name == 'Not Found'
df_not_found = df[df[name_col] == 'Not Found']
df_not_found.to_csv("output2.txt", index=False)
print(f"Saved {len(df_not_found)} rows to output2.txt")

# 2. Remove those rows from original data
df_cleaned = df[df[name_col] != 'Not Found']
df_cleaned.to_csv("output.txt", index=False)
print(f"Removed them from output.txt, remaining: {len(df_cleaned)} rows")




# ========   After all , we have to match in the excel sheet , in the format of === name , email , secret  , course , unique_number , reg_no , date , type , duration =======  #

#to check the output and all . 

import pandas as pd

# Load the CSV files
file1 = pd.read_csv("output.txt", header=None)   #output.txt file  . 
file2 = pd.read_csv(certificate_excel, header=None)    #excel that we have to match with .

# Print the shapes for debug
print("File1 shape:", file1.shape  , "Output.txt file dimensions")
print("File2 shape:", file2.shape , "Actual Excel file dimensions")

# Check if the files have the expected number of columns
if file1.shape[1] < 3 or file2.shape[1] < 9:
    raise ValueError("One of the files does not have the required number of columns.")

# Strip whitespaces from relevant columns in both files
file1[0] = file1[0].astype(str).str.strip()  # unique_number
file1[1] = file1[1].astype(str).str.strip()  # name
file1[2] = file1[2].astype(str).str.strip()  # reg_no

file2[0] = file2[0].astype(str).str.strip()  # name
file2[4] = file2[4].astype(str).str.strip()  # unique_number
file2[5] = file2[5].astype(str).str.strip()  # reg_no

# List to store rows with mismatches
error_rows = []

# Iterate through each row in file2
for index, row in file2.iterrows():
    # Match file2[unique_number] (column 5) with file1[unique_number] (column 1)
    match_rows = file1[file1[0] == row[4]]
    
    if not match_rows.empty:
        # For each match found, check name and reg_no
        for _, match_row in match_rows.iterrows():
            condition1 = match_row[1].strip() == row[0].strip()  # file1[name] == file2[name]
            condition2 = match_row[2].strip() == row[5].strip()  # file1[reg_no] == file2[reg_no]
            
            # If either condition fails, add the row to error_rows
            if not (condition1 and condition2):
                error_rows.append(row.tolist())
    else:
        # If no match found for unique_number, add the row to error_rows
        error_rows.append(row.tolist())

# Write mismatched rows to error.txt
with open("error.txt", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "email" , "code" , "course" ,"unique_number",  "reg_no" , "date" , "type" , "duration"])
    for err in error_rows:
        f.write(",".join(map(str, err)) + "\n")

print("Done. All  Mismatched rows written to error.txt.")




# ================== We got 2 csv files , and they both don't have same colms , so we are creating a new csv , we don't want it , but as of now i am doing this now only .===============


import pandas as pd
from itertools import zip_longest

# Load the CSV or TXT files
df1 = pd.read_csv('output2.txt')
df2 = pd.read_csv('error.txt')

col1 = df1['unique_number'].dropna().tolist()
col2 = df2['unique_number'].dropna().tolist()

# Interleave using zip_longest (fills shorter column with None)
interleaved = [val for pair in zip_longest(col1, col2) for val in pair if val is not None]

# Create DataFrame
new_df = pd.DataFrame({'combined_column': interleaved})

# Save to CSV
new_df.to_csv('merged_output.csv', index=False)





# =================================== If you want to delete the intermediate files , then you can uncomment this below code ================================

# import os

# # File paths
# file1 = 'output2.txt'
# file2 = 'error.txt'

# # Delete the files
# os.remove(file1)
# os.remove(file2)

# print(f"Deleted {file1} and {file2}  after doing all the processing , and now you have merged_output.csv  which contains , all the unique_numbers , of the mismatched or not matched rows , from the original csv file .")



# till now , we have matched the regex in the certificate
#then make the matched output regex in the output.txt file i.e csv file .
# then removing the noise of the data to make it clean so we can use it properly . 
# then we are filtering the NOT FOUND in the regex output.txt file , and then adding it to output2.txt file i.e is also csv file .
# then we are comparing the output.txt after the duplicates and noise removed , we are comparing it with the original csv file , and then we are adding the mismatched or not matched rows and then we are pushing the incorrect entries in the error.txt file  , i.e also csv file . 
#then we are fething the unique numbers of both the output2.txt and error.txt files . 
#then we do have an option to delete the intermediate files( output2.txt  , or error.txt) , if you want to delete them , then you can uncomment the below code .



# =======================================
            #  NOW WE WANT THAT ALL THE FILES WITH THE NAME OF UNIQUE NAME WIL LBE MOVED TO THE OUTPUT FOLDER , SO WE CAN SORT THEM MANUALLY . 
            # ==============================================================================


import os
import shutil

# Define your paths
# merged_csv_path = "merged_output.csv"    #is is static.
# folder_path = "path/to/input/folder"
# output_folder = "path/to/output/folder"

# Step 1: Read one ID per line
unique_ids = set()
with open("merged_output.csv", "r") as file:
    for line in file:
        cleaned = line.strip()
        if cleaned and cleaned.lower() != 'combined_column':  # Skip header if present
            unique_ids.add(cleaned.lower())

# Step 2: Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Step 3: Move matching .jpg files
moved_files = 0

for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if not os.path.isfile(filepath) or not filename.lower().endswith(".jpg"):
        continue

    name_without_ext = os.path.splitext(filename)[0].strip().lower()

    if name_without_ext in unique_ids:
        dst = os.path.join(output_folder, filename)
        if not os.path.exists(dst):
            shutil.move(filepath, dst)
            moved_files += 1

print(f"✅ Done. {moved_files} certificate(s) moved to '{output_folder}'.")
