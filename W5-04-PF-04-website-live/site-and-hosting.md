# Personal Website Live on the FlyRank Domain (PF-04)

Emir Cabalak, General AI Fluency track, Week 5

**Live URL:** <https://emircabalak.github.io/>

The DNS walkthrough is the second file in this folder, `dns-walkthrough.md`.

## The plan

Five pages, not one. The card says one page is enough to start, and I had already written the
case studies in Week 2, so stopping at one would have meant holding finished work back.

| Page | What is on it |
|---|---|
| `/` | name, the one-line claim, the lead case, two more cases, one line about me |
| `/leak` | the case where two individually legal columns rebuilt my label |
| `/split` | random, grouped and time-aware splits, and why all three numbers are published |
| `/ladder` | six versions of one prompt, including the version that made things worse |
| `/about` | portrait, bio, how I work, the rest of my repositories, contact |

**Who I am and what I am building** live on the home page and About. **Future posts and capstone
work** have a home already: the case pages are one template repeated, so a fourth case is a copy
of an existing file with new content, no structural work. The agent I designed in FL-06 becomes
case four when it exists.

## Hosting

**GitHub Pages, free tier, HTTPS automatic.**

The card recommends Netlify and accepts GitHub Pages. I went with Pages for a reason I had
already written down in Week 4 before this card existed: I chose a stack with no build step and
no dependencies, and Pages serves exactly that with nothing in between. It also pairs with
PF-05, and it means the site and its source are the same thing in one place.

The trade I am accepting: Netlify's custom-domain flow is slightly friendlier. Pages does the
same job in the same number of steps, which is why the walkthrough next to this file is short.

**The URL is CV-worthy on purpose.** The repo is named `emircabalak.github.io`, which is what
makes GitHub serve it at the bare `https://emircabalak.github.io/` rather than at
`https://emircabalak.github.io/some-repo-name/`. Naming the repo anything else would have put a
project name in the middle of an address I am going to print on a CV. My internship deliverables
live in a separate repo, `flyrank-ai-fluency-internship`, so the two never mix.

## Every file, and what it does

The card asks that I understand every file I deploy. There are twelve.

| File | What it is |
|---|---|
| `index.html` and four more `.html` | the pages, hand-written, one `<nav>` copied into each |
| `style.css` | four colour variables, two font stacks, about 150 lines of layout |
| `favicon.svg` | the `ec` monogram from the Week 3 identity kit |
| `hero-texture.svg` | the scatter split by a dashed wall on the home page |
| three `icon-*.svg` | one per case, drawn to the same rules |
| `portrait.jpg` | a real photograph, 400 by 400, 20KB |
| `Emir_Cabalak_CV.pdf` | the CV, linked from the footer |
| `.nojekyll` | one empty file that stops GitHub running a build I do not need |

No JavaScript. No `package.json`. Nothing installed. The whole site including the CV is about
1.2MB, and the CV is most of it.

The one file I could not have explained a month ago is `.nojekyll`, and that is because it
comes from a bug I hit rather than from a tutorial. That story is its own deliverable in
Explain It Like You Built It.

## Required links, all four live

| Link | Where it points | Where it appears |
|---|---|---|
| LinkedIn | `linkedin.com/in/emircabalak` | footer of all five pages, and About |
| GitHub | `github.com/emircabalak` | footer of all five pages, and About |
| CV | `Emir_Cabalak_CV.pdf`, served from the site itself | footer of all five pages, and About |
| Booking | `cal.com/emircabalak`, a 30 minute Intro Call | footer of all five pages, and About |

Two notes on the booking link. Cal.com generated the event slug from the duration rather than
the name, so the direct address is `/30min` and not `/intro` as I first assumed. I link the
profile page instead of the event, because if I ever change that call to 45 minutes the `/30min`
address dies and the profile address does not.

The four links sit in the footer rather than in the body. The site has one call to action, and
it is "read the leakage case". Contact details belong where somebody goes looking for them
after they have read something, not competing with the thing I want them to read.

## Checked, not assumed

Tested against the live address, logged out, rather than from my editor.

```
GET https://emircabalak.github.io/               200
GET https://emircabalak.github.io/leak.html      200
GET https://emircabalak.github.io/split.html     200
GET https://emircabalak.github.io/ladder.html    200
GET https://emircabalak.github.io/about.html     200
GET https://emircabalak.github.io/style.css      200   text/css
GET https://emircabalak.github.io/Emir_Cabalak_CV.pdf   200   application/pdf
GET http://emircabalak.github.io/                301 -> https://
```

Link targets, followed:

```
github.com/emircabalak          200
cal.com/emircabalak             200
Emir_Cabalak_CV.pdf             200
linkedin.com/in/emircabalak     999
```

The 999 is LinkedIn refusing automated requests, which is their normal behaviour and not a
broken link. A logged-out browser gets the profile, and I checked that by hand rather than
letting a status code stand in for it.

Also confirmed on a phone, on a different browser and operating system: no horizontal overflow,
the dark variant renders, and the stylesheet applies. That last one is not paranoia. It failed
once, live, while the build status said everything had succeeded.

## What happens at the end of the track

Nothing about the build changes. A custom domain is a pointer, not a migration. When
`emir.flyrank.ai` is provisioned, Ops adds one CNAME record and I add the domain on GitHub's
side, and the same files answer at a second name. The old address keeps working.

The full checklist, what a CNAME actually is, and the four things I expect to go wrong are in
`dns-walkthrough.md` next to this file. I wrote it before I need it on purpose, because the day
it is granted is a bad day to be learning what a resolver does.
