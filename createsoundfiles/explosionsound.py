import wave
import math
import random
import struct
import os

os.makedirs("assets", exist_ok=True)

filename = os.path.join("assets", "balanced_comet_explosion.wav")

sample_rate = 44100
duration = 0.38
volume = 0.78

samples = []

def square_wave(freq, t):
    return 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0

def triangle_wave(freq, t):
    return 2 * abs(2 * ((t * freq) % 1) - 1) - 1

for i in range(int(sample_rate * duration)):
    t = i / sample_rate
    p = t / duration

    # Main fade
    main_env = (1.0 - p) ** 2.7

    # Crisp initial attack
    click_env = max(0, 1.0 - p * 60)
    click = square_wave(1600, t) * click_env

    # Small hollow boom/body, not too dominant
    boom_freq = 155 * (1.0 - p) + 65
    boom = math.sin(2 * math.pi * boom_freq * t) * main_env

    # Mid punch so it does not sound empty
    punch_freq = 380 * (1.0 - p) + 150
    punch = triangle_wave(punch_freq, t) * main_env

    # Rocky pixel snap
    snap_env = max(0, 1.0 - p * 16)
    snap = square_wave(520, t) * snap_env

    # Small bright sparkle
    sparkle_env = max(0, 1.0 - abs(p - 0.2) * 9)
    sparkle_freq = random.choice([900, 1100, 1300, 1600])
    sparkle = square_wave(sparkle_freq, t) * sparkle_env

    # Tiny noise only at beginning
    noise_env = max(0, 1.0 - p * 30)
    noise = random.uniform(-1, 1) * noise_env

    # Balanced mix
    sound = (
        click * 0.28 +
        boom * 0.24 +
        punch * 0.36 +
        snap * 0.24 +
        sparkle * 0.08 +
        noise * 0.035
    )

    # Punchy soft clipping
    sound = math.tanh(sound * 1.7)

    # 8-bit style, but still clean
    bitcrush_levels = 22
    sound = round(sound * bitcrush_levels) / bitcrush_levels

    # Apply fade and volume
    sound *= main_env * volume

    # Clamp
    sound = max(-1, min(1, sound))

    samples.append(int(sound * 32767))

with wave.open(filename, "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    for sample in samples:
        wav.writeframes(struct.pack("<h", sample))

print("Created:", filename)