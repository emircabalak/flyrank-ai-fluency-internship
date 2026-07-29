# Three Roads: Choose Your Stack with AI

Emir Cabalak, General AI Fluency track, Week 4
Assignment code CUSTOM-MQX06U8B-9AAA4FBA

## The constraints I gave it

Four, stated flatly, plus the sitemap and content map pasted in full.

**Free only.** Not free trial, not free tier that expires. If it costs money in month four I do
not want it in month one, because a portfolio that goes dark when a card expires is worse than
no portfolio.

**Honest skill level.** I write Python and SQL daily. I can read HTML and CSS and change them,
and I have never built a site from scratch. I have used git for two months. I have never used a
JavaScript framework, never run a build step I did not copy from a README, and I do not know
what hydration means. That last part I made a point of saying, because the first answer I got
when I was vaguer assumed React knowledge I do not have.

**What the portfolio has to do.** Five pages: home, three case pages, about. Long-form reading
is the primary job. The cases are 800 to 1,200 words each with a numbers table in the middle.
Static content that changes maybe twice a month.

**How the work must be displayed.** This is the constraint that actually decided it. My work is
prose, tables of numbers, and a handful of screenshots. No image gallery. No video. No live
notebook. The tables have to be real HTML so they are selectable, searchable, and readable on a
screen reader, not pictures of tables. Type has to be good, because a reader who bounces off a
wall of text never reaches my numbers.

**Does anything have to be dynamic yet?** No. I said so up front and I said it again when the
model started suggesting a CMS. Week 8 of this track requires exactly one dynamic feature, so I
told it that too: whatever I pick has to have a path to one small feature later without a
rebuild.

## The three options it produced

### Option 1, simplest: hand-written HTML and CSS on GitHub Pages

**How I would build it.** Five `.html` files and one `.css` file. No build step, no
dependencies, no `node_modules`. The shared header and footer get copy-pasted into each of the
five pages. `tokens.css` from the identity kit gets imported by the stylesheet.

**Hosting.** GitHub Pages, free forever on a public repo, custom domain supported, HTTPS
included.

**Backend?** None.

**The real trade-off.** Duplication. If I change the footer I change it in five places. With
five pages that is a two-minute find and replace. At fifty pages it is a genuine problem and I
would have picked wrong.

### Option 2, middle: Astro on Cloudflare Pages

**How I would build it.** Cases as markdown files, one layout component, Astro renders it to
static HTML at build time. Content and presentation separate.

**Hosting.** Cloudflare Pages, free tier, builds on push, generous limits.

**Backend?** None by default, and Cloudflare Workers are sitting right there when I want one.

**The real trade-off.** A build step and a dependency tree I would be responsible for. Astro,
Vite, and about 300 transitive packages. It works beautifully until a dependency has a breaking
change eight months from now and I am debugging a build error in a tool I chose for a five-page
site.

### Option 3, most powerful: Next.js on Vercel

**How I would build it.** React components, MDX for the cases, an API route for the Week 8
feature, image optimization included.

**Hosting.** Vercel free tier.

**Backend?** Yes, API routes are built in.

**The real trade-off.** I would be learning React, the app router, server components, and
deployment conventions all at once, on a five-page reading site that needs none of them. Vercel
is free now and its free tier has changed before.

## Pressure test

I asked all four questions and pushed back on the answers.

**What breaks if I pick the simplest?** The honest answer is the footer duplication, and it
only bites past roughly fifteen pages. The answer I was given first was "you will outgrow it,"
which is a prediction rather than a failure mode, so I asked for the specific page count where
it hurts. Fifteen is a number I can check against my sitemap. My sitemap has five.

The second thing that breaks is that adding a sixth page is manual. That is real and it is
about ninety seconds of copy and paste.

What does not break, and I checked: typography, tables, mobile layout, accessibility, page
speed, and custom domains are all fine on plain HTML. Every requirement my content map actually
has is met by the simplest option, which is the finding.

