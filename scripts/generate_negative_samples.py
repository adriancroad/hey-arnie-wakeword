#!/usr/bin/env python3
"""
Hey Arnie - Negative Sample Generator
Generates samples that should NOT trigger the wake word

These include:
- Similar sounding words
- Common household phrases
- Random speech
"""

import subprocess
import os
from pathlib import Path
import random

# Phrases that should NOT trigger "Hey Arnie"
NEGATIVE_PHRASES = [
    # Similar sounding
    "harmony",
    "army",
    "hey barney",
    "hey johnny", 
    "hey honey",
    "alarming",
    "farming",
    "charming",
    "arty",
    "party",
    "hearty",
    
    # Common household phrases
    "hey google",
    "hey siri",
    "alexa",
    "turn on the lights",
    "what's the weather",
    "play some music",
    "set a timer",
    "good morning",
    "good night",
    "dinner is ready",
    "come here",
    "hello",
    "excuse me",
    "thank you",
    "what time is it",
    "open the door",
    "close the door",
    
    # Random speech
    "the quick brown fox",
    "i need to go shopping",
    "what's for dinner",
    "have you seen my keys",
    "the dogs need walking",
    "formula one race",
    "star trek is on",
    "watching farscape",
    "roblox time",
    "three d printing",
    "home assistant",
    "raspberry pie",
]

MACOS_VOICES = ["Alex", "Daniel", "Samantha", "Karen", "Oliver"]
RATES = [160, 180, 200]

def get_available_voices():
    result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
    available = []
    for line in result.stdout.strip().split('\n'):
        voice_name = line.split()[0]
        if voice_name in MACOS_VOICES:
            available.append(voice_name)
    return available if available else ["Alex"]

def generate_sample(text, voice, rate, output_path):
    aiff_path = output_path.replace('.wav', '.aiff')
    
    subprocess.run([
        'say', '-v', voice, '-r', str(rate), '-o', aiff_path, text
    ], check=True, capture_output=True)
    
    subprocess.run([
        'sox', aiff_path, '-r', '16000', '-c', '1', '-b', '16', output_path
    ], check=True, capture_output=True)
    
    os.remove(aiff_path)

def main():
    print("🚫 HEY ARNIE - Negative Sample Generator")
    print("=" * 45)
    
    output_dir = Path("samples/negative")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    voices = get_available_voices()
    print(f"✅ Using voices: {', '.join(voices)}")
    
    sample_count = 0
    
    print(f"\n🔄 Generating negative samples...")
    
    for phrase in NEGATIVE_PHRASES:
        voice = random.choice(voices)
        rate = random.choice(RATES)
        
        filename = f"negative_{sample_count:04d}.wav"
        output_path = output_dir / filename
        
        try:
            generate_sample(phrase, voice, rate, str(output_path))
            sample_count += 1
            
            if sample_count % 10 == 0:
                print(f"  Generated {sample_count} samples...")
        
        except Exception as e:
            print(f"  ⚠️ Failed: {phrase} - {e}")
    
    print(f"\n✅ Generated {sample_count} negative samples in {output_dir}/")
    print("\n💡 For better training, also add:")
    print("   - TV/movie audio clips")
    print("   - Music snippets")
    print("   - Background noise recordings")

if __name__ == "__main__":
    main()
