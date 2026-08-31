# Teja weds Deeksha — Wedding Invitation

A single-page, fully static wedding invitation site.

**Live site (after Pages is enabled):** https://balasubramaniteja.github.io/tejadeekshawedding/

## Events

| Event | Date | Time | Venue |
|---|---|---|---|
| Haldi | Tue, 20 October 2026 | 9:00 AM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Nalugu | Tue, 20 October 2026 | no time published; followed by lunch | 4740 West 61st Street, Mission, KS 66205 |
| Pellikuthuru | Tue, 20 October 2026 | evening; no time published | 4740 West 61st Street, Mission, KS 66205 |
| Muhurtham | Wed, 21 October 2026 | From 9:00 AM; Muhurtham 10:00–11:30 AM, then lunch | 6330 Lackman Rd, Shawnee, KS 66217 |

Nalugu and Pellikuthuru deliberately show **no clock time** — only the date and, for Nalugu, that
lunch follows. Because of that they go into the downloaded calendar file as **all-day entries**
(`DTSTART;VALUE=DATE:`), not as timed ones. That is set by `allDay:true` on those two entries in the
`W.events` config. If you later decide on times, replace `allDay:true` with real `start`/`end`
stamps in `YYYYMMDDTHHMMSS` form and put the time back on the card, so the page and the calendar
never disagree.

Event cards are text only — no photographs and no illustrations. The Muhurtham card spans the full
width of the grid and carries the running order for the day. There is no countdown timer.

## Directions

Every event card carries its own **Get directions** button, and each venue card has one too — six in
all, pointing at the two addresses. They use the Google Maps *directions* endpoint, not the search
one:

```
https://www.google.com/maps/dir/?api=1&destination=<url-encoded address>
```

The difference matters. `search/?api=1&query=` only drops a pin on the place; `dir/?api=1&destination=`
opens turn-by-turn navigation **from wherever the guest is standing**, which is what someone tapping
it on the day actually wants. On a phone the link hands off to the Google Maps app if it is
installed and falls back to the browser if not; it opens in a new tab, so nobody loses their place
in the invitation.

If an address ever changes, update it in **three** places for that venue — the event card text, the
card's `.dir` link, and the venue card's button — and re-encode it (spaces `%20`, commas `%2C`).

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
- `assets/fonts/*.woff2` — self-hosted webfonts (Marcellus + Cormorant Garamond), so the page
  renders identically without reaching Google Fonts.
- `.nojekyll` — tells GitHub Pages to serve the files as-is.

## Opening screen

The invitation opens behind a single centred play button — no caption, no second link. Phones and
desktop browsers both refuse to start audio without a real tap, so the button doubles as that tap:
it opens the invitation and starts the music together.

There is no longer an "open without music" path, so a guest who does not want sound mutes it with
the toggle that sits in the bottom-right corner once the page is open. That toggle is the only way
to silence it, so leave it in place.

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
never run out of sync with the music. There is **no Skip button** — the sequence closes itself after
`RUN` milliseconds — and it is bypassed entirely for anyone whose device asks for reduced motion.
Since a guest cannot dismiss it early, keep `RUN` short; much beyond the current 6.6 s and people
will think the page has stalled.

Timings live in the `HOW THEY MET` CSS block; the total length is the `RUN` constant in the matching
script block. Both must be changed together.

## Thalambralu

Turmeric-stained rice drifts down the page, as the couple pour over each other at the muhurtham.
It is a fixed layer of small CSS-animated grains — 32 on desktop, 18 on a phone — sitting above the
content but with `pointer-events:none`, so it never intercepts a tap. Grains start mid-fall
(negative animation delays) so the page never looks like it is waiting to begin, and the whole
layer is switched off for visitors who ask for reduced motion.

To change the density or colours, see the `THALAMBRALU` block near the bottom of `index.html`.

## Language

The page is **English throughout**. Sanskrit and Telugu terms that have no natural English
equivalent — *Shubha Vivaham*, *Sri Ganeshaya Namah*, the Saptapadi line, *Shubhamastu* — are
written in Latin transliteration rather than Telugu script, so every guest can read them and the
page needs no Indic webfont.

There is deliberately **no Telugu script anywhere**. If you ever add some back, you must also
restore the `Noto Serif Telugu` `@font-face` rules and the two `assets/fonts/telugu-*.woff2` files —
without a real Telugu font the browser falls back to a font that shapes conjuncts wrongly, so
something like `శ్రీ` renders visibly broken.

## Editing

Everything text-based is in the HTML itself. The few values used by scripts live in
one `const W = { … }` block near the bottom of `index.html`:

- `phone` — the WhatsApp number the RSVP form falls back to until the Google Form is configured.
  It is not shown anywhere on the page.
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
