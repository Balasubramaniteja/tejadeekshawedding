"""
Generates an original, loopable Carnatic 'mangala vadyam' style instrumental
(nadaswaram-like lead + tanpura drone + thavil-like percussion) in raga Mohanam.
Written from scratch — no samples, no copyrighted material.
"""
import numpy as np, subprocess, os

SR = 44100
BPM = 68
BEAT = 60.0 / BPM
SA = 146.83          # D3 tonic

# Mohanam (pentatonic): S R2 G3 P D2
RATIOS = {'S': 1.0, 'R': 9/8, 'G': 5/4, 'P': 3/2, 'D': 5/3, "S'": 2.0, "R'": 9/4, "G'": 5/2, 'D,': 5/6, 'P,': 3/4}

def env_adsr(n, a=0.04, d=0.10, s=0.72, r=0.22):
    a_n, d_n, r_n = int(a*SR), int(d*SR), int(r*SR)
    a_n = min(a_n, n//4); d_n = min(d_n, n//4); r_n = min(r_n, n//3)
    s_n = max(1, n - a_n - d_n - r_n)
    return np.concatenate([
        np.linspace(0, 1, a_n, endpoint=False),
        np.linspace(1, s, d_n, endpoint=False),
        np.full(s_n, s),
        np.linspace(s, 0, r_n)
    ])[:n]

def nadaswaram(freq, dur, amp=0.55, gliss_from=None):
    """Reedy double-reed timbre: strong odd+even harmonics, nasal formant, vibrato."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    # pitch: optional short glide in (gamaka), plus vibrato that fades in
    vib_depth = 0.007 * np.clip((t - 0.12) / 0.25, 0, 1)
    vib = 1 + vib_depth * np.sin(2*np.pi*5.4*t)
    f = np.full(n, float(freq))
    if gliss_from:
        g = int(min(0.09, dur*0.35) * SR)
        f[:g] = np.linspace(gliss_from, freq, g)
    phase = 2*np.pi*np.cumsum(f * vib) / SR
    # harmonic series with a nasal peak around the 3rd-5th partial
    harm = [1.0, 0.62, 0.78, 0.55, 0.46, 0.24, 0.16, 0.10, 0.06]
    y = np.zeros(n)
    for k, a in enumerate(harm, start=1):
        y += a * np.sin(k * phase)
    y /= sum(harm)
    # slight breath noise
    y += 0.012 * np.random.default_rng(int(freq)).normal(0, 1, n) * np.linspace(1, .3, n)
    return y * env_adsr(n) * amp

def tanpura(dur, amp=0.16):
    """Sustained Sa + Pa drone with slow shimmer."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f, a in [(SA/2, 1.0), (SA, .72), (SA*1.5, .5), (SA*2, .28), (SA*3, .12)]:
        shimmer = 1 + 0.0022*np.sin(2*np.pi*0.21*t + f)
        y += a * np.sin(2*np.pi*f*t*shimmer)
        y += a*0.28 * np.sin(2*np.pi*f*1.001*t)
    y /= 3.4
    return y * amp

def thavil(dur_total, pattern):
    """Simple thavil-ish strokes: low membrane thump + crisp right-hand tap."""
    n = int(dur_total * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(7)
    for beat, kind, vel in pattern:
        i = int(beat * BEAT * SR)
        if i >= n: continue
        if kind == 'low':
            d = int(0.28*SR); t = np.arange(d)/SR
            f = 92*np.exp(-9*t) + 58
            s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-11*t)
        else:
            d = int(0.10*SR); t = np.arange(d)/SR
            s = rng.normal(0, 1, d) * np.exp(-52*t)
            s = np.convolve(s, np.ones(6)/6, mode='same')
            s += 0.5*np.sin(2*np.pi*430*t)*np.exp(-40*t)
        d = min(d, n - i)
        out[i:i+d] += s[:d] * vel
    return out * 0.30

# ---- melody: swara, beats, glide-in? -------------------------------------
MEL = [
    # opening call
    ("S", 1.5, None), ("R", .5, None), ("G", 1.0, "R"), ("P", 1.0, None),
    ("G", 1.0, None), ("R", 1.0, None), ("S", 2.0, "R"),
    # ascending phrase
    ("S", .5, None), ("R", .5, None), ("G", .5, None), ("P", .5, None),
    ("D", 1.0, "P"), ("P", 1.0, None), ("G", 2.0, "P"),
    # upper register
    ("P", 1.0, None), ("D", 1.0, None), ("S'", 2.0, "D"),
    ("S'", .5, None), ("D", .5, None), ("P", 1.0, None), ("G", 2.0, "P"),
    # resolution
    ("P", 1.0, None), ("G", 1.0, None), ("R", 1.0, None), ("S", 3.0, "R"),
    ("D,", 1.0, None), ("S", 3.0, "D,"),
]

total_beats = sum(m[1] for m in MEL) + 2
DUR = total_beats * BEAT

lead = np.zeros(int(DUR*SR) + SR)
pos = 1.0 * BEAT           # small pickup of drone before the lead enters
for sw, beats, gl in MEL:
    d = beats * BEAT
    f = SA * RATIOS[sw] * 2          # lead sits an octave above the tonic
    gf = SA * RATIOS[gl] * 2 if gl else None
    seg = nadaswaram(f, d*0.97, amp=0.5, gliss_from=gf)
    i = int(pos*SR)
    lead[i:i+len(seg)] += seg
    pos += d

drone = tanpura(DUR + 1.0)

# adi tala-ish 8-beat cycle
pat = []
b = 2.0
while b < total_beats - 1:
    for off, kind, vel in [(0,'low',1.0), (1.5,'tap',.55), (2,'tap',.7), (3,'low',.8),
                           (4,'tap',.6), (5,'low',.9), (6,'tap',.5), (6.5,'tap',.45), (7,'tap',.65)]:
        pat.append((b+off, kind, vel))
    b += 8
perc = thavil(DUR + 1.0, pat)

n = min(len(lead), len(drone), len(perc))
mix = lead[:n] + drone[:n] + perc[:n]

# gentle fade so the loop point is seamless
fade = int(1.2*SR)
mix[:fade] *= np.linspace(0, 1, fade)
mix[-fade:] *= np.linspace(1, 0, fade)

# soft limiter
mix = np.tanh(mix * 1.15)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.88

os.makedirs("assets", exist_ok=True)
raw = (mix * 32767).astype(np.int16)
import wave
with wave.open("assets/_tmp.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(raw.tobytes())

subprocess.run(["ffmpeg","-y","-loglevel","error","-i","assets/_tmp.wav",
                "-codec:a","libmp3lame","-b:a","80k","-ar","44100","-ac","1",
                "assets/mangala-vadyam.mp3"], check=True)
os.remove("assets/_tmp.wav")
print("duration %.1fs" % (n/SR), "size", os.path.getsize("assets/mangala-vadyam.mp3"), "bytes")
