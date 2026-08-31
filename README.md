# Teja weds Deeksha — Wedding Invitation

A single-page, fully static wedding invitation site.

**Live site (after Pages is enabled):** https://balasubramaniteja.github.io/tejadeekshawedding/

## Events

| Event | Date | Time | Venue |
|---|---|---|---|
| Haldi (పసుపు) | Tue, 20 October 2026 | 9:00 AM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Nalugu (నలుగు) | Tue, 20 October 2026 | 4:00 PM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Pellikuthuru (పెళ్ళికూతురు) | Tue, 20 October 2026 | 9:00 AM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Muhurtham (ముహూర్తం) | Wed, 21 October 2026 | 11:30 AM | 6330 Lackman Rd, Shawnee, KS 66217 |

Each event card carries a supplied illustration. Behind each one an SVG scene is also drawn inline
in `index.html` and shown automatically if the image file is ever missing, so a card can never end
up blank.

## Files

- `index.html` — the entire site (HTML + CSS + JS + SVG illustrations inlined). No build step, no dependencies.
- `assets/wedding-music.mp3` — background music, supplied by the couple ("Pushpaka Vimanam").
  Re-encoded from 128 kbps stereo (918 KB) down to 96 kbps (688 KB) and set to `preload="none"`, so
  the file is only fetched when a guest actually taps play. It plays at 40% volume.

  The clip is **0:57 and set to loop**, so a guest reading the page hears the seam roughly once a
  minute. The supplied file ran at full level right up to both ends (−0.6 dB in, −1.5 dB out), which
  would have clicked audibly every time it wrapped, so a 1.2 s fade-in and a 1.8 s fade-out were
  baked in — both ends now sit around −17 dB and the loop joins softly instead.

  To change the music, drop a new file in under the same name. If it is longer than about a minute
  the loop matters less, but **always check the first and last second are quiet** or the loop will
  click:

  ```bash
  ffmpeg -i new.mp3 -af "afade=t=in:st=0:d=1.2,afade=t=out:st=<duration-1.8>:d=1.8" \
         -c:a libmp3lame -b:a 96k assets/wedding-music.mp3
  ```

  The filename is referenced once in `index.html`.
- `assets/img/journey.webm`, `assets/img/journey.mp4`, `assets/img/journey-poster.jpg` — the
  California-to-Kansas map animation, supplied by the couple as a GIF and re-encoded (47 KB / 56 KB).
- `assets/img/deities.png` — the artwork that opens the invitation, supplied by the couple. The flat
  white around the marigold frame was made transparent and the panel inside it recoloured to the page
  cream, so it sits on the background rather than in a white box (880 px wide, 165 KB).
- `assets/fonts/*.woff2` — self-hosted webfonts. Telugu text needs a real Telugu font to shape
  conjuncts correctly, so the fonts ship with the site rather than loading from Google Fonts.
- `assets/events/` — drop your own event photos here (see **Event images** below).
- `.nojekyll` — tells GitHub Pages to serve the files as-is.

## Opening screen

The invitation opens behind a centred play button. Phones and desktop browsers both refuse to
start audio without a real tap, so rather than failing silently the site asks the guest to open
it — with music, or via the "Open without music" link. Once opened, a small toggle sits in the
bottom-right corner for the rest of the visit.

## The journey

After the opening tap, one scene plays before the invitation appears (about 7 seconds): the couple's
own animated map, his avatar travelling the dashed arc from California to Kansas and ending
"Finally together in Kansas."

The journey is a real video, not a GIF. The supplied GIF was 6.8 MB; re-encoded it is **47 KB** as
VP9 WebM and **56 KB** as H.264 MP4 — a hundred times smaller, with no visible loss. Both sources are
listed: Chrome and Firefox take the WebM, Safari and iOS take the MP4. It is `preload="metadata"` and
starts from frame zero each time, so it can never appear mid-animation. If autoplay is ever refused
the poster frame stands in and the story carries on.

The animation is held until the guest taps open (the `.playing` class starts the timeline), so it can
never run out of sync with the music. There is a **Skip** button, and the sequence is bypassed
entirely for anyone whose device asks for reduced motion.

Timings live in the `HOW THEY MET` CSS block; the total length is the `RUN` constant in the matching
script block. Both must be changed together.

## Thalambralu

Turmeric-stained rice drifts down the page, as the couple pour over each other at the muhurtham.
It is a fixed layer of small CSS-animated grains — 32 on desktop, 18 on a phone — sitting above the
content but with `pointer-events:none`, so it never intercepts a tap. Grains start mid-fall
(negative animation delays) so the page never looks like it is waiting to begin, and the whole
layer is switched off for visitors who ask for reduced motion.

To change the density or colours, see the `THALAMBRALU` block near the bottom of `index.html`.

## Event images

Each event card shows a supplied image, and falls back to its drawn SVG scene if the file is ever
missing. The four in use are the couple's own illustrations — the haldi tub, the నలుగు ceremony, the
pellikuthuru ceremony and the muhurtham — resized to 880 px wide and saved as progressive JPEG
(~155 KB each, 625 KB total). File names:

```
assets/events/haldi.jpg
assets/events/nalugu.jpg
assets/events/pellikuthuru.jpg
assets/events/muhurtham.jpg
```

To replace one, drop in a file with the same name. Roughly **880 × 455 px** (about 1.94:1) fits the
card exactly; anything wider or taller is cropped from the centre. Keep each under ~200 KB so the
page stays quick on a phone. Images load lazily, so they cost nothing until the guest scrolls down.

