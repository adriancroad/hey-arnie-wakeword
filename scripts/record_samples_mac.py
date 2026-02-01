#!/usr/bin/env python3
"""
Hey Arnie - Direct Mac Recording
Record wake word samples directly from your Mac's microphone

Usage: python record_samples_mac.py [--negative]

Controls:
  SPACE  = Record a sample (hold while speaking)
  S      = Skip / mark bad take
  Q      = Quit and save
"""

import subprocess
import sys
import os
import time
import tempfile
from pathlib import Path

# Check for required dependencies
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
except ImportError:
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "sounddevice", "soundfile", "numpy", "-q"])
    import sounddevice as sd
    import soundfile as sf
    import numpy as np

# Configuration
SAMPLE_RATE = 16000  # Required for microWakeWord
CHANNELS = 1         # Mono

def get_key():
    """Get a single keypress (macOS/Unix)"""
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def record_sample(duration=2.0):
    """Record audio for specified duration"""
    print("🔴 RECORDING...", end=" ", flush=True)
    audio = sd.rec(int(duration * SAMPLE_RATE), 
                   samplerate=SAMPLE_RATE, 
                   channels=CHANNELS,
                   dtype='float32')
    sd.wait()
    print("✅ Done!")
    return audio

def record_while_held():
    """Record while spacebar is held (push-to-talk style)"""
    print("🔴 RECORDING (release SPACE to stop)...", end=" ", flush=True)
    
    frames = []
    
    # Start recording stream
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32') as stream:
        while True:
            data, _ = stream.read(1024)
            frames.append(data.copy())
            
            # Check if key released (non-blocking check is tricky, use timeout)
            # For simplicity, record for max 3 seconds or until buffer
            if len(frames) > int(SAMPLE_RATE * 3 / 1024):
                break
    
    print("✅ Done!")
    return np.concatenate(frames)

def save_sample(audio, output_path):
    """Save audio to WAV file"""
    sf.write(output_path, audio, SAMPLE_RATE)

def list_microphones():
    """List available input devices"""
    print("\n🎤 Available microphones:")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            default = " (DEFAULT)" if i == sd.default.device[0] else ""
            print(f"   [{i}] {dev['name']}{default}")
    print()

def main():
    is_negative = "--negative" in sys.argv or "-n" in sys.argv
    
    sample_type = "NEGATIVE" if is_negative else "POSITIVE"
    output_dir = Path("samples/negative" if is_negative else "samples/positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Count existing samples
    existing = list(output_dir.glob("mac_*.wav"))
    sample_num = len(existing)
    
    print("🎤 HEY ARNIE - Mac Recording Studio")
    print("=" * 45)
    print(f"Recording: {sample_type} samples")
    print(f"Output: {output_dir}/")
    print(f"Starting from sample #{sample_num}")
    print()
    
    list_microphones()
    
    if is_negative:
        print("📝 Say phrases that should NOT trigger 'Hey Arnie'")
        print("   Examples: 'hey honey', 'harmony', 'turn on lights'")
    else:
        print("📝 Say 'HEY ARNIE' clearly when recording")
        print("   Vary your tone, speed, and distance from mic!")
    
    print()
    print("Controls:")
    print("  ENTER = Record 2-second sample")
    print("  Q     = Quit")
    print()
    print("Ready when you are! 💪")
    print("-" * 45)
    
    while True:
        print(f"\n[Sample #{sample_num}] Press ENTER to record (Q to quit): ", end="", flush=True)
        
        key = get_key()
        print()  # New line after keypress
        
        if key.lower() == 'q':
            print(f"\n✅ Session complete! Recorded {sample_num - len(existing)} new samples.")
            print(f"   Total in {output_dir}/: {sample_num}")
            break
        
        if key in ['\r', '\n', ' ']:
            # Countdown
            for i in [3, 2, 1]:
                print(f"   {i}...", end=" ", flush=True)
                time.sleep(0.5)
            print()
            
            # Record
            audio = record_sample(duration=2.0)
            
            # Trim silence from start/end
            threshold = 0.01
            nonsilent = np.where(np.abs(audio) > threshold)[0]
            if len(nonsilent) > 0:
                start = max(0, nonsilent[0] - 1600)  # 0.1s padding
                end = min(len(audio), nonsilent[-1] + 1600)
                audio = audio[start:end]
            
            # Save
            filename = f"mac_{sample_num:04d}.wav"
            output_path = output_dir / filename
            save_sample(audio, str(output_path))
            
            print(f"   💾 Saved: {filename} ({len(audio)/SAMPLE_RATE:.2f}s)")
            sample_num += 1

if __name__ == "__main__":
    main()
