#!/usr/bin/env python3
"""
Hey Arnie - iPhone Recording Processor
Converts and splits iPhone Voice Memo recordings into training samples

Usage:
1. Record yourself saying "Hey Arnie" with pauses between each one
2. AirDrop the recording to your Mac
3. Run: python process_iphone_recordings.py /path/to/recording.m4a

The script will:
- Convert to proper format (16kHz mono WAV)
- Split on silence to get individual samples
- Save to samples/positive/
"""

import subprocess
import sys
import os
from pathlib import Path

def process_recording(input_file, output_dir="samples/positive", prefix="real"):
    """Process an iPhone recording into individual samples"""
    
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        return
    
    print(f"🎤 Processing: {input_path.name}")
    
    # Count existing real samples to continue numbering
    existing = list(output_path.glob(f"{prefix}_*.wav"))
    start_num = len(existing)
    
    # Step 1: Convert to WAV (16kHz mono)
    temp_wav = output_path / "temp_full.wav"
    print("  Converting to WAV...")
    subprocess.run([
        'sox', str(input_path),
        '-r', '16000',
        '-c', '1',
        '-b', '16',
        str(temp_wav)
    ], check=True, capture_output=True)
    
    # Step 2: Split on silence
    print("  Splitting on silence...")
    output_pattern = output_path / f"{prefix}_{start_num:04d}_.wav"
    
    # Sox silence command to split on pauses
    subprocess.run([
        'sox', str(temp_wav),
        str(output_path / f"{prefix}_.wav"),
        'silence', '1', '0.1', '1%',  # Strip leading silence
        '1', '0.3', '1%',              # Split on 0.3s silence
        ':', 'newfile', ':', 'restart'
    ], check=True, capture_output=True)
    
    # Clean up temp file
    temp_wav.unlink()
    
    # Rename split files with proper numbering
    split_files = sorted(output_path.glob(f"{prefix}_*.wav"))
    renamed_count = 0
    
    for i, f in enumerate(split_files):
        # Skip very short files (< 0.3 seconds = likely noise)
        result = subprocess.run(
            ['sox', '--i', '-D', str(f)],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
        
        if duration < 0.3:
            f.unlink()  # Remove too-short samples
            continue
        
        if duration > 3.0:
            f.unlink()  # Remove too-long samples (probably multiple words)
            continue
        
        new_name = output_path / f"{prefix}_{start_num + renamed_count:04d}.wav"
        f.rename(new_name)
        renamed_count += 1
    
    print(f"✅ Extracted {renamed_count} samples!")
    print(f"   Saved to: {output_path}/")
    
    return renamed_count

def main():
    if len(sys.argv) < 2:
        print("🎤 Hey Arnie - iPhone Recording Processor")
        print("=" * 45)
        print("\nUsage: python process_iphone_recordings.py <recording.m4a>")
        print("\nTips for recording on iPhone:")
        print("  1. Open Voice Memos app")
        print("  2. Start recording")
        print("  3. Say 'Hey Arnie' with 1-2 second pauses between")
        print("  4. Record 20-30 times")
        print("  5. Stop and AirDrop to your Mac")
        print("  6. Run this script on the file")
        print("\nFor best results:")
        print("  - Vary your tone (normal, excited, tired, questioning)")
        print("  - Vary your distance (close, arm's length, across room)")
        print("  - Get Angela and Alden to record too!")
        return
    
    for input_file in sys.argv[1:]:
        process_recording(input_file)

if __name__ == "__main__":
    main()
