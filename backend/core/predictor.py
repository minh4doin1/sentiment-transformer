import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from underthesea import word_tokenize
from .normalizer import normalize_teencode
from .lexicon import get_all_keywords
import os

class SentimentPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            # Calculate root path relative to this file: backend/core/predictor.py -> backend/core -> backend -> root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(os.path.dirname(current_dir))
            model_path = os.path.join(root_dir, "models/final_model")
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
            
            # Get peak emotion and confidence
            top_prob = probs.max().item()
            top_index = probs.argmax().item()
            top_label = self.labels[top_index]
            
            # High Precision Logic: Thresholding
            threshold = 0.5 
            is_uncertain = top_prob < threshold
            
            return {
                "top_emotion": top_label if not is_uncertain else "Uncertain",
                "probabilities": results,
                "confidence": float(top_prob),
                "is_uncertain": is_uncertain,
                "highlights": list(set(highlights))
            }
        else:
            return {
                "top_emotion": "Other",
                "probabilities": {label: 1.0/len(self.labels) for label in self.labels},
                "confidence": 0.0,
                "is_uncertain": True,
                "highlights": list(set(highlights)),
                "message": "Model not trained yet."
            }

if __name__ == "__main__":
    predictor = SentimentPredictor()
    print(predictor.predict("Tôi rất hnay vui quá xá luôn á"))
