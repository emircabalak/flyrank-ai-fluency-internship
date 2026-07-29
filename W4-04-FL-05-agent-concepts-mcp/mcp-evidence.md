# FL-05 evidence: the MCP connector and the three tasks

Emir Cabalak, General AI Fluency track, Week 4

## The setup

**MCP client:** Claude Code.
**MCP server:** the browser server, which exposes a real Chromium instance over MCP.
**Tools used:** `preview_start`, `navigate`, `resize_window`, `javascript_tool`,
`read_console_messages`, `read_network_requests`.

Configuration, `.claude/launch.json` in the repo root, which is how the server is told what to
run:

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

The thing under test is my own Week 4 site, the near-blank page from Empty but Live. That is
deliberate. I wanted three tasks I actually needed done, not three demos.

## Why these three tasks are impossible in plain chat

Chat can read my HTML and CSS and tell me what it thinks will happen. It cannot run a browser.
Everything below is a measurement taken from a live rendering engine, and in the first attempt
one of those measurements came back wrong, which is the whole argument for doing it this way.

---

## Task 1: start a real server and read back the computed styles

**Tool calls:** `preview_start` then `javascript_tool`.

`preview_start` launched `python -m http.server` on port 8017 and returned:

```
serverId: b281a6f1-f315-42e5-babe-c1546ccd52ca
port: 8017
Server started successfully on port 8017. Opened tab "tab-7" at http://localhost:8017
```

Then, executed inside the page:

```js
JSON.stringify({
  bg: getComputedStyle(document.body).backgroundColor,
  ink: getComputedStyle(document.body).color,
  link: getComputedStyle(document.querySelector('footer a')).color,
  headingFont: getComputedStyle(document.querySelector('h1')).fontFamily
})
```

Returned:

```json
{"bg":"rgb(20, 22, 26)","ink":"rgb(233, 231, 227)","link":"rgb(240, 131, 77)",
 "headingFont":"\"Space Grotesk\", \"Segoe UI\", Helvetica, Arial, sans-serif"}
```

`rgb(20,22,26)` is `#14161A`, `rgb(233,231,227)` is `#E9E7E3`, and `rgb(240,131,77)` is
`#F0834D`. All three are my dark-mode values from the identity kit, which means the
`prefers-color-scheme` block fired and the browser it is running in is set to dark. I had never
checked the dark variant against the real engine, only read it.

**What this caught.** My first attempt at this task pointed the browser at the file directly
rather than through a server, and the same call returned `bg: rgba(0,0,0,0)`, `link:
rgb(0,0,238)`, and a 16px claim. Default browser styling. The stylesheet had not loaded at all.
It was an artifact of how that mode serves local files rather than a bug in my CSS, but I only
know that because I had a number in front of me instead of an opinion. If I had written "dark
mode verified" off the first run I would have written something false.

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
{"viewport":"375x812","scrollW":375,"horizontalOverflow":false,"h1":"32px","claim":"18px"}
```

`scrollW` equals the viewport width, so nothing overflows sideways, which is the failure mode
that makes a phone page scroll horizontally and feel broken.

The two font sizes are the ones I actually wanted. My heading is `clamp(2rem, 7vw, 2.75rem)`.
At 375 pixels, 7vw is 26.25px, below the 32px floor, so the clamp should return 32px. It
returned 32px. The claim is `clamp(1.125rem, 3.6vw, 1.375rem)`, where 3.6vw is 13.5px, below
the 18px floor, so it should return 18px. It returned 18px.

I can compute both of those by hand. Computing them by hand is not the same as knowing the
browser agrees, and the mobile overflow bug I hit in Week 4 was exactly a case where my
arithmetic was right and my markup was wrong.

---

## Task 3: check the network and the webfonts

**Tool calls:** `read_console_messages` and `read_network_requests`, then `javascript_tool`.

```
read_console_messages -> No console logs.

read_network_requests ->
[B77706AAADF5F95ACE7121CA01A9EB0E] GET http://localhost:8017/ -> 200 OK
[22772.27]                        GET http://localhost:8017/style.css -> 200 OK
```

Zero console messages of any level, so nothing is erroring quietly. Two requests, both 200, and
no request for anything I did not intend to ship. For a page whose selling point is that it has
no JavaScript and no dependencies, a network log with exactly two entries is the proof of that
claim rather than a restatement of it.

Then the font question, which the network log alone does not answer because `@import` fetches
happen in a separate pass:

```js
JSON.stringify({
  spaceGroteskAvailable: document.fonts.check("600 32px 'Space Grotesk'"),
  plexAvailable: document.fonts.check("400 17px 'IBM Plex Sans'"),
  loaded: [...document.fonts].filter(f => f.status === "loaded").map(f => f.family + " " + f.weight)
})
```

Returned:

```json
{"spaceGroteskAvailable":true,"plexAvailable":true,
 "loaded":["IBM Plex Sans 400","Space Grotesk 500","Space Grotesk 600"]}
```

Three faces loaded, the three the page uses. `IBM Plex Sans 600` shows as unloaded because
nothing on a near-blank page is bold yet, and the browser only downloads a face when something
needs it. That is correct behavior and it is also a small trap: when the case pages arrive with
bold text, that face will load and I should recheck. I would not have known to expect that
without seeing the list.

---

## Summary of tool use

| Task | Tools | What it produced that chat could not |
|---|---|---|
| 1 | `preview_start`, `javascript_tool` | live computed colors from a rendering engine, and a caught false positive |
| 2 | `resize_window`, `javascript_tool` | real overflow and clamp measurements at 375px |
| 3 | `read_console_messages`, `read_network_requests`, `javascript_tool` | the actual request log and font load state |

All three are reads of a live process. Nothing in this file is a prediction about what a browser
would do.
