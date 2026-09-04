# Make It Do Something

Emir Cabalak, General AI Fluency track, Week 6

**The live feature:** <https://emircabalak.github.io/checker.html>

One feature. A leakage checker. Give it a table of features and tell it which column is the
label, and it finds pairs of columns that are harmless on their own and together rebuild the
thing you are trying to predict.

Press **Load the example** and it runs on 961 rows in front of you.

## Why this one

The card says most people should build a contact form, and for some a live demo of their own
work is the better answer. My site already has four ways to reach me and none of them are the
thing anybody is deciding on. What a reader cannot currently do is check whether I am right.

This is [case 1](https://emircabalak.github.io/leak.html) turned into a tool. That
case is the strongest thing on my site and it asks you to take my word for it. Now you can run
the same check on your own data and see whether it finds anything.

## What it does, in order

1. You paste a CSV, or press the example button.
2. It splits the text into columns and works out which ones are numbers.
3. It correlates every numeric column with the label, one at a time. This is the check most
   people do, and on a real leak it usually finds nothing.
4. It works out what guessing the majority class already scores. If 71% of your rows are zero,
   then always answering zero scores 0.71, and anything near 0.71 is not a finding.
5. It divides every numeric column by every other numeric column, applies your threshold, and
   asks how often that reproduces the label. Every ordered pair, both directions.
6. It shows the best five pairs with their distance from chance, and flags any column whose
   zeros look like a missing marker rather than a real zero.

On the example, the strongest single column correlates with the label at **-0.15**, which
nobody would investigate. One pair reproduces the label on **all 961 rows**, which is **0.29
above chance**. That gap is the entire argument for the tool.

## What a backend is, and why this has none

A **backend** is a computer somewhere else that runs code for you. You send it something, it
does work you cannot or should not do on your own machine, and it sends an answer back. It is
where a contact form's email actually gets sent from, where a password gets checked, and where
a database lives. You need one when the work needs a secret you cannot show anybody, or data
that has to outlive the browser tab, or power the visitor's laptop does not have.

**This feature has none of those needs**, so it does not have one.

There is no secret: the code does arithmetic. There is nothing to remember: when you close the
tab, it is gone, and that is correct because it was your data. And the work is small enough
that a phone does it in milliseconds.

So the whole thing is one file of JavaScript sitting next to my HTML.

## How the data flows

This is the part I want to be exact about, because it is the reason I would send this link to
somebody with a real feature table.

```
   your CSV                        your browser tab
   (in the textarea)  ----->   parse, correlate, scan pairs   ----->   the result on screen

                                        |
                                        |  nothing crosses this line
                                        v
                                 no server, no network,
                                 no database, no log
```

When you press **Check it**, the text in the box goes into a JavaScript function running in
your own tab. Nothing is sent anywhere. There is no upload, no request, no endpoint, no
database row, and no copy of your file on any machine but yours.

I can say that without hedging, and you can verify it rather than trusting me: open the network
tab in your browser's developer tools and press the button. You will see nothing new. The only
request the page ever makes is the one that fetches the example file when you ask for it, and
that fetch goes to my own site to pull a file down, not to push yours up.

That property is the reason the feature is useful. The people who would most want to run a
leakage check are working on data they are not allowed to paste into somebody's website. A tool
that needs a server is a tool they cannot use.

## What it does not do

Written on the page itself, not just here.

It only tests ratios of pairs. A leak expressed as a difference, a product, or spread across
three columns walks straight past it.

It cannot tell when a column was computed. A column backfilled after the outcome closed, with an
innocent name and a mild correlation, is invisible to it.

It cannot see how your rows were chosen. If the population itself was filtered on something
from the outcome window, every column can be clean and the answer still wrong.

Those three are the same limits the Python version has, and I found them by running it against
six datasets where I already knew the answer. It scored five out of six. The one it failed was
the population case, and it failed it in a way I do not think tuning fixes.

## Checked, not assumed

Tested against the live address in a real browser before I said any of this.

Running the example on <https://emircabalak.github.io/checker.html>:

```
Found 3 column pairs that rebuild the label.
961 rows, 13 columns. Label rate 0.292, baseline 0.7076.

numerator                  denominator           agreement   over baseline
tracked_terms_returning    term_universe_size       1.0000        +0.2924
tracked_terms_returning    total_queries            0.8356        +0.1280
tracked_terms_returning    queries_with_data        0.7846        +0.0770

Strongest single column: tracked_terms_returning at -0.1513

Checked 961 rows in 27ms, entirely in this tab.
```

Those are the same figures the Python version produces on the same file, which is the check that
the browser version is doing the real work rather than a simplified version of it.

The network log for that whole run, taken from the live page:

```
GET https://emircabalak.github.io/checker.html    200
GET https://emircabalak.github.io/style.css       200
GET https://emircabalak.github.io/checker.js      200
GET https://emircabalak.github.io/sample-features.csv  200
```

Four requests, all GET, all pulling files down. No POST, no upload, nothing leaving the tab.
That is the data-flow claim above, verified rather than asserted.

The rest, also tested.

A clean table of random numbers returns "Nothing above chance", so it does not invent findings.

A wrong label name returns the column names it did find, instead of a stack trace.

An empty box asks for input instead of failing.

Zero console errors, no page overflow at 375 pixels, buttons 44 pixels tall, and the results
table scrolls inside its own container rather than pushing the page sideways.
