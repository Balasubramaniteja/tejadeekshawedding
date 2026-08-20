# Teja weds Deeksha — Wedding Invitation

A single-page, fully static wedding invitation site.

**Live site (after Pages is enabled):** https://balasubramaniteja.github.io/tejadeekshawedding/

## Events

| Event | Date | Time | Venue |
|---|---|---|---|
| Haldi (పసుపు) | Tue, 20 October 2026 | 9:00 AM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Nalugu (నలుగు) | Tue, 20 October 2026 | 4:00 PM onwards | 4740 West 61st Street, Mission, KS 66205 |
| Muhurtham (ముహూర్తం) | Wed, 21 October 2026 | 11:30 AM | 6330 Lackman Rd, Shawnee, KS 66217 |

## Files

- `index.html` — the entire site (HTML + CSS + JS + SVG illustrations inlined). No build step, no dependencies.
- `.nojekyll` — tells GitHub Pages to serve the files as-is.

## Editing

Everything text-based is in the HTML itself. The few values used by scripts live in
one `const W = { … }` block near the bottom of `index.html`:

- `phone` — used by the RSVP button (WhatsApp) and the footer `tel:` link
- `countdownTo` — the Muhurtham timestamp the countdown counts down to
- `events` — the three calendar entries produced by the "Add to calendar" button

To change a name, date or address, edit the visible text directly in `index.html`
(search for the word you want to replace).

## RSVP

The RSVP form does not need a server. On submit it composes the reply and opens
WhatsApp to the number in `W.phone`, with an SMS fallback link. To switch to a
Google Form instead, create the form and replace the `rsvpForm` submit handler
with a `<iframe src="…">` embed.

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
