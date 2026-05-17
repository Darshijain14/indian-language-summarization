# src/preprocess.py


import pandas as pd
import sys
import os
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
from torch.utils.data import Dataset
import torch

# Adding parent directory to path so train.py can import this file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_NAME  = "google/mt5-small"
MAX_INPUT   = 256    # Reduced for Windows (less RAM usage)
MAX_TARGET  = 64
DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset.csv')

def load_and_clean_data(path=DATA_PATH):
    """Load CSV and remove bad rows."""
    path = os.path.abspath(path)
    print(f"Loading data from: {path}")
    df = pd.read_csv(path, encoding='utf-8')

    # Check columns exist
    if 'article' not in df.columns or 'summary' not in df.columns:
        raise ValueError("CSV must have 'article' and 'summary' columns.")

    print(f"Rows before cleaning: {len(df)}")
    df = df.dropna(subset=['article', 'summary'])
    df = df[df['article'].str.strip() != '']
    df = df[df['summary'].str.strip() != '']
    df = df.drop_duplicates(subset=['article'])

    # Limit to 3000 rows for faster training on Windows CPU
    df = df.sample(min(3000, len(df)), random_state=42).reset_index(drop=True)
    print(f"Rows after cleaning: {len(df)}")
    return df

def split_data(df):
    """Split into train, validation, test."""
    train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)
    train_df, val_df  = train_test_split(train_df, test_size=0.1, random_state=42)
    print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)

class SummarizationDataset(Dataset):
    """PyTorch Dataset that tokenizes article-summary pairs."""

    def __init__(self, dataframe, tokenizer, max_input=MAX_INPUT, max_target=MAX_TARGET):
        self.data       = dataframe.reset_index(drop=True)
        self.tokenizer  = tokenizer
        self.max_input  = max_input
        self.max_target = max_target

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        article = "summarize: " + str(self.data.loc[idx, 'article'])
        summary = str(self.data.loc[idx, 'summary'])

        # Tokenize input
        src = self.tokenizer(
            article,
            max_length=self.max_input,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        # Tokenize output (target)
        tgt = self.tokenizer(
            summary,
            max_length=self.max_target,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        labels = tgt['input_ids'].squeeze()
        # Replace padding token id with -100 so loss ignores padding
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            'input_ids':      src['input_ids'].squeeze(),
            'attention_mask': src['attention_mask'].squeeze(),
            'labels':         labels
        }


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    df = load_and_clean_data()
    train_df, val_df, test_df = split_data(df)
    dataset = SummarizationDataset(train_df, tokenizer)
    sample = dataset[0]
    print("Input IDs shape:", sample['input_ids'].shape)
    print("Labels shape   :", sample['labels'].shape)
    print("Preprocessing test passed!")
