import os
import zipfile
import streamlit as st
import pdfplumber
import shutil

def search_word_in_pdf(pdf_path, word):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            if text:
                print(f"Extracted text from {pdf_path}:")
            else:
                print(f"No text extracted from {pdf_path}")

            # Search for the word
            if text and word.lower() in text.lower():
                return True

    return False

def solve(folder_path, words):
    folder_path = os.path.join(folder_path, 'how')
    pdfs_paths = os.listdir(folder_path)
    for file_name in pdfs_paths:
        base_folder = os.path.join(folder_path, '..')

        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            file_copied = False
            
            for word in words:
                word_lower = word.lower()
                word_folder = os.path.join(base_folder, 'extracted', word_lower)
                os.makedirs(word_folder, exist_ok=True)
                
                if search_word_in_pdf(file_path, word_lower):
                    shutil.copy(file_path, word_folder)
                    print(f"Moved {file_name} to {word_folder}")
                    file_copied = True
                else:
                    print(f"Word '{word}' not found in {file_name}")

            if file_copied:
                os.remove(file_path)
                print(f"Removed {file_name} from {folder_path}")


st.title("PDF Word Search and Move")
uploaded_folder = st.file_uploader("Upload a ZIP folder containing PDFs", type="zip")
search_words = st.text_input("Enter words to search for (comma separated)")

if st.button("Search and Move PDFs"):
    if uploaded_folder is not None and search_words:
        log_placeholder = st.empty()
        
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

        # Convert the input string to a list of words
        words = [word.strip().lower() for word in search_words.split(",")]

        # Perform the search and move operation
        solve(folder_path, words)

        st.success(f"PDFs containing the words '{search_words}' have been moved to their respective folders within the extracted folder.")
        
    else:
        st.error("Please upload a folder and enter words to search for.")
