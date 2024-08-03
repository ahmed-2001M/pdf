# import os 



# import pdfplumber

# def search_word_in_pdf(pdf_path, word):
#     with pdfplumber.open(pdf_path) as pdf:
#         for page_num, page in enumerate(pdf.pages):
#             text = page.extract_text()

#             # Search for the word
#             if text and word.lower() in text.lower():
#                 return True

#     return False




# def solve(folder_path, word):
#     pdfs_paths = os.listdir(folder_path)
#     for file_path in pdfs_paths:
#         file_name = os.path.basename(file_path)
#         extention = os.path.splitext(file_name)[1]
#         if extention == '.pdf':
#             res = search_word_in_pdf(os.path.join(folder_path, file_name), word)
#             if res:
#                 src_path = os.path.join(folder_path, file_name)
#                 dst_path = os.path.join(folder_path, word, file_name)
#                 os.mkdir(os.path.join(folder_path, word))
                
#                 os.replace(src_path, dst_path)
            
            
            
        
        



# if __name__ == '__main__':
#     word = 'MAHFOUZ TOURISM'.lower()
    
#     solve('./how', word)
    
    
    
import os
import zipfile
import streamlit as st
import pdfplumber
import shutil

def search_word_in_pdf(pdf_path, word):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            # Search for the word
            if text and word.lower() in text.lower():
                return True

    return False

def solve(folder_path, word):
    pdfs_paths = os.listdir(folder_path)
    for file_path in pdfs_paths:
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1]
        if extension == '.pdf':
            res = search_word_in_pdf(os.path.join(folder_path, file_name), word)
            if res:
                src_path = os.path.join(folder_path, file_name)
                dst_path = os.path.join(folder_path, word, file_name)
                os.makedirs(os.path.join(folder_path, word), exist_ok=True)
                os.replace(src_path, dst_path)

st.title("PDF Word Search and Move")
uploaded_folder = st.file_uploader("Upload a ZIP folder containing PDFs", type="zip")
search_word = st.text_input("Enter the word to search for")

if st.button("Search and Move PDFs"):
    if uploaded_folder is not None and search_word:
        # Save the uploaded ZIP file
        with open("uploaded_folder.zip", "wb") as f:
            f.write(uploaded_folder.getbuffer())
        
        folder_path = "extracted_folder"
        
        # Remove the existing folder if it exists
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        
        # Extract the ZIP file
        with zipfile.ZipFile("uploaded_folder.zip", "r") as zip_ref:
            zip_ref.extractall(folder_path)

        # Perform the search and move operation
        solve(folder_path, search_word.lower())

        st.success(f"PDFs containing the word '{search_word}' have been moved to the '{search_word}' folder within the extracted folder.")
        
    else:
        st.error("Please upload a folder and enter a word to search for.")
