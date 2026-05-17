
# Abstractive Summarization of Indian Languages using Transformers

A web application that generates abstractive summaries for Indian language
text using the multilingual mT5 transformer model.

## Project Demo

<img width="1892" height="902" alt="image" src="https://github.com/user-attachments/assets/ea1a2f34-fc48-4a96-9ab8-545e144e2e28" />
<img width="1851" height="880" alt="image" src="https://github.com/user-attachments/assets/4dbc3790-2a48-46a2-89b5-2905f341792d" />









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
