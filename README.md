# Teja weds Deeksha — Wedding Invitation

A single-page, fully static wedding invitation site.

**Live site (after Pages is enabled):** https://balasubramaniteja.github.io/tejadeekshawedding/

## Events

| Event | Date | Time | Venue |
|---|---|---|---|
| Haldi | Tue, 20 October 2026 | 9:00 AM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Pellikoduku & Pellikuthuru | Tue, 20 October 2026 | 11:00 AM onwards, then lunch | 4740 West 61st Street, Mission, KS 66205 |
| Wedding | Wed, 21 October 2026 | From 9:00 AM; ceremony 10:00–11:30 AM, then lunch | 6330 Lackman Rd, Shawnee, KS 66217 |

Every event now publishes a time, so there are **no all-day calendar entries left** — the `allDay`
flag is still supported by the `.ics` builder if one is ever needed again.

**The muhurtham is labelled "Wedding" everywhere a guest can see it** — the card heading, the running
order, the hero line, the RSVP checkbox and the calendar entry. The word "Muhurtham" survives only as
the RSVP's posted *value* and the `uid`, both of which must not change (see the RSVP section).

**Nalugu was removed** — the couple treat it as the same function as Haldi.

Lunch on 20 October follows **Pellikoduku & Pellikuthuru**, not Haldi.

**There is no separate Venues section.** Both addresses appear on the event cards themselves, each
with its own directions button, so a standalone venue list only repeated them. The muggu divider that
used to close that section now closes the events section instead.

Event cards are text only — no photographs and no illustrations. The Wedding card spans the full
width of the grid and carries the running order for the day. There is no countdown timer. The
"The Wedding" ribbon that used to sit on it was removed once the heading itself read *Wedding*; the
gold border, deeper shadow and full width already mark it out.

The events grid is **not** `auto-fit`: the featured Wedding card spans `1/-1`, which keeps every
track alive, so `auto-fit` would leave an empty third column beside the two day-one cards. It is one
column on a phone and an explicit two above 760px.

## Reminders

**"Add to calendar" is the reminder system.** The downloaded `.ics` carries `VALARM` blocks, so the
guest's own phone fires the notifications — no push permission prompt, no service worker, no backend,
and it keeps working even if this site is never opened again.

| Event | Reminders |
|---|---|
| Haldi | 1 day before · 2 hours before |
| Pellikoduku & Pellikuthuru | 1 day before · 2 hours before |
| Wedding | 1 week before · 1 day before · 2 hours before |

Edit them with the `alarms` array on each entry in `W.events` — ISO-8601 durations before the start
(`-P7D`, `-P1D`, `-PT2H`). The wording each one shows comes from the `ALARM_TEXT` map just above the
calendar handler, keyed by the same string, so a **new duration needs an entry in both places** or the
reminder reads "undefined".

If an event is ever switched back to `allDay:true`, remember its `DTSTART` is midnight — use
`-PT15H` (9:00 AM the previous day) rather than `-P1D`, which would fire at midnight.

**Coverage.** Apple Calendar (iPhone, iPad, Mac) and Outlook honour these reliably. Google Calendar
sometimes discards imported alarms and applies the account's own default notification instead, so a
Google Calendar guest still gets *a* reminder, just possibly not at these exact offsets. That is
worth knowing but not worth engineering around.

### What was deliberately not built

Web push notifications (the kind a website asks permission for) would need a service worker plus a
server holding subscriptions and sending them — impossible on static hosting — and on iPhone they
only work if the guest first adds the site to their home screen. For a wedding audience that is a lot
of machinery for worse reach than a calendar entry.

If you later want **email reminders** instead, the path is: add an optional email field to both the
site form and the Google Form, then attach a time-driven Apps Script to the responses sheet that
mails everyone who accepted. That needs the email field first — the form does not collect one today.

## Directions

Every event card carries its own **Get directions** button — three in all, pointing at the two
addresses. This is the only place the venues appear now. They use the Google Maps *directions* endpoint, not the search
one:

```
https://www.google.com/maps/dir/?api=1&destination=<url-encoded address>
```

The difference matters. `search/?api=1&query=` only drops a pin on the place; `dir/?api=1&destination=`
opens turn-by-turn navigation **from wherever the guest is standing**, which is what someone tapping
it on the day actually wants. On a phone the link hands off to the Google Maps app if it is
installed and falls back to the browser if not; it opens in a new tab, so nobody loses their place
in the invitation.

If an address ever changes, update it in **two** places on each card that uses it — the visible
`.where` text and the `.dir` link — and re-encode it for the link (spaces `%20`, commas `%2C`).

## Files

- `index.html` — the entire site (HTML + CSS + JS + SVG illustrations inlined). No build step, no dependencies.
- `assets/wedding-music.mp3` — background music, supplied by the couple ("Radha Ramanam", *Thipparaa Meesam*).
  Re-encoded from the supplied 136 kbps Opus/WebM (1.0 MB) to 96 kbps MP3 (718 KB) and set to
  `preload="none"`, so the file is only fetched when a guest actually taps play. MP3 rather than the
  original WebM because Safari and older iOS will not decode Opus in a bare `<audio>` element.
  It plays at 40% volume.

  The clip is **1:01 and set to loop**, so a guest reading the page hears the seam roughly once a
  minute. The supplied file ran near full level at both ends (−6.5 dB in, −3.1 dB out), which would
  have clicked audibly every time it wrapped, so a 1.2 s fade-in and a 1.8 s fade-out were baked in —
  both ends now sit below −19 dB and the loop joins softly instead.

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
| 4 | Which events will you attend? | Checkboxes | `Haldi` · `Pellikuthuru` · `Muhurtham` |
| 5 | A wish for the couple | Paragraph | — |

The option text must match exactly — Google silently drops values it does not recognise.

> **Deliberate label/value mismatches — do not "fix" these.** What a guest reads on the site and
> what gets posted to Google are decoupled on purpose, because Google silently discards any value
> its form does not recognise. Three places differ:
>
> | Shown on the site | Posted to Google |
> |---|---|
> | Yes, I can make it. | `Joyfully accepts` |
> | Unfortunately, I can't make it. | `Regretfully declines` |
> | Pellikoduku & Pellikuthuru | `Pellikuthuru` |
> | Wedding | `Muhurtham` |
>
> The wording guests see can be changed freely. The **values must not change** unless the matching
> option is renamed on the live form in the same edit — otherwise that answer disappears from every
> future RSVP with no error shown to anyone. There are HTML comments beside both inputs saying so.

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
