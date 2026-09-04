# Open It on Your Phone: the fix log

Emir Cabalak, General AI Fluency track, Week 6

**Live URL:** <https://emircabalak.github.io/>

Phone screenshots before and after are attached with this submission.

## How I audited it

Not by squinting. I measured the live site, logged out, at five widths: 320, 375, 768, 1024 and
1440. Every number below is a measurement taken from a rendering engine rather than an
impression, because "looks fine" is how the two real problems survived four weeks.

I asked for three things per width: does anything overflow sideways, is every tap target big
enough to hit, and does the contrast pass.

## What was already fine

Worth writing down, because a fix log that only lists failures implies everything else was
checked and it usually was not.

**No horizontal overflow at any width.** Document scroll width equals viewport width at 320,
375, 768, 1024 and 1440. The layout holds from a small phone to a wide desktop.

**The widest table fits.** Case 2 has a five-column metrics table. At 375 pixels it measures 335
wide inside a 335 wide container, so it fits without needing to scroll, at a 15px cell size.

**Contrast passes comfortably.** Measured against the actual rendered background in dark mode:
body text 14.67, headings 8.20, the call to action 6.95. AA needs 4.5. The lowest number on the
site has half again the margin it needs.

**Nothing is oversized.** Stylesheet 4KB, portrait 20KB, each SVG 1 to 2KB. The whole home page
is five requests. There is no JavaScript to compress and no image to shrink.

The one heavy file is the CV at 1.16MB, which is large for a single page and comes from the
LaTeX template embedding its fonts. It only downloads when somebody clicks it, so it costs
nothing on page load, and it stays as it is.

## What was broken

### 1. Footer links were too small to hit

The real one. At 375 pixels every footer link measured **19 pixels tall**, and the CV link was
**18 by 19 pixels**. The gap between neighbours was 12 pixels.

WCAG 2.5.8 sets the minimum target at 24 by 24. An 18 by 19 target is under it in both
directions, sitting 12 pixels from its neighbour. On a phone that is a link you miss, and the
one you hit instead is somebody's else's page.

This is the whole reason the assignment exists. The footer looks perfectly tidy on a laptop.
Nothing about it reads as broken until you measure it or try to tap it with a thumb.

**Fixed.** Footer links became inline-block with 0.55rem vertical and 0.35rem horizontal
padding, the footer font went from 0.9375rem to 1rem, and line height went to 2.4 so the rows
stop crowding each other.

| Link | Before | After |
|---|---|---|
| email | 175 x 19 | 198 x 56 |
| GitHub | 47 x 19 | 62 x 56 |
| LinkedIn | 59 x 19 | 74 x 56 |
| **CV** | **18 x 19** | **31 x 56** |
| Book a call | 73 x 19 | 89 x 56 |

### 2. Navigation links were one pixel over the line

Every nav link measured **25 pixels tall**. That clears the 24 pixel minimum by one pixel, which
is passing on a technicality rather than being comfortable. The common guidance is 44.

**Fixed.** 0.6rem of vertical padding on each nav link. All five are now **44 pixels tall**. The
nav gap was split into 0.25rem vertical and 1.5rem horizontal so wrapped rows do not collide.

After the change, nothing on the page is under 24 pixels tall except three inline links inside
running text, which are words in a sentence rather than buttons.

### 3. The most important case had no icon

The home page gives the lead case a coloured rule and three sentences, and gives the two
supporting cases an icon each. So the two things I want read less had a visual marker and the
one thing I want read most did not.

**Fixed.** The lead case now carries `icon-leak.svg` at 40 pixels.

### 4. The home page did not say what the site was for

Not a layout bug, and it belongs here because it was found the same way: by putting it in front
of somebody. When I sent the bare link to a friend in Week 5, their first message back, before
opening it, was "ne işe yarıyor", what is it for.

The home page said what I do. It did not say what a reader gets or how long it takes.

**Fixed.** One line under the claim: three write-ups about a number that looked good for the
wrong reason and what it cost me to find out, fifteen minutes if you read one.

### 5. Case 2 lost the only person who read it

The same reader stopped in case 2 and said the sentences were hard to hold. That page sits in
the middle of the reading path, and the only outward call to action is at the end of case 3, so
losing people there loses the whole chain.

**Fixed.** Every section of case 2 now opens with one plain sentence saying what the section is
about before it starts arguing, and the four longest paragraphs were split. Nothing was removed
and no number changed. The technical vocabulary stayed, because the reader it is written for
knows those words.

### 6. The icons were white boxes in dark mode, and only a real phone showed it

Found last, and not by me.

I audited five widths and fixed five things, then took the after-screenshots on an actual phone.
The case icons were rendering as small white squares against the dark page. Next to a link, they
read as broken images rather than as icons.

The cause was in the SVGs. Each one carried `<rect width="96" height="96" fill="#FAF9F7"/>`, the
light paper colour, baked in as a background. On the light theme that disappears into the page.
On the dark theme it is a white block. The split icon was worse: its dashed divider was
`#16181D`, the near-black ink colour, which on a near-black background is simply not there.

**Fixed.** The background rectangle is gone from all three, so the page shows through. The
stroke colours moved to values that clear the 3:1 non-text contrast threshold on both grounds
rather than only on one:

| Element | Before | After | On light | On dark |
|---|---|---|---|---|
| strokes and dots | `#2E4B6B` | `#6E90B5` | 3.16 | 5.45 |
| the accent element | `#C2410C` | `#E2703A` | 3.02 | 5.70 |
| the split divider | `#16181D` | `#8A8F98` | 3.09 | 5.57 |

**Why my audit missed it.** I measured geometry: widths, heights, overflow, computed font sizes,
contrast of text against its background. Every one of those numbers was correct while the icons
looked broken, because an icon with a white background has perfectly good contrast. It just
looks wrong.

That is the argument for this assignment in one bug. A headless browser at 375 pixels answers
"does it fit and can you tap it". It does not answer "does it look like something went wrong",
and a person glancing at a phone answers that in about a second.

The hero image keeps its light panel deliberately. It has a border, it holds a chart with axis
labels, and it reads as a figure on paper rather than as a broken element. The small icons had
no such excuse.

## The mistake I nearly made while verifying the fixes

After pushing, I remeasured and the footer links still came back at 19 pixels. The HTML had
updated, the stylesheet on the server had updated, and the rendered page had not.

The browser was still using the stylesheet it had cached. Fetching the CSS with a cache-busting
query string and applying it gave 44 and 56 pixels immediately.

So for a few minutes I had a working fix and a measurement saying it had failed. If I had
trusted the measurement I would have gone looking for a bug in CSS that was already correct.
The same caching that makes a DNS change look broken for one person and fine for another was
sitting between me and my own page.

## Still open

**The three empty screenshot boxes** on the case pages. They are honest placeholders and they
are still three dashed rectangles announcing unfinished work.

**No analytics**, so I still cannot tell whether any of this is read.

**Mobile is now verified, not designed.** I have confirmed that nothing overflows, everything is
tappable and the type scales. I have not asked whether a five-column table is a good experience
on a phone, only whether it fits.

**The navigation wraps to two rows on a phone**, with About alone on the second line. Six items
do not fit across 375 pixels at a comfortable tap size, and I would rather have the wrap than
shrink the targets I just spent this assignment enlarging.
