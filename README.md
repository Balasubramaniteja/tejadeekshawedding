# Teja weds Deeksha — Wedding Invitation

A single-page, fully static wedding invitation site.

**Live site (after Pages is enabled):** https://balasubramaniteja.github.io/tejadeekshawedding/

## Events

| Event | Date | Time | Venue |
|---|---|---|---|
| Haldi (పసుపు) | Tue, 20 October 2026 | 9:00 AM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Nalugu (నలుగు) | Tue, 20 October 2026 | 4:00 PM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Welcome Dinner (విందు) | Tue, 20 October 2026 | 7:00 PM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Pellikoduku & Pellikuthuru (పెళ్ళికొడుకు & పెళ్ళికూతురు) | Wed, 21 October 2026 | 9:00 AM onwards | 6330 Lackman Rd, Shawnee, KS 66217 |
| Muhurtham (ముహూర్తం) | Wed, 21 October 2026 | 11:30 AM | 6330 Lackman Rd, Shawnee, KS 66217 |

Each event card carries a supplied illustration. Behind each one an SVG scene is also drawn inline
in `index.html` and shown automatically if the image file is ever missing, so a card can never end
up blank.

## Files

- `index.html` — the entire site (HTML + CSS + JS + SVG illustrations inlined). No build step, no dependencies.
- `assets/wedding-music.mp3` — background music, supplied by the couple. Re-encoded from the
  original 256 kbps stereo (5.6 MB) down to 96 kbps (2.0 MB) and set to `preload="none"`, so the
  file is only fetched when a guest actually taps play. 2:54 long; it fades out at the end and
  begins quietly, so the loop joins without a click.
  Replace this file to change the music — the filename is referenced once in `index.html`.
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

## How they met

After the opening tap, three scenes play before the invitation appears (about 15 seconds):

1. **The flight** — a plane arcs from California to Shawnee, Kansas across a vintage map, drawing a
   dotted gold trail behind it while the camera pans across.
2. **First sight** — the map dissolves into Fat Bee Coffee, sunlight streaking through the windows.
   The clock rolls up and settles on **2:45:36**, the background softens, and they see each other.
3. **The first selfie** — the view becomes a phone viewfinder, the shutter taps, and a white flash
   hands over to the invitation.

Every animation is held until the guest taps open (the `.playing` class starts the whole timeline),
so it can never run out of sync with the music. There is a **Skip** button throughout, and the whole
sequence is bypassed for anyone whose device asks for reduced motion. It plays once per page load;
reloading the page plays it again.

Timings live in one place — the `HOW THEY MET` CSS block — and the total length is the `RUN` constant
in the matching script block. Both must be changed together.

## Thalambralu

Turmeric-stained rice drifts down the page, as the couple pour over each other at the muhurtham.
It is a fixed layer of small CSS-animated grains — 32 on desktop, 18 on a phone — sitting above the
content but with `pointer-events:none`, so it never intercepts a tap. Grains start mid-fall
(negative animation delays) so the page never looks like it is waiting to begin, and the whole
layer is switched off for visitors who ask for reduced motion.

To change the density or colours, see the `THALAMBRALU` block near the bottom of `index.html`.

## Event images

Each event card shows a supplied image, and falls back to its drawn SVG scene if the file is ever
missing. The five in use are the couple's own illustrations, resized to 880 px wide and saved as
progressive JPEG (~135 KB each, 675 KB total). File names:

```
assets/events/haldi.jpg
assets/events/nalugu.jpg
assets/events/welcome-dinner.jpg
assets/events/pellikoduku-pellikuthuru.jpg
assets/events/muhurtham.jpg
```

To replace one, drop in a file with the same name. Roughly **880 × 455 px** (about 1.94:1) fits the
card exactly; anything wider or taller is cropped from the centre. Keep each under ~200 KB so the
page stays quick on a phone. Images load lazily, so they cost nothing until the guest scrolls down.

The haldi and nalugu illustrations arrived on a flat white field, which would have shown as a bright
rectangle against the cream card, so the white was recoloured to the page background.

Only use images you own or are licensed to use — this page is public once deployed. Stock-library
images (Freepik, Shutterstock, Adobe Stock and the like) need a licence that covers use on a public
website, and some free tiers additionally require visible attribution.

The five event illustrations and the background music were supplied by the couple. Everything else
on the page — the toran, the opening-screen mandala, the muggu dividers and the per-event
fallback scenes — is drawn in SVG specifically for this invitation, so there is nothing to licence or
attribute for those.

## Language

All devotional text is Telugu script, as used in a South Indian Telugu wedding —
`శ్రీ గణేశాయ నమః`, `శుభ వివాహం`, the Saptapadi verse, and `శుభమస్తు`.
Event names carry their Telugu equivalents (పసుపు, నలుగు, ముహూర్తం).

## Editing

Everything text-based is in the HTML itself. The few values used by scripts live in
one `const W = { … }` block near the bottom of `index.html`:

- `phone` — used by the RSVP button (WhatsApp) and the footer `tel:` link
- `countdownTo` — the Muhurtham timestamp the countdown counts down to
- `events` — the five calendar entries produced by the "Add to calendar" button

To change a name, date or address, edit the visible text directly in `index.html`
(search for the word you want to replace).

## RSVP — where replies go

The styled form on the page posts straight into a **Google Form**, so every reply lands in a Google
Sheet you own and Google emails you on each submission. No server, no backend, works on any host.
Until it is configured the form falls back to opening WhatsApp with the reply pre-written.

### 1. Create the form

New Google Form with these five questions, **in this order**:

| # | Question | Type | Options |
|---|---|---|---|
| 1 | Your name | Short answer | — |
| 2 | Will you join us? | Multiple choice | `Joyfully accepts` · `Regretfully declines` |
| 3 | Number of guests (including you) | Short answer | — |
| 4 | Which events will you attend? | Checkboxes | `Haldi` · `Nalugu` · `Welcome Dinner` · `Pellikoduku & Pellikuthuru` · `Muhurtham` |
| 5 | A wish for the couple | Paragraph | — |

The option text must match exactly — Google silently drops values it does not recognise.

### 2. Turn on the sheet and the alerts

**Responses → Link to Sheets** creates the spreadsheet.
**Responses → ⋮ → Get email notifications for new responses** emails you on every RSVP.

### 3. Find the field ids

Open the form → **⋮ → Get pre-filled link** → type a dummy answer into every question → **Get link**.
The copied URL contains one `entry.NNNNNNN=` per question, in the same order as above.

### 4. Fill in the config

In `index.html`, in the `const W = { … }` block:

```js
googleForm: {
  action:    "https://docs.google.com/forms/d/e/<FORM_ID>/formResponse",
  name:      "entry.1111111111",
  attending: "entry.2222222222",
  guests:    "entry.3333333333",
  events:    "entry.4444444444",
  message:   "entry.5555555555"
}
```

`action` is your form's normal link with the trailing `/viewform` replaced by `/formResponse`.

The browser posts into a hidden iframe, so the guest never leaves the invitation and never sees a
Google page. Google returns a cross-origin response the page cannot read, which is why the site
shows its own confirmation message rather than waiting for one.

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
