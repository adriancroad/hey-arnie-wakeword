# 🎤💪 "Hey Arnie" Custom Wake Word

Train a custom wake word for Home Assistant Voice Preview Edition and M5Stack Atom Echo devices.

**Goal:** Say "Hey Arnie" and your smart home responds!

---

## 📋 Prerequisites

- Mac (Apple Silicon or Intel)
- Home Assistant Voice PE and/or M5Stack Atom Echo
- iPhone for recording samples
- ~1-2 hours total time

---

## 🚀 Quick Start

### Step 1: Set Up Your Mac

Open Terminal and run:

```bash
# Download the setup script from your workspace
# (Or copy hey-arnie-wakeword folder to your Mac)

cd ~/hey-arnie-wakeword
chmod +x scripts/setup_mac.sh
./scripts/setup_mac.sh
```

This installs:
- Python + dependencies
- sox (audio processing)
- ffmpeg (media tools)
- microWakeWord training repo

### Step 2: Generate Synthetic Samples

```bash
cd ~/hey-arnie-wakeword
source venv/bin/activate
python scripts/generate_samples.py
```

This creates ~200 synthetic "Hey Arnie" samples using macOS voices.

### Step 3: Record Real Samples (IMPORTANT!)

Synthetic samples get you started, but **real recordings make it work well**.

#### Option A: Record Directly on Mac (Recommended) 🎤

```bash
python scripts/record_samples_mac.py
```

This opens an interactive recording session:
- Press **ENTER** to record a 2-second sample
- Say "Hey Arnie" clearly after the countdown
- Press **Q** when done
- Record 20-30 samples minimum

**For negative samples (phrases that shouldn't trigger):**
```bash
python scripts/record_samples_mac.py --negative
```

#### Option B: Record on iPhone, Transfer to Mac

1. Open **Voice Memos** app on iPhone
2. Say "Hey Arnie" with 1-2 second pauses between each
3. AirDrop recording to your Mac
4. Process it:
```bash
python scripts/process_iphone_recordings.py ~/Downloads/your_recording.m4a
```

**Tips for good samples:**
- Vary your tone (normal, tired, excited, questioning)
- Vary your distance (close, arm's length, across room)
- Get Angela and Alden to record too!
- Different voices = better accuracy

### Step 4: Generate Negative Samples

These are phrases that SHOULDN'T trigger the wake word:

```bash
python scripts/generate_negative_samples.py
```

### Step 5: Train the Model

```bash
python scripts/train_model.py
```

☕ This takes 30-60 minutes. Go walk Snob and Zigby!

### Step 6: Deploy to Your Devices

1. Copy `trained_model/hey_arnie.tflite` to your Home Assistant
   - Location: `config/esphome/hey_arnie.tflite`

2. Update your ESPHome device config (see `esphome_config_example.yaml`)

3. Install to your Voice PE / M5Stack Atoms

4. Test it: Say "Hey Arnie!" 🎉

---

## 📁 Project Structure

```
hey-arnie-wakeword/
├── README.md                    # You are here
├── esphome_config_example.yaml  # ESPHome configuration template
├── scripts/
│   ├── setup_mac.sh             # Mac environment setup
│   ├── generate_samples.py      # Create synthetic wake word samples
│   ├── generate_negative_samples.py  # Create non-wake-word samples
│   ├── process_iphone_recordings.py  # Convert iPhone recordings
│   └── train_model.py           # Train the model
├── samples/
│   ├── positive/                # "Hey Arnie" samples
│   └── negative/                # Non-wake-word samples
├── trained_model/
│   └── hey_arnie.tflite         # Output model (after training)
└── microWakeWord/               # Training framework (cloned)
```

---

## 🔧 Troubleshooting

### Model triggers on wrong words
- Add more negative samples of similar-sounding words
- Increase `probability_cutoff` in ESPHome config

### Model doesn't trigger reliably
- Record more real voice samples
- Decrease `probability_cutoff` in ESPHome config
- Make sure samples are clear (no background noise)

### Training fails
- Check you have enough samples (50+ positive, 30+ negative)
- Ensure Python virtual environment is activated
- Check microWakeWord GitHub for updated instructions

---

## 📚 Resources

- [microWakeWord GitHub](https://github.com/kahrendt/microWakeWord)
- [Home Assistant Voice](https://www.home-assistant.io/voice_control/)
- [ESPHome micro_wake_word](https://esphome.io/components/micro_wake_word.html)

---

*Built with 💪 by Arnie*

*"I'll be listening... for 'Hey Arnie'!"*
