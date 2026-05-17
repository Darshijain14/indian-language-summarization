# src/evaluate.py
# PURPOSE: Calculate ROUGE scores on test data
# HOW TO RUN: python src/evaluate.py  (run AFTER training)

import os
import sys
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from rouge_score import rouge_scorer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'mt5_summarizer')
TEST_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.csv')

device    = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)
model.eval()

def generate_summary(text, max_input=256, max_summary=64):
    inputs = tokenizer(
        "summarize: " + text,
        return_tensors="pt",
        max_length=max_input,
        truncation=True
    ).to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids            = inputs["input_ids"],
            attention_mask       = inputs["attention_mask"],
            max_length           = max_summary,
            num_beams            = 4,
            length_penalty       = 2.0,
            early_stopping       = True,
            no_repeat_ngram_size = 2
        )
    return tokenizer.decode(output[0], skip_special_tokens=True)

def evaluate(num_samples=50):
    df     = pd.read_csv(TEST_PATH, encoding='utf-8').head(num_samples)
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
    scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}

    print(f"Evaluating on {len(df)} samples...")
    for i, row in df.iterrows():
        pred   = generate_summary(str(row['article']))
        ref    = str(row['summary'])
        result = scorer.score(ref, pred)
        scores['rouge1'].append(result['rouge1'].fmeasure)
        scores['rouge2'].append(result['rouge2'].fmeasure)
        scores['rougeL'].append(result['rougeL'].fmeasure)
        if i % 10 == 0:
            print(f"  [{i}/{len(df)}] ROUGE-1: {result['rouge1'].fmeasure:.3f}")

    avg = lambda k: sum(scores[k]) / len(scores[k])
    print("\n── Results ───────────────────────────────────")
    print(f"  ROUGE-1 : {avg('rouge1'):.4f}")
    print(f"  ROUGE-2 : {avg('rouge2'):.4f}")
    print(f"  ROUGE-L : {avg('rougeL'):.4f}")
    print("──────────────────────────────────────────────")

if __name__ == '__main__':
    evaluate()