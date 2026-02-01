#!/usr/bin/env python3
"""
Hey Arnie - Wake Word Model Trainer
Trains a microWakeWord model using collected samples

This wraps the microWakeWord training process with Hey Arnie defaults.
"""

import subprocess
import os
import sys
from pathlib import Path
import shutil

def check_samples():
    """Verify we have enough samples"""
    pos_dir = Path("samples/positive")
    neg_dir = Path("samples/negative")
    
    pos_count = len(list(pos_dir.glob("*.wav"))) if pos_dir.exists() else 0
    neg_count = len(list(neg_dir.glob("*.wav"))) if neg_dir.exists() else 0
    
    print(f"📊 Sample counts:")
    print(f"   Positive (wake word): {pos_count}")
    print(f"   Negative (not wake):  {neg_count}")
    print()
    
    if pos_count < 50:
        print("⚠️  Warning: Less than 50 positive samples!")
        print("   Recommend at least 100-200 for good accuracy.")
        print("   Run generate_samples.py and record more with your iPhone.")
        return False
    
    if neg_count < 30:
        print("⚠️  Warning: Less than 30 negative samples!")
        print("   Run generate_negative_samples.py for more.")
        return False
    
    return True

def train():
    """Run the training process"""
    print("🏋️ HEY ARNIE - Model Training")
    print("=" * 45)
    print()
    
    if not check_samples():
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Check if microWakeWord is cloned
    mww_dir = Path("microWakeWord")
    if not mww_dir.exists():
        print("📥 Cloning microWakeWord repository...")
        subprocess.run([
            'git', 'clone', 
            'https://github.com/kahrendt/microWakeWord.git'
        ], check=True)
    
    # Prepare training data in microWakeWord format
    print("\n📁 Preparing training data...")
    
    train_dir = mww_dir / "training_data" / "hey_arnie"
    train_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy positive samples
    pos_target = train_dir / "positive"
    pos_target.mkdir(exist_ok=True)
    for f in Path("samples/positive").glob("*.wav"):
        shutil.copy(f, pos_target / f.name)
    
    # Copy negative samples  
    neg_target = train_dir / "negative"
    neg_target.mkdir(exist_ok=True)
    for f in Path("samples/negative").glob("*.wav"):
        shutil.copy(f, neg_target / f.name)
    
    print("✅ Training data prepared")
    
    # Run training
    print("\n🔥 Starting training (this may take 30-60 minutes)...")
    print("   Go grab a protein shake! 💪\n")
    
    os.chdir(mww_dir)
    
    # The actual training command depends on microWakeWord's interface
    # This is a template - may need adjustment based on their current API
    try:
        subprocess.run([
            sys.executable, 'train.py',
            '--name', 'hey_arnie',
            '--epochs', '50',
            '--batch-size', '32'
        ], check=True)
        
        print("\n✅ Training complete!")
        
        # Copy output model
        model_file = Path("models/hey_arnie.tflite")
        if model_file.exists():
            output_dir = Path("../trained_model")
            output_dir.mkdir(exist_ok=True)
            shutil.copy(model_file, output_dir / "hey_arnie.tflite")
            print(f"📦 Model saved to: trained_model/hey_arnie.tflite")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training failed: {e}")
        print("\nThe microWakeWord training interface may have changed.")
        print("Check their README for current instructions:")
        print("https://github.com/kahrendt/microWakeWord")
    except FileNotFoundError:
        print("\n⚠️  Training script not found in microWakeWord repo.")
        print("The repo structure may have changed. Check their docs.")
        print("https://github.com/kahrendt/microWakeWord")

def main():
    train()

if __name__ == "__main__":
    main()
