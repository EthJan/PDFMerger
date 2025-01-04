import PyPDF2
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import spacy
from voice_to_text import voice_input
import os
import re

def extract_keywords(pdf_text):
    # extract keywords using spacy import
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(pdf_text)

    # Extract nouns and proper nouns as the keywords (open to change)
    keywords = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return set(keywords)

def find_groups(path, files):
    add_seperator()
    print("Finding groups...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    pdf_texts = []
    pdf_names = []
    pdf_keywords = {}

    # Extract text for all pdfs
    for file in files:
        filePath = os.path.join(path, file)
        reader = PdfReader(filePath)
        text = "".join(page.extract_text() for page in reader.pages)
        pdf_texts.append(text)
        pdf_names.append(file)
        pdf_keywords[file] =  extract_keywords(text) # extract keywords and assign to file key

    # Convert text to embeddings
    embeddings = model.encode(pdf_texts, convert_to_tensor=True)

    # Calculate consine similarity betwen embeddings
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
    
    # use cosine similarity and keyword overlap to find groupings
    groups = []
    similarity_threshold = 0.8 # keyword overlap threshold
    grouped_files = set()

    for i in range(len(files)):
        if files[i] in grouped_files:
            continue
        current_group = [files[i]]
        shared_keywords = pdf_keywords[files[i]].copy()
        grouped_files.add(files[i])
        for j in range(i + 1, len(files)):
            if files[j] in grouped_files:
                continue
            if similarity_matrix[i][j] > similarity_threshold:
                current_group.append(files[j])
                shared_keywords.intersection_update(pdf_keywords[files[j]])
                grouped_files.add(files[j])                
        groups.append((shared_keywords, current_group))

    return groups


def suggested_merge(path, groups):
    # Merge and place into one singular folder
    add_seperator()
    print("Merging Suggested Groups...")
    # check that they are all in directory
    for keywords, files in groups:
        for file in files:
            if not file.endswith(".pdf"):
                print(f"{file} is not a valid PDF format, please reformat and try again")
                return_menu(path)
            if file not in os.listdir(path):
                print(f"{file} does not exist in the directory.")
                return_menu(path)
        unique_name = False
        while not unique_name:
            add_seperator()
            print("Merging the following Files")
            for file in files:
                print(f"- {file}")
            print(f"Group descripters: {','.join(keywords)}")
            # Possible error may occur where it compares directory paths instead of names
            file_output_name = input("Input the name for the combined file (will auto make into pdf): ").strip()
            file_output_name = file_output_name + ".pdf"
            if file_output_name in os.listdir(path):
                print("File already exists. Choose a different name")
            else:
                unique_name = True
    
        merger = PyPDF2.PdfMerger()

        # Add each file to the merger and write it to a new pdf
        for file in files:
            # Join the file name with the path directory to get the path for the file 
            file_path = os.path.join(path, file)  
            # merge
            merger.append(file_path)

        # Write the merged PDF
        output_path = os.path.join(path, file_output_name)
        merger.write(output_path)
        merger.close()
    
    print("All groups have been merged. ")
    confirm()
    

def merge(path, files):
    add_seperator()
    print("Merging...")
    # check that they are all in directory
    for file in files:
        if not file.endswith(".pdf"):
            print(f"{file} is not a valid pdf format, please reformat and try again.")
            return_menu(path)
        if file not in os.listdir(path):
            print(f"{file} does not exist in the directory.")
            return_menu(path)

        file_output_name = ""
    unique_name = False
    while not unique_name:
        add_seperator()
        # Possible error may occur where it compares directory paths instead of names
        file_output_name = input("Input the name for the combined file (will auto make into pdf): ").strip()
        file_output_name = file_output_name + ".pdf"
        if file_output_name in os.listdir(path):
            print("File already exists. Choose a different name")
        else:
            unique_name = True
   
    merger = PyPDF2.PdfMerger()

    # Add each file to the merger and write it to a new pdf
    for file in files:
        # Join the file name with the path directory to get the path for the file 
        file_path = os.path.join(path, file)  
        # merge
        merger.append(file_path)

    # Write the merged PDF
    output_path = os.path.join(path, file_output_name)
    merger.write(output_path)
    merger.close()

    print("All files have been merged. ")
    confirm()

def file_organize(path):    
    # Ask which files to import 
    files_input = input("Enter then files seperated by spaces (Copy and paste is the easiest): ")
    files = re.split(r'[ ]', files_input)

    # merge 
    groups = find_groups(path,files)
    for keywords, files in groups:
        group_desc = ", ".join(sorted(keywords)) if keywords else "Unknown Type"
        print(f"\nGroup Type: {group_desc}")
        print(f"Files in this group: {files}")

    # Group merge or manual merge
    merge_option = input("Would you like to use the suggested merge groups? (y or n): ").lower()
    if merge_option == "n":
        merge(path, files)
    elif merge_option == "y":
        suggested_merge(path, groups)

def voice_organize(path):
    # parse through file and create a list of files by splitting at spaces
    with open("output.txt", "r") as file:
        output_files = file.read().strip()
        # create list of  fikes
        files = output_files.split(" ")
    file.close
    merge(path, files)


def add_seperator():
    print("")
    for i in range(10):
        print("#", end="")
    print("\n")

def FAQ():
    print("1. Is there a file limit?")
    print("No, there is no file limit or space constraint.\n")
    print("\n2. How should my files be named?")
    print("Your files may contain any characters except for spaces.\n")

    input("Press enter to return to menu: ")

def confirm():
    add_seperator()
    confirmation = input("Would you like to use another operation? (y or n): ").lower()
    if confirmation == "y":
        main()
    elif confirmation == "n":
        exit()

def return_menu(path):
    print("Returning to menu...")
    menu(path)

def menu(path):
    choice = 0
    while choice not in [1,2,3,4]:
        choice = input("Enter "
                       "\n1. for manual file input"
                        "\n2. for voice file input"
                        "\n3. FAQ"
                        "\n4. exit\n")
        if choice == "1":
            add_seperator()
            file_organize(path)
        if choice =="2":
            add_seperator()
            voice_input()
            voice_organize(path)
        if choice == "3":
            add_seperator()
            FAQ()
            continue
        if choice == "4":
            print("Quiting Program.")
            exit()
        print("Enter a valid command.")

def main():
    print("File Combiner Time!")
    print("Welcome!")
    path = input("Enter the directory path: ")
    add_seperator()
    menu(path)

# todo

    # Suggest grouped merges
if __name__ == "__main__":
    main()