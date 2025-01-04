# PDFMerger
A PDF merger created to help ease the difficulty of finding an online reliable and easy to use pdf combiner for my school work pdf files. Additionally, I implemented AI allows for multiple varying topics of pdfs to be merged simultaneously into separately identified groups of pdfs.  

Programmed using Python, the PDFMerger takes in a directory path and offers the user to input files through console or voice command, allowing for hands-free access, something I've always wished that online applications had, overcoming the issue of needing to alt+tab between Windows and reorder files. After the files are inputted, the program uses PyPDF2 to read the content of the PDFs, extracting text from each page to prepare for analysis.

The extracted text is then processed using natural language processing (NLP) techniques in order to provide the user with the suggested sub-groups to merge. I wanted to add this feature because I found I would be merging pdfs for multiple classes in multiple takes. The AI allows for multiple pdf operations to be completed in one run. Once the text is extracted, the SentenceTransformer library is used to generate semantic embeddings of the text, to compare between each of the files based on content. These embeddings are analyzed with cosine similarity to group PDFs that share similar topics or themes, allowing for logical suggested merge groups. 

To further enhance the grouping process, the program employs keyword extraction techniques using spaCy, identifying key terms in each document. This enables the program to label and categorize the grouped files based on shared terms, providing transparency and insight into how the groups are formed.

Once the files are grouped, the program provides options for the user to merge each group into a single PDF, with the ability to customize output file names. The merging process uses PyPDF2’s Merger class, ensuring that files are combined in the desired order while preserving their original formatting and structure.