Only use images you own or are licensed to use — this page is public once deployed. Stock-library
images (Freepik, Shutterstock, Adobe Stock and the like) need a licence that covers use on a public
website, and some free tiers additionally require visible attribution.

The event illustrations, the story images, the journey animation and the background music were all
supplied by the couple. Everything else on the page — the toran, the opening-screen mandala, the
muggu dividers, the thalambralu and the per-event fallback scenes — is drawn in SVG specifically for
this invitation, so there is nothing to licence or attribute for those.

## Language

All devotional text is Telugu script, as used in a South Indian Telugu wedding —
`శ్రీ గణేశాయ నమః`, `శుభ వివాహం`, the Saptapadi verse, and `శుభమస్తు`.
Event names carry their Telugu equivalents (పసుపు, నలుగు, ముహూర్తం).

## Editing

Everything text-based is in the HTML itself. The few values used by scripts live in
one `const W = { … }` block near the bottom of `index.html`:

- `phone` — the WhatsApp number the RSVP form falls back to until the Google Form is configured.
  It is not shown anywhere on the page.
- `countdownTo` — the Muhurtham timestamp the countdown counts down to
- `events` — the four calendar entries produced by the "Add to calendar" button

To change a name, date or address, edit the visible text directly in `index.html`
(search for the word you want to replace).

## RSVP — where replies go

The styled form on the page posts straight into a **Google Form**, so every reply lands in a Google
Sheet you own and Google emails you on each submission. No server, no backend, works on any host.
This is **configured and live** — the ids are in section 4 below. If `action` is ever blanked out the
form falls back to opening WhatsApp with the reply pre-written.

### 1. Create the form

New Google Form with these five questions, **in this order**:

| # | Question | Type | Options |
|---|---|---|---|
| 1 | Your name | Short answer | — |
| 2 | Will you join us? | Multiple choice | `Joyfully accepts` · `Regretfully declines` |
| 3 | Number of guests (including you) | Short answer | — |
| 4 | Which events will you attend? | Checkboxes | `Haldi` · `Nalugu` · `Pellikuthuru` · `Muhurtham` |
| 5 | A wish for the couple | Paragraph | — |

The option text must match exactly — Google silently drops values it does not recognise.

### 2. Turn on the sheet and the alerts

**Responses → Link to Sheets** creates the spreadsheet.
**Responses → ⋮ → Get email notifications for new responses** emails you on every RSVP.

### 3. Find the field ids

Open the form → **⋮ → Get pre-filled link** → type a dummy answer into every question → **Get link**.
The copied URL contains one `entry.NNNNNNN=` per question, in the same order as above.

### 4. Fill in the config — **done**

This is already wired up. In `index.html`, in the `const W = { … }` block:

```js
googleForm: {
  action:    "https://docs.google.com/forms/d/e/1FAIpQLSddhxROwwf6gTaP7TP2h-wGorTD5r7ts9ZfE9lPKRvSoks2pg/formResponse",
  name:      "entry.374166117",
  attending: "entry.426617619",
  guests:    "entry.669232451",
  events:    "entry.1665966449",
  message:   "entry.248071712"
}
```

`action` is the form's normal link with the trailing `/viewform` replaced by `/formResponse`.

**If you ever rebuild the form from scratch, these ids change** and must be replaced — a stale id means
that answer silently disappears from the sheet. Re-run the "Get pre-filled link" step to get the new ones.

**Do not make questions required.** The site submits in the background and never sees Google's reply, so
a rejected submission still shows the guest a success message. A guest who declines sends no events at
all, and a required events question would throw that RSVP away with nobody the wiser.

The browser posts into a hidden iframe, so the guest never leaves the invitation and never sees a
Google page. Google returns a cross-origin response the page cannot read, which is why the site
shows its own confirmation message rather than waiting for one.

### What actually gets sent

The event checkboxes are a single Google Forms checkbox question, so each ticked event is posted as a
repeated parameter under the same entry id. A guest who ticks Haldi, Pellikuthuru and Muhurtham sends:

```
entry.<name>      = Ravi Kumar
entry.<attending> = Joyfully accepts
entry.<guests>    = 3
entry.<events>    = Haldi
entry.<events>    = Pellikuthuru
entry.<events>    = Muhurtham
entry.<message>   = So happy for you both!
```

In the spreadsheet that lands as one row, with the events column reading
`Haldi, Pellikuthuru, Muhurtham` — so you can filter or count per event. The option text on the form
must match the site's values exactly, or Google drops the ones it does not recognise.

## Deploying to GitHub Pages

```bash
git clone https://github.com/Balasubramaniteja/tejadeekshawedding.git
cd tejadeekshawedding
# copy index.html, .nojekyll and README.md in here
git add .
git commit -m "Wedding invitation site"
git push origin main
```

Then: **Settings → Pages → Build and deployment → Source: Deploy from a branch →
Branch: `main` / `/ (root)` → Save.** The site is live in about a minute.

### Custom domain (optional)

Buy a domain, add a file named `CNAME` at the repo root containing just the domain
(e.g. `tejadeekshawedding.com`), then point these DNS records at GitHub:

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
CNAME www balasubramaniteja.github.io
```

Finally set the domain under **Settings → Pages → Custom domain** and tick
**Enforce HTTPS**.
