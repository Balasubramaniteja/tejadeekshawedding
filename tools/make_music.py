"""
Mangala Vadyam — original nadaswaram + thavil wedding instrumental.

Written from scratch (numpy synthesis, no samples, no copyrighted material) in the
South Indian 'mangala vadyam' idiom traditionally played at a Telugu wedding:
a nadaswaram lead over a tanpura/ottu drone, joined by thavil percussion.

Raga Mohanam (S R2 G3 P D2), Adi tala. The Carnatic character comes mostly from
the gamakas — kampita (oscillation around a note) and jaru (slides between them) —
so those are modelled explicitly rather than playing flat tones.

    python3 make_music.py    ->  assets/mangala-vadyam.mp3
"""
import numpy as np, subprocess, os, wave
from scipy.signal import butter, sosfilt, lfilter

SR   = 44100
BPM  = 64
BEAT = 60.0 / BPM
SA   = 146.83                      # D3 tonic
RNG  = np.random.default_rng(20261021)

# Mohanam
R = {'S': 1.0, 'R': 9/8, 'G': 5/4, 'P': 3/2, 'D': 5/3,
     "S'": 2.0, "R'": 9/4, "G'": 5/2, 'D.': 5/6, 'P.': 3/4, 'G.': 5/8}
ORDER = ['G.', 'P.', 'D.', 'S', 'R', 'G', 'P', 'D', "S'", "R'", "G'"]


