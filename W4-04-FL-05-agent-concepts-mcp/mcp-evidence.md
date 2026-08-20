# FL-05 evidence: the MCP connector and the three tasks

Emir Cabalak, General AI Fluency track, Week 4

## The setup

**MCP client:** Claude Code.
**MCP server:** the browser server, which exposes a real Chromium instance over MCP.
**Tools used:** `navigate`, `resize_window`, `javascript_tool`, `read_console_messages`,
`read_network_requests`, plus `preview_start` for the local runs.

The thing under test is my own site, live at `https://emircabalak.github.io/`. That is
deliberate. I wanted three tasks I actually needed done, not three demos, and pointing the
browser at the public URL means anybody can rerun these and get the same numbers.

For the local runs the server is configured in `.claude/launch.json` at the repo root:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "site",
      "runtimeExecutable": "python",
      "runtimeArgs": ["-m", "http.server", "8017", "--directory", "deliverables/site"],
      "port": 8017
    }
  ]
}
```

## Why these three tasks are impossible in plain chat

Chat can read my HTML and CSS and tell me what it thinks a browser will do. It cannot run one.
Everything below is a measurement taken from a live rendering engine, and on the first attempt
one of those measurements came back wrong, which is the whole argument for doing it this way.

---

## Task 1: read the computed styles off the live page

**Tool calls:** `navigate` then `javascript_tool`.

```js
JSON.stringify({
  url: location.href,
  bg: getComputedStyle(document.body).backgroundColor,
  ink: getComputedStyle(document.body).color,
  accent: getComputedStyle(document.querySelector('.cta a')).color,
  scripts: document.scripts.length
})
```

Returned:

```json
{"url":"https://emircabalak.github.io/","bg":"rgb(20, 22, 26)","ink":"rgb(233, 231, 227)",
 "accent":"rgb(240, 131, 77)","scripts":0}
```

`rgb(20,22,26)` is `#14161A`, `rgb(233,231,227)` is `#E9E7E3`, and `rgb(240,131,77)` is
`#F0834D`. All three are the dark-mode values from my identity kit, so the
`prefers-color-scheme` block is firing and the browser it runs in is set to dark. I had never
checked the dark variant against a real engine, only read it.

`scripts: 0` is the one I care about most. My whole stack argument in Three Roads was that this
site ships no JavaScript. That is now a measured fact rather than an intention.

**What this caught.** My first attempt at this task pointed the browser at the file directly
rather than through a server, and the same call returned `bg: rgba(0,0,0,0)` and
`link: rgb(0,0,238)`. Default browser styling, no stylesheet. It turned out to be an artifact
of how that mode serves local files rather than a bug in my CSS, but I only know that because I
had a number in front of me instead of an impression. If I had written "dark mode verified" off
the first run I would have written something false.

That false positive was worth more than the pass, because the same failure signature, a page
serving with no stylesheet, is exactly what later happened for real on GitHub Pages when Jekyll
ate my `style.css`.

---

## Task 2: measure the mobile layout at 375 by 812

**Tool calls:** `resize_window` with the mobile preset, then `javascript_tool`.

```
Viewport set to 375x812 (mobile).
```

```js
JSON.stringify({
  viewport: innerWidth + "x" + innerHeight,
  scrollW: document.documentElement.scrollWidth,
  horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
  h1: getComputedStyle(document.querySelector('h1')).fontSize,
  claim: getComputedStyle(document.querySelector('.claim')).fontSize
})
```

Returned:

```json
{"viewport":"375x812","scrollW":375,"horizontalOverflow":false,"h1":"28px","claim":"18px"}
```

`scrollW` equals the viewport width, so nothing overflows sideways. That is the failure that
makes a phone page scroll horizontally and feel broken, and it is invisible on a laptop.

The two font sizes are the ones I wanted. My heading is `clamp(1.75rem, 6vw, 2.5rem)`. At 375
pixels 6vw is 22.5px, below the 28px floor, so the clamp should return 28px. It returned 28px.
The claim is `clamp(1.125rem, 3.6vw, 1.375rem)`, where 3.6vw is 13.5px, below the 18px floor,
so it should return 18px. It returned 18px.

I can do both of those calculations by hand. Doing them by hand is not the same as knowing the
browser agrees, and the arithmetic being right is not much comfort when the markup is wrong.

I ran the same check on `split.html`, which carries the widest table on the site, five columns.
At 375 pixels the table measured 335 wide inside a 335 wide container with no overflow, so the
table fits without needing to scroll.

---

## Task 3: read the network log and the font loading state

**Tool calls:** `read_network_requests` and `read_console_messages`, then `javascript_tool`.

```
read_network_requests ->
GET https://emircabalak.github.io/                   -> 200
GET https://emircabalak.github.io/style.css          -> 200
GET https://emircabalak.github.io/hero-texture.svg   -> 200
GET https://emircabalak.github.io/icon-split.svg     -> 200
GET https://emircabalak.github.io/icon-ladder.svg    -> 200

read_console_messages -> No console logs.
```

Five requests, all 200, nothing I did not intend to ship, and no request to any third party
except the font host. Zero console messages of any level, so nothing is failing quietly.

This is the task that would have caught the Jekyll bug on its own. When `style.css` was
returning 404 on the live site, this exact call is what showed it, while the GitHub Pages build
status still said `built` with no error. A green build is not a working site, and the request
log is the thing that knows the difference.

Then the fonts, which the request log does not answer because `@import` fetches happen in a
separate pass:

```js
JSON.stringify({
  grotesk: document.fonts.check("600 28px 'Space Grotesk'"),
  plex: document.fonts.check("400 17px 'IBM Plex Sans'"),
  loaded: [...document.fonts].filter(f => f.status === "loaded").map(f => f.family + " " + f.weight)
})
```

Returned:

```json
{"grotesk":true,"plex":true,
 "loaded":["IBM Plex Sans 400","IBM Plex Sans 600","Space Grotesk 500","Space Grotesk 600"]}
```

Four faces loaded, exactly the four the site declares. Worth noting that on the earlier
near-blank version of this page only three came back loaded, because nothing on it was bold yet
and a browser only downloads a face when something needs it. That is correct behaviour and it
is a small trap: a font can look fine until the first bold word appears.

---

## Summary of tool use

| Task | Tools | What it produced that chat could not |
|---|---|---|
| 1 | `navigate`, `javascript_tool` | live computed colors and a script count from a real engine, plus a caught false positive |
| 2 | `resize_window`, `javascript_tool` | real overflow, clamp and table measurements at 375px |
| 3 | `read_network_requests`, `read_console_messages`, `javascript_tool` | the actual request log and font load state |

All three are reads of a live process against a public URL. Nothing in this file is a prediction
about what a browser would do, and all of it can be rerun.
