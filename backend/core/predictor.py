import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from underthesea import word_tokenize
from .normalizer import normalize_teencode
from .lexicon import get_all_keywords
import os

class SentimentPredictor:
    def __init__(self, model_path="d:/side_project/sentiment-transformer-thesis/models/final_model"):
        self.labels = ["Enjoyment", "Sadness", "Fear", "Anger", "Disgust", "Surprise", "Other"]
        self.emotion_lexicon = get_all_keywords()
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        if os.path.exists(model_path):
            print(f"Loading custom fine-tuned model from {model_path}...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path).to(self.device).eval()
        else:
            print("WARNING: Custom model not found. Using default PhoBERT or placeholder logic.")
            # Fallback for testing UI before training
            self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
            self.model = None

    def predict(self, text):
        raw_text = text
        # 1. Normalization
        text = normalize_teencode(text)
        
        # 2. Key keywords extraction (Explainability) using Lexicon
        highlights = [word for word in text.split() if word.lower() in self.emotion_lexicon]
        
        # 3. Word Segmentation
        text = word_tokenize(text, format="text")
        
        # 4. Model Inference
        if self.model:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            results = {}
            for i, label in enumerate(self.labels):
                results[label] = float(probs[0][i])
            
            # Get peak emotion
            top_label = self.labels[probs.argmax().item()]
            return {
                "top_emotion": top_label,
                "probabilities": results,
                "confidence": float(probs.max()),
                "highlights": list(set(highlights))
            }
        else:
            return {
                "top_emotion": "Other",
                "probabilities": {label: 1.0/len(self.labels) for label in self.labels},
                "confidence": 0.0,
                "highlights": list(set(highlights)),
                "message": "Model not trained yet."
            }

if __name__ == "__main__":
    predictor = SentimentPredictor()
    print(predictor.predict("Tôi rất hnay vui quá xá luôn á"))
