# Kill your darlings: Curate Your Images

Emir Cabalak, General AI Fluency track, Week 3
Assignment code CUSTOM-MQX033TI-DE712A19

## The list

Every image the site actually needs, against the sitemap. Nine slots, and I killed four ideas
before this list existed.

| # | Slot | Page | What it is | Source |
|---|---|---|---|---|
| 1 | Hero texture | home | scatter split by a dashed wall | generated, in this folder |
| 2 | Portrait | about | photograph of me | real photo, to shoot |
| 3 | Case 1 icon | home card, case page header | the leaking pair | generated, in this folder |
| 4 | Case 2 icon | home card, case page header | the split wall | generated, in this folder |
| 5 | Case 3 icon | home card, case page header | the ladder with one step down | generated, in this folder |
| 6 | Feature verdict table | case 1 | screen capture of the notebook table | real capture, to take |
| 7 | Three-split comparison | case 2 | screen capture of the metrics table | real capture, to take |
| 8 | V3 vs V4 output diff | case 3 | screen capture of the two outputs side by side | real capture, to take |
| 9 | Favicon | every page | the `ec` monogram | vector, already built in the Week 3 identity kit |

Six of the nine are real or vector. The three generated ones are the connective tissue only.
Nothing that represents my work is generated, and nothing that represents me is generated.

## The generated set

Files: `hero-texture.svg`, `icon-leak.svg`, `icon-split.svg`, `icon-ladder.svg`.

They are a set on purpose. All four share the same rules: paper background `#FAF9F7`, strokes
in main `#2E4B6B` at two pixels, one element in accent `#C2410C` and never more than one, no
fills except the dots, no gradients, no shadows, square line caps. Every icon puts the accent
on the thing the case is actually about: the leak, the held-out side, the step that went down.

The hero is the same rule at a larger scale. Points rising to the left of a dashed wall, points
in accent to the right of it, and two small labels. Someone who knows what a train and test
split looks like will recognize it in about a second. Someone who does not still sees a quiet
chart and reads the words.

**How I held the style steady.** I did not get consistency by asking nicely. I wrote the rules
above into the prompt as a fixed block, generated one icon, then reused that finished icon as
the reference for the next two and asked for changes only to the shapes. Attempt one, where I
described the mood in words and generated all three at once, gave me three icons with three
different stroke weights and two different backgrounds. Describing a mood does not hold a
style. Fixing the numbers does.

**Why vector rather than raster.** These are diagrams, not pictures. As SVG they are a few
hundred bytes each, they stay sharp on a phone, and I can retheme them by changing the hex
codes in one place when the identity kit changes. A generated PNG of the same idea would be
150KB and frozen.

## Where I chose a real capture over AI, and why

**Case screenshots, slots 6, 7 and 8.** These are the proof. A generated image of a table of
numbers is a picture of numbers I did not compute, which on a site whose entire claim is that
my numbers hold up would be the single most self-defeating thing on the page. If a reader
zooms in on my verdict table, every cell has to be a cell that a real run produced. That is not
a style preference, it is the argument.

They also have to be legible, which is where most portfolio screenshots die. My rules for each
one: crop to the table and nothing else, no browser chrome, no visible file paths or client
names, light theme so it sits on paper without a dark rectangle punched into the page, and at
least 2x pixel density so the digits survive a retina screen.

**Portrait, slot 2.** A real photo. An AI portrait on a page arguing for honest evaluation is a
joke that writes itself, and people can tell. Plain background, no suit, the same warm-neutral
tone as the paper color so it does not fight the page.

## What I rejected

**A generated "data scientist at work" hero.** I made one: a person at a desk, three monitors,
blue code glow, the whole stock-photo grammar. It looked competent and it was the easiest thing
on the page to delete. It says nothing that my one-line claim does not already say better, and
it makes a specific claim about a workspace that is not mine. It is decoration where the hero
slot is the most valuable space on the site.

**A generated abstract neural network mesh.** Glowing nodes and connecting lines. I rejected it
for a more useful reason than taste: I do not build neural networks. The work in these cases is
gradient boosting and cross-validation design. Putting a neural mesh at the top of the page
promises something the cases do not deliver, and a reader who came for that leaves disappointed
by the second paragraph. An image that misdescribes the work is worse than no image.

**A generated portrait.** Killed on sight, for the reason above.

**A logo with a shield or a checkmark.** I tried it because "numbers you can trust" pushes you
toward trust badges. It looked like a security product. Claiming trustworthiness with an icon
is the opposite of demonstrating it with a case study, so the monogram stayed plain.

## Still to capture

These are the two slots I cannot fill from a text editor, so they are on my list rather than
in this folder.

- The portrait. One session, plain wall, daylight, single frame chosen.
- The three case screenshots. All three come from notebooks that already exist, so this is a
  crop-and-export job rather than new work. Public-safety pass first: no client names, no
  domains, no private queries, no file paths in the frame.

Until they land, the case pages use the icon plus the numbers as text, which is honest and also
faster to read. The screenshots are corroboration, not the content.
