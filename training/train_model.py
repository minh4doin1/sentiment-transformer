import torch
import pandas as pd
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    Trainer, 
    TrainingArguments,
    EarlyStoppingCallback
)
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import os

# Cấu hình nhãn cảm xúc
EMOTIONS = ["Enjoyment", "Sadness", "Fear", "Anger", "Disgust", "Surprise", "Other"]
label2id = {label: i for i, label in enumerate(EMOTIONS)}
id2label = {i: label for i, label in enumerate(EMOTIONS)}

def compute_metrics(eval_pred):
    """Tính toán Accuracy và F1-Score (Macro) để đánh giá mô hình chuẩn xác hơn"""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='macro')
    return {"accuracy": acc, "f1": f1}

def train():
    print("🚀 Bắt đầu quá trình huấn luyện toàn diện (GPU Optimized)...")
    
    # 1. Project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 2. Tải dữ liệu đã chuẩn bị
    train_df = pd.read_csv(os.path.join(root_dir, "data/train.csv"))
    val_df = pd.read_csv(os.path.join(root_dir, "data/validation.csv"))
    
    # 🌟 Cải tiến: Trọng số lớp để xử lý dữ liệu mất cân bằng (Imbalanced Data)
    # Tỉ lệ dựa trên: 1563 (max) / count
    class_weights = torch.tensor([
        1.0,   # Enjoyment
        1.77,  # Sadness
        13.24, # Fear
        3.88,  # Anger
        2.08,  # Disgust
        24.04, # Surprise
        1.05   # Other
    ]).to("cuda" if torch.cuda.is_available() else "cpu")

    # Tùy chỉnh Trainer để hỗ trợ Weighted Loss
    class WeightedTrainer(Trainer):
        def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
            labels = inputs.get("labels")
            outputs = model(**inputs)
            logits = outputs.get("logits")
            loss_fct = torch.nn.CrossEntropyLoss(weight=class_weights)
            loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
            return (loss, outputs) if return_outputs else loss
    
    # Chuẩn bị dataset cho HuggingFace
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    
    # 2. Tải Tokenizer và Model PhoBERT
    model_name = "vinai/phobert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, 
        num_labels=len(EMOTIONS),
        id2label=id2label,
        label2id=label2id
    )
    
    # 3. Tokenization function
    def tokenize_function(examples):
        tokens = tokenizer(examples["Sentence"], padding="max_length", truncation=True, max_length=128)
        tokens["label"] = [label2id[l] for l in examples["Emotion"]]
        return tokens

    print("Tokenizing data...")
    train_tokenized = train_dataset.map(tokenize_function, batched=True)
    val_tokenized = val_dataset.map(tokenize_function, batched=True)
    
    # 4. Cấu hình Training (Tối ưu cho GTX 1060 6GB)
    training_args = TrainingArguments(
        output_dir=os.path.join(root_dir, "models/checkpoints"),
        learning_rate=2e-5,
        per_device_train_batch_size=8, # Tăng lên 8 cho GPU 6GB
        per_device_eval_batch_size=8,
        num_train_epochs=3,            # Chạy full 3 epochs
        weight_decay=0.01,
        eval_strategy="epoch",  # Đánh giá sau mỗi epoch
        save_strategy="epoch",
        load_best_model_at_end=True,   # Tự động lấy model tốt nhất
        metric_for_best_model="f1",    # Dựa trên F1-score
        warmup_steps=500,             # Giai đoạn khởi động giúp học ổn định hơn
        logging_steps=50,             # Theo dõi log thường xuyên hơn
        logging_dir=os.path.join(root_dir, "logs"),
        report_to="none" 
    )
    
    # 5. Huấn luyện với WeightedTrainer (Tối ưu độ chính xác cho nhãn hiếm)
    trainer = WeightedTrainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=val_tokenized,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)] 
    )
    
    print("🎮 Đang huấn luyện với Weighted Loss (Chống lệch dữ liệu)...")
    trainer.train()
    
    # 6. Lưu mô hình cuối cùng
    print("Saving the best model...")
    final_output = os.path.join(root_dir, "models/final_model")
    model.save_pretrained(final_output)
    tokenizer.save_pretrained(final_output)
    
    print(f"✅ Hoàn tất! Model 'xịn' đã được lưu tại: {final_output}")

if __name__ == "__main__":
    train()
