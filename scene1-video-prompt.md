# Scene 1 — "Where Our Story Began"
### Prompt for a text-to-video model (Sora, Veo, Kling, Runway, Hailuo)

**How to use this:** attach the selfie of Teja and Deeksha as the character reference / "ingredient"
image, then paste the prompt below. Most tools cap a single generation at 8–12 seconds, so this is
split into four shots that cut together cleanly. Generate them separately and join them — asking one
generation to carry the whole 40-second arc is where these models fall apart.

Target: **1920×1080, 24 fps**, cinematic 3D animated feature look.

---

## Global style (paste into every shot)

> Premium Disney/Pixar-inspired 3D animated feature look. Warm cinematic lighting, shallow depth of
> field, soft volumetric golden light, gentle film grain. Romantic, dreamy, intimate — not a tourism
> advert. Use the attached photograph as the facial and appearance reference for both characters:
> preserve their recognisable facial features, skin tones, hairstyles, expressions and body
> proportions. Do not make their faces generic. He wears round glasses, a navy jacket over a dusty
> pink shirt; she has long dark wavy hair and a black jacket.

---

## Shot 1 — the map draws itself (≈8s)

> Deep midnight-blue screen filled with drifting tiny warm golden particles. A delicate glowing
> golden line slowly draws the outline of the state of Kansas, as if a love story is being sketched
> onto a map. The camera pushes slowly toward the outline. Small warm golden lights bloom one by one
> across the landscape inside it. One light near the eastern edge grows brighter than the others.
> No text. Slow push-in, no cuts.

## Shot 2 — arriving in Kansas City (≈8s)

> The single bright golden light blooms and dissolves into a romantic Kansas City evening. Warm
> street lamps, elegant architecture, distant city lights and a hint of the Kansas City skyline,
> softly out of focus. The camera settles at street level. Intimate and cinematic, early evening,
> warm amber key light. No people yet. Continuous move, no cuts.

## Shot 3 — the couple (≈10s)

> [global style] A young Indian couple stand together on a Kansas City street in the evening. The
> woman is slightly closer to camera, the man beside and just behind her, matching the natural
> easy chemistry of the reference photograph. Very subtle life: natural blinking, soft smiles,
> a little hair movement in the breeze, gentle breathing, a small affectionate glance at each
> other. The camera slowly orbits them. Warm golden particles float through the air. A thin
> glowing golden thread appears in the air between them. Shallow depth of field, background lights
> bokeh. One continuous orbiting shot.

## Shot 4 — forward into the mandap (≈10s)

> [global style] The same couple walk forward together, the camera tracking with them. The
> environment flows through moments without hard cuts — city lights, drifting autumn leaves, a warm
> sunset, tiny flashes of memory. A golden thread runs ahead of them along the ground. In the
> distance an elegant Indian wedding mandap appears in silhouette, decorated with marigold flowers,
> jasmine, warm diyas and golden fairy lights. As the camera moves past them toward the mandap,
> their silhouettes shift subtly toward wedding attire — he in traditional Indian groom's dress,
> she in bridal wear — without fully completing the change. The faint golden outline of Kansas
> glows behind the mandap. End on a wide shot, the couple small against the glowing horizon.

---

## Text overlays

Do **not** ask the video model to render these — text generation is where these models are least
reliable, and misspelt names on a wedding invitation are unforgivable. Add them afterwards in any
editor (CapCut, Canva, iMovie, Premiere), or send me the finished clip and I will overlay them in
the browser, where they will always be crisp and correctly spelt.

| When | Text | Style |
|---|---|---|
| End of shot 3 | We met in Kansas… | Elegant serif, warm gold, fades in over 1.5s |
| End of shot 4 | …and in Kansas, our forever begins. | Same, larger |
| Under it | Teja ❤️ Deeksha | Smaller |
| Under that | October 21, 2026 • Kansas City | Smaller still, letter-spaced |

---

## Two practical notes

**Faces drift between shots.** Every generation interprets the reference photo slightly differently.
Generate several takes of shot 3 and pick the one that looks most like them, then use a still frame
from that take as the reference for shot 4 so the two match.

**Keep the file small.** A 40-second 1080p clip is typically 15–30 MB. A full visit to the
invitation is currently 3.5 MB, so a video would be five to ten times the whole rest of the site.
Before it goes on the page I would re-encode it to about 6–8 MB (720p, H.264, ~1.2 Mbps) and set it
to load only after the guest taps open — otherwise it will be slow for relatives on phone data, and
it will consume Netlify credits far faster than everything else combined.