# ----------------------------------------------------------------- helpers
def adsr(n, a=.05, d=.12, s=.74, r=.24):
    a_n, d_n, r_n = (min(int(x*SR), n//4) for x in (a, d, r))
    s_n = max(1, n - a_n - d_n - r_n)
    return np.concatenate([np.linspace(0, 1, a_n, endpoint=False),
                           np.linspace(1, s, d_n, endpoint=False),
                           np.full(s_n, s),
                           np.linspace(s, 0, r_n)])[:n]


def resonator(x, f0, q=4.0):
    """Cheap formant peak — gives the reed its nasal bite."""
    w = f0 / (SR / 2)
    sos = butter(2, [max(w*0.72, 1e-4), min(w*1.38, .99)], btype='band', output='sos')
    return sosfilt(sos, x)


def pitch_curve(n, freq, prev=None, gamaka='kampita', depth=1.0):
    """
    Returns a per-sample frequency array.
      jaru     — slide in from the previous swara
      kampita  — oscillate towards the neighbouring swara, the core Carnatic ornament
    """
    t = np.arange(n) / SR
    f = np.full(n, float(freq))

    if prev is not None:                       # jaru: glide in
        g = min(int(0.085 * SR), n // 3)
        if g > 1:
            f[:g] = np.geomspace(prev, freq, g)

    if gamaka == 'kampita' and n > int(0.18 * SR):
        rate = 5.2
        # oscillation grows in, then settles — never a flat machine wobble
        grow = np.clip((t - 0.10) / 0.30, 0, 1) * np.clip((t[-1] - t) / 0.25 + .35, 0, 1)
        cents = 62 * depth * grow * np.sin(2 * np.pi * rate * t)
        f *= 2 ** (cents / 1200)
    elif gamaka == 'plain':
        f *= 2 ** (5 * np.sin(2*np.pi*5.6*t) * np.clip((t-.15)/.3, 0, 1) / 1200)
    return f


def nadaswaram(freq, dur, amp=.5, prev=None, gamaka='kampita', depth=1.0, bright=1.0):
    n = int(dur * SR)
    if n < 64:
        return np.zeros(max(n, 1))
    f = pitch_curve(n, freq, prev, gamaka, depth)
    phase = 2 * np.pi * np.cumsum(f) / SR
    harm = np.array([1.0, .66, .82, .60, .52, .34, .26, .18, .12, .08, .05])
    y = sum(a * np.sin(k * phase) for k, a in enumerate(harm, 1)) / harm.sum()
    y = .70 * y + .55 * resonator(y, 1450 * bright, q=5)     # reed formant
    y += .010 * RNG.normal(0, 1, n) * np.linspace(1, .25, n)  # breath
    return y * adsr(n) * amp


def tanpura(dur, amp=.15):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for f, a in [(SA/2, 1.0), (SA, .70), (SA*1.5, .48), (SA*2, .26), (SA*3, .13), (SA*4, .06)]:
        y += a * np.sin(2*np.pi*f*t * (1 + .0020*np.sin(2*np.pi*.19*t + f)))
        y += a*.26 * np.sin(2*np.pi*f*1.0012*t)
    # slow swell so the drone breathes
    return y / 3.6 * amp * (1 + .10*np.sin(2*np.pi*.07*t))


def stroke(kind, vel):
    if kind == 'boom':                                    # left hand, pitched membrane
        d = int(.34*SR); t = np.arange(d)/SR
        f = 96*np.exp(-8.5*t) + 54
        s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-9.5*t)
        s += .22*np.sin(2*np.pi*np.cumsum(f*2)/SR) * np.exp(-16*t)
    elif kind == 'ta':                                    # right hand, sharp
        d = int(.11*SR); t = np.arange(d)/SR
        s = RNG.normal(0, 1, d) * np.exp(-55*t)
        b, a = butter(2, [1800/(SR/2), 7000/(SR/2)], btype='band')
        s = lfilter(b, a, s)
        s += .45*np.sin(2*np.pi*520*t)*np.exp(-42*t)
    elif kind == 'ki':                                    # lighter tap
        d = int(.07*SR); t = np.arange(d)/SR
        s = RNG.normal(0, 1, d) * np.exp(-85*t)
        b, a = butter(2, [2600/(SR/2), 9000/(SR/2)], btype='band')
        s = lfilter(b, a, s) * .8
    else:                                                 # temple bell accent
        d = int(1.7*SR); t = np.arange(d)/SR
        s = sum(a*np.sin(2*np.pi*f*t)*np.exp(-dk*t) for f, a, dk in
                [(1046, 1, 1.6), (1570, .55, 2.2), (2093, .35, 2.8), (3140, .18, 4.0)])
    return s * vel


def render_perc(total, events):
    out = np.zeros(int(total*SR) + SR*2)
    for beat, kind, vel in events:
        i = int(beat * BEAT * SR)
        s = stroke(kind, vel)
        out[i:i+len(s)] += s
    return out


# ----------------------------------------------------------------- the piece
# (swara, beats, gamaka)  — 'k' kampita, 'p' plain, 'f' flat/held
ALAPANA = [                                    # free opening over the drone alone
    ('S', 2.0, 'k'), ('R', 1.0, 'k'), ('G', 2.5, 'k'), ('R', 1.0, 'p'), ('S', 3.0, 'k'),
    ('D.', 1.5, 'k'), ('S', 1.0, 'p'), ('R', 1.0, 'p'), ('G', 3.0, 'k'),
]
BODY = [                                       # the rhythmic mangala melody
    ('P', 1.5, 'k'), ('G', .5, 'p'), ('R', 1.0, 'p'), ('S', 2.0, 'k'),
    ('S', .5, 'p'), ('R', .5, 'p'), ('G', .5, 'p'), ('P', .5, 'p'),
    ('D', 1.0, 'k'), ('P', 1.0, 'k'), ('G', 2.0, 'k'),

    ('P', 1.0, 'p'), ('D', 1.0, 'p'), ("S'", 2.5, 'k'), ("R'", 1.5, 'k'),
    ("S'", 1.0, 'p'), ('D', 1.0, 'k'), ('P', 2.0, 'k'),

    ('D', .5, 'p'), ('P', .5, 'p'), ('G', .5, 'p'), ('R', .5, 'p'),
    ('S', 1.0, 'k'), ('R', 1.0, 'p'), ('G', 1.0, 'p'), ('P', 1.0, 'k'),
    ('G', 1.0, 'p'), ('R', 1.0, 'p'), ('S', 3.0, 'k'),
]
CODA = [                                       # mangalam — settle on Sa
    ('G', 1.0, 'p'), ('R', 1.0, 'p'), ('S', 1.0, 'k'),
    ('D.', 1.5, 'k'), ('S', 4.5, 'k'),
]

SEQ = [('alapana', ALAPANA), ('body', BODY), ('coda', CODA)]

total_beats = 2 + sum(b for _, sec in SEQ for _, b, _ in sec) + 3
DUR = total_beats * BEAT
lead = np.zeros(int(DUR*SR) + SR*3)

pos = 2.0 * BEAT              # drone alone before the reed enters
body_start = None
prev_f = None
for name, sec in SEQ:
    if name == 'body':
        body_start = pos / BEAT
    for sw, beats, gk in sec:
        d = beats * BEAT
        f = SA * R[sw] * 2                                  # lead an octave up
        gamaka = {'k': 'kampita', 'p': 'plain', 'f': 'none'}[gk]
        # kampita leans towards the next scale degree, as a nadaswaram player would
        seg = nadaswaram(f, d*0.985, amp=.48, prev=prev_f, gamaka=gamaka,
                         depth=1.0 if beats >= 1.5 else .5)
        i = int(pos*SR)
        lead[i:i+len(seg)] += seg
        prev_f = f
        pos += d
body_end = pos / BEAT

# --- thavil: adi tala, 8 beats, entering with the body -------------------
CYCLE = [(0, 'boom', 1.00), (0.5, 'ki', .40), (1, 'ta', .70), (1.5, 'ki', .45),
         (2, 'ta', .82), (3, 'boom', .85), (3.5, 'ki', .40),
         (4, 'ta', .68), (4.5, 'ki', .42), (5, 'boom', .92),
         (6, 'ta', .60), (6.5, 'ki', .48), (7, 'ta', .72), (7.5, 'ki', .50)]
FILL  = [(6, 'ta', .75), (6.33, 'ta', .60), (6.66, 'ta', .68),
         (7, 'ta', .80), (7.33, 'ki', .55), (7.66, 'ta', .70)]

events, b, cyc = [], body_start, 0
while b < body_end - 1:
    pattern = FILL if (cyc % 4 == 3) else []
    for off, k, v in CYCLE:
        if not any(abs(off - fo) < .2 for fo, _, _ in pattern):
            events.append((b + off, k, v))
    for off, k, v in pattern:
        events.append((b + off, k, v))
    b += 8; cyc += 1

events.append((2.0, 'bell', .30))                    # bell at the opening
events.append((body_start, 'bell', .26))             # and as the tala enters
events.append((body_end + 0.5, 'bell', .34))         # and on the mangalam

perc  = render_perc(total_beats, events)
drone = tanpura(DUR + 2.0)

n = min(len(lead), len(drone), len(perc))
mix = lead[:n] + drone[:n] + 0.34 * perc[:n]

# light room reverb
ir = np.zeros(int(.34*SR))
for tap, g in [(.021, .34), (.037, .27), (.058, .21), (.083, .16), (.121, .11), (.178, .07)]:
    ir[int(tap*SR)] = g
ir[0] = 1.0
mix = np.convolve(mix, ir)[:n]

fade = int(1.4*SR)
mix[:fade] *= np.linspace(0, 1, fade)
mix[-fade:] *= np.linspace(1, 0, fade)

mix = np.tanh(mix * 1.1)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= .90

os.makedirs("assets", exist_ok=True)
with wave.open("assets/_tmp.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "assets/_tmp.wav",
                "-codec:a", "libmp3lame", "-b:a", "88k", "-ar", "44100", "-ac", "1",
                "assets/mangala-vadyam.mp3"], check=True)
os.remove("assets/_tmp.wav")
print("duration %.1fs  size %d bytes" % (n/SR, os.path.getsize("assets/mangala-vadyam.mp3")))