**What do I maintain if I pick the most powerful?** A dependency tree I did not read, a
framework with a major version bump roughly annually, and a build that can break without me
touching anything. On my current skill level that is not a small tax, it is the difference
between fixing the site in an evening and not fixing it at all. The maintenance question is not
"can I handle it today," it is "can I handle it on a bad week in November," and the answer for
Next.js is no.

**Can I finish in two weeks?** Option 1, yes, comfortably, because there is nothing to learn
before I start writing content. Option 2, probably, with maybe two days lost to Astro's
conventions. Option 3, not honestly. I would finish something in two weeks, and it would be a
tutorial with my name on it.

**Does it show my work the way it needs to be shown?** All three render HTML tables and long
prose correctly, so on the deciding constraint they tie. Option 3's advantages are image
optimization and interactivity, and my content map has nine images, three of which are vector
and four of which are screenshots. There is nothing to optimize.

## The decision

**I chose option 1: hand-written HTML and CSS on GitHub Pages.**

The deciding argument is not that it is easiest. It is that my content map asks for exactly
nothing the other two options are better at. Astro's advantage is content scaling and I have
five pages. Next.js's advantage is interactivity and dynamic rendering, and my answer to "does
anything need to be dynamic" was no. Picking either would mean paying a real maintenance cost
for a capability my own plan says I do not need.

**Can I maintain this?** Yes, and this is the part I am most confident about. There is nothing
to maintain. No dependencies means no dependency updates, no lockfile, no build that can break,
no framework version to track. If I do not touch the site for a year it works exactly as it
does today. HTML and CSS from 2015 still render. I cannot say that about a `package.json` from
2015. On top of that, plain HTML is the one part of this stack I can fully read, so when
something is wrong I can find it myself instead of pasting an error into a chat and hoping.

**Does it show my work well?** Yes, and slightly better than the alternatives, for one reason
I did not expect going in. With no framework there is no client-side JavaScript at all, so the
page renders instantly and the text is there before anything else loads. For a site whose one
action is "read a case study end to end," time to readable text is the metric that matters,
and the simplest option wins it outright.

**Backend: not yet.** Nothing on the site needs one today. The three cases are prose and
numbers, and the contact method is my email address in plain text.

For Week 8 I already know what the one feature will be, and I checked that it fits before
committing to this stack. It is a small in-browser leakage checker: paste your column names and
your label definition, and it flags any pair of columns that could rebuild the label. It is the
rule from case 1 turned into something a visitor can run. It is pure client-side JavaScript in
one `.js` file, so it needs no server, no API route, and no build step, and it can be added to
this stack by writing one script tag. That is the check that option 1 is not a corner I painted
myself into.

If I am wrong about that and I do need a server later, the escape is cheap: the same repo
deploys to Cloudflare Pages without changing a file, and a Worker gives me an endpoint. Moving
from plain HTML to anything else is easy in a way that moving off Next.js is not, which is
itself an argument for starting simple.

## The two I did not choose

**Astro** is the option I would pick if I were wrong about page count. It is genuinely well
suited to a content site and I liked it. I did not choose it because it solves a scaling
problem I do not have, and it charges for that in a dependency tree I would own. If this site
reaches fifteen pages I will move to it, and the move is not painful, because markdown case
files and plain HTML case files are close relatives.

**Next.js** is the wrong tool for this job at any page count I can foresee. It is a good
framework for an application. My site is a document. Choosing it would be choosing to spend my
build weeks learning React instead of writing my cases, and the cases are the thing anyone is
actually going to judge me on.

The general lesson, and the reason this assignment was worth two hours: the model's first
answer, before I gave it my real skill level, was Next.js. It was not being lazy. It was
answering the question most people ask, which is "what is the best stack." That is not my
question. My question was "what is the best stack for a person who has never run a build step,
building five pages of prose, who needs it to still work in a year." Once the constraints were
real, the same model argued for plain HTML without me steering it there. The constraints did
the choosing. My job was to state them honestly, including the unflattering one about not
knowing JavaScript.
