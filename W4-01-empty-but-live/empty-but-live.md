# Empty but Live: Ship a Blank Page

Emir Cabalak, General AI Fluency track, Week 4
Assignment code CUSTOM-MQX07T4U-1F9328FE

## What is live

**URL:** `https://emircabalak.github.io/`
**Repo:** `https://github.com/emircabalak/emircabalak.github.io`

Live over HTTPS, HTTP redirects to it with a 301, certificate valid. Screenshot taken on my
phone is attached with this submission.

## One thing to say up front

The assignment is called Empty but Live and the page at that URL is not empty. It has five
pages and all three case studies on it.

That is not me quietly moving the goalposts, so here is the actual sequence. I built the
near-blank version first: name, the one-line claim, one line saying the cases were not there
yet, my email. I styled it with the identity kit and I checked it in a real browser. Then,
before I had pushed anything, I kept going and wrote the case pages, because the writing was
already done in Week 2 and it felt silly to stop. By the time I ran `git push` for the first
time, the repo was the whole site.

So the first commit in that repo is `Add portfolio site: home, three case pages, about`, and
anybody can check that. There is no blank-page commit and I am not going to invent one. What I
can show is the milestone this card is actually about, which is the gap between "it works on my
machine" and "it works on a URL". That gap turned out to be real, and it is the interesting
part of this writeup.

## The project

Matches the stack I chose in Three Roads: hand-written HTML and CSS on GitHub Pages, no build
step, no dependencies.

```
index.html  leak.html  split.html  ladder.html  about.html
style.css
favicon.svg  hero-texture.svg  icon-leak.svg  icon-split.svg  icon-ladder.svg
portrait.jpg
.nojekyll
```

No `package.json`, no `node_modules`, nothing to install, and zero JavaScript. I can explain
every one of those files, which is the point of choosing this stack.

The repo is named `emircabalak.github.io` rather than something descriptive, because that exact
name is what makes GitHub serve it at `https://emircabalak.github.io/` instead of
`https://emircabalak.github.io/some-repo-name/`. The URL is going on a CV, so the path matters.
My assignment deliverables live in a separate repo, `flyrank-ai-fluency-internship`, because
they belong to the internship and this site does not.

## What I checked before pushing

I served the folder locally with `python -m http.server` and drove a real browser at it rather
than trusting how it looked. At 375 pixels wide: document scroll width 375, so no horizontal
overflow. Heading resolved to 28px and the claim to 18px, which are the floors of their
`clamp()` values at that width, so the clamps were doing what I thought. Background resolved to
`rgb(20, 22, 26)`, which is my dark-mode paper, so the `prefers-color-scheme` block was firing.
Zero console messages.

Everything passed. Then I pushed, and it broke.

## The bug that only exists on a URL

First load of the live site: the page rendered in Times New Roman on a white background with
blue underlined links. Default browser styling. The stylesheet was not there.

`style.css` was returning 404 while `index.html`, every SVG and every other page returned 200.
The file was in the repo, on `main`, at the root. The GitHub Pages build reported `built` with
no error message.

The cause is that GitHub Pages runs Jekyll over the repo by default, and the stylesheet was not
surviving that pass. The fix is a single empty file at the repo root:

```bash
touch .nojekyll
```

That tells Pages to skip the whole build step and serve the files as they are. One commit, and
`style.css` came back as 200 with `Content-Type: text/css`.

This is the reason the card exists, and I would not have found it any other way. My local
server had been serving the same eleven files correctly for an hour. Nothing about the code was
wrong. The difference was entirely in what sat between the files and the browser, and the only
way to see it was to put the files on a URL and ask for them over the network.

The second lesson is smaller and worse: the Pages build said `built`. A green build is not a
working site. I now check the actual response code for every file rather than the build status.

## Confirming it is really live

A laptop is not proof. A page can render perfectly from a local file and be broken on the
internet, which is precisely what happened here.

So I opened the URL on my phone, on a different browser and a different operating system from
the machine that built it. Nothing about that page is being served from my laptop.

What I checked while the device was in my hand, and what the screenshot shows:

- The page loads at all, which is the whole assignment.
- The address bar says `emircabalak.github.io`, so it is the public URL and not a local file.
- The stylesheet actually applied, since that is the thing that had just been broken. The
  screenshot is the proof: real fonts, my colours, the accent rule down the side of the lead
  case.
- Dark mode. My phone is set to dark, so I saw the dark variant before I ever saw the light one.
- The claim wraps onto three lines and nothing runs off the side, which is what the `clamp()`
  on that line is for.
- Chrome on Android no longer draws a padlock, so I checked the certificate separately from the
  laptop instead: HTTP returns a 301 to HTTPS and the certificate is valid.

## Claude Project loaded

Everything the build week needs is in the project, so I am never pasting context again:

- `identity-kit.md`, plus `tokens.css`, `logo.svg` and `favicon.svg`
- `framed-cases.md`, the three cases with the voice card at the top
- `content-map.md`, the one-line claim, the page-by-page sections, and the CTA chain
- `stack-rationale.md`, so nothing suggests React at me again

The voice card and the style note are pinned as standing project instructions rather than left
in a file, because instructions in a file get treated as reference and instructions in the
project get followed. I learned that the boring way: with the identity kit merely uploaded as a
document, the first draft I got back used a colour that is not in my palette.

## What is deliberately not there

No analytics, no cookie banner, no contact form, no social row, and no JavaScript at all. The
network log for the home page is the HTML, the stylesheet and three SVGs. For a site whose one
action is "read a case study end to end", the number of things loading before the text appears
is a number worth keeping small.
