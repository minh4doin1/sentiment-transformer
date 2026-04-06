from datasets import load_dataset
import pandas as pd
import os

def prepare_data():
    print("Downloading UIT-VSMEC dataset from HuggingFace...")
    # Load dataset
    dataset = load_dataset("tridm/UIT-VSMEC")
    
    # Project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Save splits for inspection and training
    for split in ['train', 'validation', 'test']:
        df = pd.DataFrame(dataset[split])
        output_path = os.path.join(data_dir, f"{split}.csv")
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved {split} set to {output_path} ({len(df)} rows)")

    print("Data preparation complete.")

if __name__ == "__main__":
    prepare_data()
