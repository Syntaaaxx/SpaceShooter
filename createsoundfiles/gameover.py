import wave
import math
import struct
import os

os.makedirs("assets", exist_ok=True)

filename = os.path.join("assets", "game_over_8bit.wav")

sample_rate = 44100
volume = 0.65

samples = []

def square_wave(freq, t):
    return 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0

def add_note(freq, duration, volume_multiplier=1.0):
    note_samples = int(sample_rate * duration)

    for i in range(note_samples):
        t = i / sample_rate
        p = i / note_samples

        # Fade in/out to avoid ugly clicks
        attack = min(1.0, p * 12)
        release = min(1.0, (1.0 - p) * 8)
        envelope = attack * release

        tone = square_wave(freq, t)

        # Add a tiny lower octave for weight
        sub = square_wave(freq / 2, t) * 0.25

        sound = (tone * 0.75 + sub) * envelope
        sound *= volume * volume_multiplier

        # Clamp
        sound = max(-1, min(1, sound))

        samples.append(int(sound * 32767))

def add_silence(duration):
    for _ in range(int(sample_rate * duration)):
        samples.append(0)

# Falling "game over" melody
add_note(440, 0.18, 0.75)   # A
add_silence(0.04)

add_note(392, 0.18, 0.75)   # G
add_silence(0.04)

add_note(330, 0.22, 0.75)   # E
add_silence(0.05)

add_note(262, 0.35, 0.85)   # C
add_silence(0.06)

# Final low sad note
add_note(196, 0.65, 1.0)    # G low

with wave.open(filename, "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    for sample in samples:
        wav.writeframes(struct.pack("<h", sample))

print("Created:", filename)