
# Abstractive Summarization of Indian Languages using Transformers

A web application that generates abstractive summaries for Indian language
text using the multilingual mT5 transformer model.

## Project Demo

<img width="1901" height="897" alt="image" src="https://github.com/user-attachments/assets/699d384c-a7c4-44f9-86ac-07dfae7952d0" />
<img width="1415" height="875" alt="image" src="https://github.com/user-attachments/assets/31c584f6-1a44-492e-a622-4dc08c3a1cd1" />
<img width="1885" height="885" alt="image" src="https://github.com/user-attachments/assets/bdc57453-b3a9-4dad-a0ff-dba318df0e69" />
<img width="1801" height="858" alt="image" src="https://github.com/user-attachments/assets/7944383e-20f5-4518-a40b-bdc951882b55" />





## Features

- Summarizes text in 9+ Indian languages including Hindi, Tamil, Telugu,
  Bengali, Marathi, Gujarati, Kannada, Malayalam and Urdu
- Upload documents in PDF, DOCX or TXT format
- Translate summary to any language including English, Hindi, Tamil and more
- Text-to-Speech reads the summary aloud in the correct Indian language
- Download summary as TXT file
- Shows compression ratio and word count statistics

## Model Used

This project uses `csebuetnlp/mT5_multilingual_XLSum` which is a
multilingual T5 model fine-tuned on the XLSum dataset containing
1.35 million BBC news article-summary pairs across 45 languages
including all major Indian languages.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Core language |
| HuggingFace Transformers | mT5 model loading |
| PyTorch | Deep learning backend |
| Streamlit | Web interface |
| gTTS | Text-to-speech |
| deep-translator | Translation feature |
| pdfplumber | PDF text extraction |
| python-docx | Word document extraction |
| langdetect | Language detection |

## Project Structure
indian_summarization/
├── data/
│   └── dataset.csv
├── model/
│   └── mt5_summarizer/     ← download separately (see below)
├── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── evaluate.py
│   └── inference.py
├── app.py
├── requirements.txt
└── README.md
