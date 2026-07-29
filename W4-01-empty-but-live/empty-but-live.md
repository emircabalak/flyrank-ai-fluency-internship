# Empty but Live: Ship a Blank Page

Emir Cabalak, General AI Fluency track, Week 4
Assignment code CUSTOM-MQX07T4U-1F9328FE

## What is live

**URL:** `https://emircabalak.github.io/`
**Repo:** `https://github.com/emircabalak/emircabalak.github.io`

The page has my name, the one-line claim from Week 3, a line saying the cases are not there
yet, and my email. That is it, and being nearly empty is the point.

Screenshot of the live URL on my phone is attached with this submission.

## The project

Matches the stack I chose in Three Roads: hand-written HTML and CSS on GitHub Pages, no build
step, no dependencies.

Three files:

```
index.html    32 lines
style.css     the identity kit tokens plus about 50 lines of layout
favicon.svg   the ec monogram from the identity kit
```

No `package.json`, no `node_modules`, nothing to install. The whole site is 4KB before fonts.

The repo is named `emircabalak.github.io` rather than something descriptive, because that exact
name is what makes GitHub serve it at `https://emircabalak.github.io/` instead of
`https://emircabalak.github.io/some-repo-name/`. The URL is going on a CV, so the path matters.
My assignment deliverables live in a separate repo, `flyrank-ai-fluency-internship`, because
they belong to the internship and this site does not.

The near-blank page already carries the identity kit rather than default browser styling,
because wiring the fonts and the four colors now is the part that would otherwise get put off,
and it means week 5 is genuinely just writing.

It also already has the things that are annoying to retrofit: a viewport meta tag, a
description, a `prefers-color-scheme` dark variant, a visible focus outline on the one link,
and `tabular-nums` so the numbers in the case tables line up when they arrive.

## How it got there

```bash
git init
git add .
git commit -m "Add name, claim and identity kit styling"
git branch -M main
git remote add origin https://github.com/emircabalak/emircabalak.github.io.git
git push -u origin main
```

Then in the repo, Settings, Pages, source set to "Deploy from a branch", branch `main`, folder
`/ (root)`. First build took about a minute.

## Confirming it is really live

Laptop is not proof. A page can render perfectly from a local file and be completely broken on
the internet, and the two failures I was actually worried about only show up on a second
device.

So I opened the URL on my phone, on mobile data with wifi turned off, which rules out anything
being served from my own machine or cached by my laptop's browser.

What I checked while I was there, since I had the device in my hand:

- The page loads at all, which is the whole assignment.
- HTTPS, with the padlock. GitHub Pages does this by default and I confirmed rather than
  assumed.
- The claim wraps onto three lines instead of overflowing sideways. This is the one thing that
  was actually wrong on the first try: I had the claim at a fixed `1.5rem` and it pushed the
  page wide on a narrow screen. Changing it to `clamp(1.125rem, 3.6vw, 1.375rem)` fixed it. I
  would not have caught that on a laptop, which is exactly why the assignment asks.
- The favicon shows in the tab.
- Dark mode. My phone is set to dark, so I saw the dark variant before I saw the light one,
  which was a useful accident.

## Claude Project loaded

Everything the build week needs is now in the project, so I am never pasting context again:

- `identity-kit.md`, plus `tokens.css`, `logo.svg` and `favicon.svg`
- `framed-cases.md`, the three cases with the voice card at the top
- `content-map.md`, the one-line claim, the page-by-page sections, and the CTA chain
- `stack-rationale.md`, so the model does not suggest React at me again
- The style note and the voice card pinned as standing project instructions rather than left
  in a file, because instructions in a file get treated as reference and instructions in the
  project get followed

The voice card and style note are the two that need to be standing instructions. I learned that
the boring way: with the identity kit merely uploaded as a document, the first draft it gave me
used a color that is not in my palette.

## What is deliberately not there yet

No navigation, because there is nowhere to navigate to and a nav bar with dead links is worse
than no nav bar. No case pages, no about page, no portrait, no analytics, and no "coming soon"
countdown. The one line saying the cases arrive in week 5 is the only promise on the page, and
it is a promise I can keep.
