# Decide Once: Build Your Identity Kit

Emir Cabalak, General AI Fluency track, Week 3
Assignment code CUSTOM-MQX00WJN-0CE9EDFA

Everything on one page. Files in this folder: `logo.svg`, `favicon.svg`, `tokens.css`.

## Type

Two fonts, both free, both on Google Fonts.

**Headings: Space Grotesk.** Weights 500 and 600 only. It has slightly odd letterforms without
being a novelty face, which reads as considered rather than defaulted. Space Grotesk at 600
with tight tracking is the whole visual identity, so it has to carry.

**Body: IBM Plex Sans.** Weights 400 and 600. It was drawn for technical documentation, so it
survives a page full of numbers and does not fight the headings.

Fallback stack for both, so nothing shifts if the webfont fails:
`"Segoe UI", Helvetica, Arial, sans-serif`.

**What I cut.** I wanted a third face, IBM Plex Mono, for metric tables. It would look right and
it is the wrong call: three fonts is a pile, and the tables can use `font-variant-numeric:
tabular-nums` on IBM Plex Sans to get aligned digits without another download. That covers the
actual reason I wanted mono.

## Palette

Four colors. Hex codes are the real ones, taken from `tokens.css`.

| Role | Hex | Where it goes |
|---|---|---|
| Paper | `#FAF9F7` | page background, warm off-white rather than pure white |
| Ink | `#16181D` | all body text and headings |
| Main | `#2E4B6B` | logo block, rules, table headers, the site's one structural color |
| Accent | `#C2410C` | the single call to action, and nothing else |

Contrast on paper: ink 17:1, main 8.8:1, accent 4.9:1. All pass WCAG AA for normal body text,
which matters because the accent is a link and links get read.

The accent has one job. If it starts appearing on subheads and bullets it stops meaning "click
this" and the page loses its only pointer. One accent, one use.

Dark mode is in `tokens.css` as a `prefers-color-scheme` block: paper `#14161A`, ink `#E9E7E3`,
main `#8FB2D6`, accent `#F0834D`. Same four roles, lifted so they survive on a dark background.

## Logo and favicon

`logo.svg` is a rounded square in main color with a lowercase `ec` in paper color, then my name
in Space Grotesk beside it and the line "numbers that hold up" underneath in body font.

`favicon.svg` is the square alone. Nothing else survives at 16 pixels, and a monogram that has
to be squinted at is a monogram that failed.

Both are SVG, both use the same fallback stack, so they render even where the webfont has not
loaded. Lowercase rather than caps because `EC` in a box looks like a corporate badge and this
is a person's site.

## Style note

The two lines that now sit in my Claude Project so every build inherits them:

> Fonts: Space Grotesk for headings, IBM Plex Sans for body. Colors: paper `#FAF9F7`, ink
> `#16181D`, main `#2E4B6B`, accent `#C2410C`, dark mode variants in `tokens.css`. Accent is
> reserved for the single call to action.
>
> Mood: a lab notebook, not a brochure. Plain, quiet, and slightly technical, so the numbers
> and the writing are the loudest thing on the page. Generous white space, one column, no
> gradients, no shadows, no animation.

## Why this mood

My claim is that my numbers hold up when someone checks them. A page with gradients and motion
undercuts that before a reader hits a sentence, because it is visibly trying to impress and my
whole argument is that I am not. Quiet is not a taste preference here, it is the same claim in
another medium.
