import os
import sys
import subprocess
import wave
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from openwakeword.utils import AudioFeatures

# Define voices and rates to use for training data generation
VOICES = ["Daniel", "Samantha", "Kathy", "Fred", "Karen", "Rishi", "Tara", "Albert", "Moira", "Fiona", "Tessa", "Veena"]
RATES = [140, 175, 210]

# Positive and negative phrases
POS_PHRASES = ["Hey Avelyn"]
NEG_PHRASES = [
    "Hey Jarvis",
    "Alexa",
    "Hey Google",
    "Hey Siri",
    "improve this prompt",
    "make this better",
    "hello",
    "what time is it",
    "good morning"
]

def generate_audio(phrase, voice, rate, filepath):
    cmd = [
        "say",
        "-v", voice,
        "-r", str(rate),
        "-o", filepath,
        "--file-format=WAVE",
        "--data-format=LEI16@16000",
        phrase
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class WakeWordClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(
            nn.Linear(16 * 96, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(self.flatten(x))

def main():
    print("Initializing feature extractor...")
    extractor = AudioFeatures(inference_framework='onnx')

    # Create temporary directory for audio generation
    temp_dir = "scratch/temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    X_pos = []
    X_neg = []

    print("Generating positive samples...")
    for phrase in POS_PHRASES:
        for voice in VOICES:
            for rate in RATES:
                filename = f"pos_{voice}_{rate}.wav"
                filepath = os.path.join(temp_dir, filename)
                generate_audio(phrase, voice, rate, filepath)
                
                if not os.path.exists(filepath):
                    continue

                # Load wav and pad
                with wave.open(filepath, 'rb') as wf:
                    data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
                
                # Pad with 1 second of silence on both sides
                padded_data = np.concatenate((
                    np.zeros(16000, dtype=np.int16),
                    data,
                    np.zeros(16000, dtype=np.int16)
                ))

                # Extract embeddings
                emb = extractor._get_embeddings(padded_data)
                if emb.shape[0] < 16:
                    continue

                # Slide window and find the window with max raw RMS energy to align the wake word
                n_chunks = len(padded_data) // 1280
                rms = []
                for j in range(n_chunks):
                    chunk = padded_data[j*1280:(j+1)*1280]
                    rms.append(np.sqrt(np.mean(chunk.astype(np.float64)**2)))

                # Find window of size 16 that maximizes sum of RMS
                max_energy = -1
                best_idx = 0
                for idx in range(emb.shape[0] - 16 + 1):
                    energy = sum(rms[idx:idx+16])
                    if energy > max_energy:
                        max_energy = energy
                        best_idx = idx

                X_pos.append(emb[best_idx:best_idx+16])

    print(f"Collected {len(X_pos)} positive samples.")

    print("Generating negative samples...")
    for phrase in NEG_PHRASES:
        for voice in VOICES:
            for rate in RATES:
                filename = f"neg_{phrase.replace(' ', '_')}_{voice}_{rate}.wav"
                filepath = os.path.join(temp_dir, filename)
                generate_audio(phrase, voice, rate, filepath)

                if not os.path.exists(filepath):
                    continue

                with wave.open(filepath, 'rb') as wf:
                    data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

                padded_data = np.concatenate((
                    np.zeros(16000, dtype=np.int16),
                    data,
                    np.zeros(16000, dtype=np.int16)
                ))

                emb = extractor._get_embeddings(padded_data)
                if emb.shape[0] < 16:
                    continue

                # Collect all windows from negative files
                for idx in range(emb.shape[0] - 16 + 1):
                    X_neg.append(emb[idx:idx+16])

    print(f"Collected {len(X_neg)} negative samples.")

    # Clean up temp files
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    # Convert to tensors
    X_pos = np.array(X_pos, dtype=np.float32)
    X_neg = np.array(X_neg, dtype=np.float32)

    y_pos = np.ones((X_pos.shape[0], 1), dtype=np.float32)
    y_neg = np.zeros((X_neg.shape[0], 1), dtype=np.float32)

    X = np.vstack((X_pos, X_neg))
    y = np.vstack((y_pos, y_neg))

    # Shuffle dataset
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]

    # Split into train / val
    split = int(0.8 * X.shape[0])
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = WakeWordClassifier().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Training wake word model...")
    epochs = 80
    batch_size = 32

    for epoch in range(epochs):
        model.train()
        permutation = torch.randperm(X_train.shape[0])
        epoch_loss = 0
        for i in range(0, X_train.shape[0], batch_size):
            indices = permutation[i:i+batch_size]
            batch_x = torch.tensor(X_train[indices]).to(device)
            batch_y = torch.tensor(y_train[indices]).to(device)

            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(indices)

        model.eval()
        with torch.no_grad():
            val_x = torch.tensor(X_val).to(device)
            val_y = torch.tensor(y_val).to(device)
            val_outputs = model(val_x)
            val_loss = criterion(val_outputs, val_y).item()
            preds = (val_outputs >= 0.5).float()
            correct = (preds == val_y).sum().item()
            val_acc = correct / len(val_y)

        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch {epoch+1:02d}/{epochs} - Train Loss: {epoch_loss/X_train.shape[0]:.4f} - Val Loss: {val_loss:.4f} - Val Acc: {val_acc*100:.2f}%")

    # Final evaluation on the entire dataset
    model.eval()
    with torch.no_grad():
        all_x = torch.tensor(X).to(device)
        all_y = torch.tensor(y).to(device)
        all_outputs = model(all_x)
        preds = (all_outputs >= 0.5).float()
        
        # False positives and false negatives
        true_pos = ((preds == 1) & (all_y == 1)).sum().item()
        false_pos = ((preds == 1) & (all_y == 0)).sum().item()
        true_neg = ((preds == 0) & (all_y == 0)).sum().item()
        false_neg = ((preds == 0) & (all_y == 1)).sum().item()

        accuracy = (true_pos + true_neg) / len(y)
        fpr = false_pos / (true_neg + false_pos) if (true_neg + false_pos) > 0 else 0
        fnr = false_neg / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0

        print("\n=== Training Summary ===")
        print(f"Accuracy: {accuracy*100:.2f}%")
        print(f"False Positive Rate (FPR): {fpr*100:.4f}% ({false_pos}/{true_neg + false_pos})")
        print(f"False Negative Rate (FNR): {fnr*100:.2f}% ({false_neg}/{true_pos + false_neg})")

    # Export to ONNX
    print("\nExporting model to ONNX...")
    assets_models_dir = "assets/models"
    os.makedirs(assets_models_dir, exist_ok=True)
    onnx_path = os.path.join(assets_models_dir, "hey_avelyn.onnx")

    dummy_input = torch.randn(1, 16, 96).to(device)
    model.eval()
    
    # We must match the input/output names.
    # Openwakeword uses dynamic batch sizes if possible, but mostly single predictions.
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=15,
        do_constant_folding=True,
        input_names=['x.1'],
        output_names=['53'],
        dynamic_axes={'x.1': {0: 'batch_size'}, '53': {0: 'batch_size'}}
    )

    print(f"Custom model successfully saved to: {onnx_path}")

if __name__ == "__main__":
    main()
