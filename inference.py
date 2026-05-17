# src/inference.py
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


PRETRAINED_MODEL = "csebuetnlp/mT5_multilingual_XLSum"

class Summarizer:
    def __init__(self, model_path=None):
        print("Loading csebuetnlp/mT5_multilingual_XLSum...")
        print("First run downloads ~2GB — please wait...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Use the professionally fine-tuned multilingual model
        self.tokenizer = AutoTokenizer.from_pretrained(
            PRETRAINED_MODEL,
            use_fast=False
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            PRETRAINED_MODEL
        ).to(self.device)
        self.model.eval()
        print(f"Model loaded on {self.device.upper()}!")

    def summarize(self, text, max_input=512, max_summary=128, num_beams=4):
        if not text or len(text.strip()) < 20:
            return "Please enter a longer text."

        # This model requires a special whitespace token
        WHITESPACE_HANDLER = lambda k: re.sub(
            r'\s+', ' ', re.sub(r'\n+', ' ', k.strip())
        )

        inputs = self.tokenizer(
            WHITESPACE_HANDLER(text),
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=max_input
        ).to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                input_ids            = inputs["input_ids"],
                attention_mask       = inputs["attention_mask"],
                max_length           = max_summary,
                num_beams            = num_beams,
                length_penalty       = 2.0,
                no_repeat_ngram_size = 3,
                early_stopping       = True
            )

        summary = self.tokenizer.decode(
            output[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )
        return summary
