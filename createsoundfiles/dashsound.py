import wave
import math
import random
import struct
import os

os.makedirs("assets", exist_ok=True)

filename = os.path.join("assets", "dash_swoosh.wav")

sample_rate = 44100
duration = 0.28
volume = 0.65

samples = []

def square_wave(freq, t):
    return 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0

def triangle_wave(freq, t):
    return 2 * abs(2 * ((t * freq) % 1) - 1) - 1

for i in range(int(sample_rate * duration)):
    t = i / sample_rate
    p = t / duration

    # Dash envelope: quick attack, smooth fade
    attack = min(1.0, p * 12)
    fade = (1.0 - p) ** 1.8
    envelope = attack * fade

    # Rising then falling swoosh pitch
    sweep_freq = 280 + math.sin(p * math.pi) * 900
    sweep = triangle_wave(sweep_freq, t)

    # Bright arcade layer
    bright_freq = 700 + math.sin(p * math.pi) * 1200
    bright = square_wave(bright_freq, t)

    # Very light air/noise texture
    noise = random.uniform(-1, 1)

    # Noise fades quickly so it is not too harsh
    noise_env = max(0, 1.0 - p * 2.2)

    # Small ending pop
    pop_env = max(0, 1.0 - abs(p - 0.82) * 18)
    pop = square_wave(420, t) * pop_env

    # Mix
    sound = (
        sweep * 0.45 +
        bright * 0.18 +
        noise * 0.12 * noise_env +
        pop * 0.18
    )

    # Soft clipping for punch
    sound = math.tanh(sound * 1.4)

    # Light bitcrush for 8-bit game feel
    bitcrush_levels = 26
    sound = round(sound * bitcrush_levels) / bitcrush_levels

    # Apply envelope and volume
    sound *= envelope * volume

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