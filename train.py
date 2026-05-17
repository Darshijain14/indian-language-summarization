# src/train.py


import os
import sys
import torch

# Fixing Windows path issue so preprocess can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback
)
from preprocess import load_and_clean_data, split_data, SummarizationDataset

#  Config 
MODEL_NAME  = "google/mt5-small"
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'model', 'mt5_summarizer')
DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset.csv')
EPOCHS      = 3
BATCH_SIZE  = 2      # Keep at 2 for Windows CPU (use 4 if you have GPU)
LR          = 5e-4

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device.upper()}")
print(f"Output will be saved to: {os.path.abspath(OUTPUT_DIR)}")

# Loading model
print("Downloading/loading mT5-small (first run downloads ~1.2GB)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.to(device)

# Loading data 
df = load_and_clean_data(DATA_PATH)
train_df, val_df, test_df = split_data(df)

# Save test set for evaluation later
test_df.to_csv(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.csv'),
    index=False, encoding='utf-8'
)

train_ds = SummarizationDataset(train_df, tokenizer)
val_ds   = SummarizationDataset(val_df,   tokenizer)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

# Training arguments 
args = Seq2SeqTrainingArguments(
    output_dir                  = OUTPUT_DIR,
    num_train_epochs            = EPOCHS,
    per_device_train_batch_size = BATCH_SIZE,
    per_device_eval_batch_size  = BATCH_SIZE,
    learning_rate               = LR,
    warmup_steps                = 100,
    weight_decay                = 0.01,
    logging_dir                 = os.path.join(OUTPUT_DIR, 'logs'),
    logging_steps               = 20,
    evaluation_strategy         = "epoch",
    save_strategy               = "epoch",
    load_best_model_at_end      = True,
    predict_with_generate       = True,
    generation_max_length       = 64,
    fp16                        = False,   # Set True only if you have NVIDIA GPU
    report_to                   = "none",  # Disable Weights & Biases
    dataloader_num_workers      = 0,       # Required on Windows (avoid multiprocessing errors)
)

#  Trainer 
trainer = Seq2SeqTrainer(
    model         = model,
    args          = args,
    train_dataset = train_ds,
    eval_dataset  = val_ds,
    tokenizer     = tokenizer,
    data_collator = data_collator,
    callbacks     = [EarlyStoppingCallback(early_stopping_patience=2)]
)

#  Train 
print("Starting training... (this will take 30-60 min on CPU)")
trainer.train()

# Save 
os.makedirs(OUTPUT_DIR, exist_ok=True)
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"Model saved to: {os.path.abspath(OUTPUT_DIR)}")
