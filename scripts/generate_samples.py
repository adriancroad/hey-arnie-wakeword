#!/usr/bin/env python3
"""
Hey Arnie - Synthetic Sample Generator
Generates TTS samples for wake word training using macOS voices

Run: python generate_samples.py
"""

import subprocess
import os
from pathlib import Path
import random

# Wake word variations
WAKE_WORDS = [
    "hey arnie",
    "hey arnie", 
    "hey arnie",
    "arnie",
    "hey arnold",
    "hay arnie",  # Common mishearing
]

# macOS voices to use (variety helps training)
# Run 'say -v ?' to see all available voices
MACOS_VOICES = [
    "Alex",        # US Male
    "Daniel",      # UK Male
    "Fred",        # US Male
    "Karen",       # AU Female
    "Moira",       # IE Female
    "Oliver",      # UK Male
    "Samantha",    # US Female
    "Tessa",       # ZA Female
    "Tom",         # US Male
    "Veena",       # IN Female
]

# Rate variations (words per minute)
RATES = [140, 160, 180, 200, 220]

def get_available_voices():
    """Get list of voices actually installed on this Mac"""
    result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
    available = []
    for line in result.stdout.strip().split('\n'):
        voice_name = line.split()[0]
        if voice_name in MACOS_VOICES:
            available.append(voice_name)
    
    # If none of our preferred voices, use whatever's available
    if not available:
        for line in result.stdout.strip().split('\n'):
            available.append(line.split()[0])
    
    return available[:10]  # Max 10 voices

def generate_sample(text, voice, rate, output_path):
    """Generate a single audio sample using macOS say command"""
    # Generate AIFF first (native format)
    aiff_path = output_path.replace('.wav', '.aiff')
    
    cmd = [
        'say',
        '-v', voice,
        '-r', str(rate),
        '-o', aiff_path,
        text
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Convert to WAV (16kHz mono - required for microWakeWord)
    subprocess.run([
        'sox', aiff_path, 
        '-r', '16000',  # 16kHz sample rate
        '-c', '1',       # Mono
        '-b', '16',      # 16-bit
        output_path
    ], check=True, capture_output=True)
    
    # Clean up AIFF
    os.remove(aiff_path)
    
    return output_path

def main():
    print("🎤 HEY ARNIE - Synthetic Sample Generator")
    print("=" * 45)
    
    output_dir = Path("samples/positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    voices = get_available_voices()
    print(f"✅ Found {len(voices)} voices: {', '.join(voices)}")
    
    sample_count = 0
    target_samples = 200  # Generate 200 synthetic samples
    
    print(f"\n🔄 Generating {target_samples} samples...")
    
    while sample_count < target_samples:
        for wake_word in WAKE_WORDS:
            for voice in voices:
                for rate in RATES:
                    if sample_count >= target_samples:
                        break
                    
                    filename = f"synthetic_{sample_count:04d}_{voice}_{rate}.wav"
                    output_path = output_dir / filename
                    
                    try:
                        generate_sample(wake_word, voice, rate, str(output_path))
                        sample_count += 1
                        
                        if sample_count % 20 == 0:
                            print(f"  Generated {sample_count}/{target_samples} samples...")
                    
                    except Exception as e:
                        print(f"  ⚠️ Failed: {voice} @ {rate}wpm - {e}")
                
                if sample_count >= target_samples:
                    break
            if sample_count >= target_samples:
                break
    
    print(f"\n✅ Generated {sample_count} synthetic samples in {output_dir}/")
    print("\n💪 Next: Record real samples with your iPhone!")
    print("   - Say 'Hey Arnie' 20-30 times")
    print("   - Vary your distance, tone, and speed")
    print("   - Get Angela and Alden to record some too!")

if __name__ == "__main__":
    main()
