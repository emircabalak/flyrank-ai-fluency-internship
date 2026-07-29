# Frame It as Cases

Emir Cabalak, General AI Fluency track, Week 2
Assignment code CUSTOM-MQWZWF7R-9D0535B1

## Voice card

Direct, plain, technical, no buzzwords, admits what broke.

Six words. This is now a standing instruction in my Claude Project, pasted at the top of the
project instructions so every draft inherits it:

> Voice: direct, plain, technical, no buzzwords, admits what broke. Write senior to senior.
> Short paragraphs. No em dashes. Say the thing once. If a sentence could appear in any
> portfolio, cut it. Keep my numbers exactly as I give them and never round them up.

## What the sitemap calls for

Five pieces, so five framings below. The site is one page plus three case pages.

1. Home, the claim and the one action
2. Case: the leak I found in my own features
3. Case: the split that was lying to me
4. Case: the prompt ladder, an AI-fluency piece rather than an ML one
5. About and contact, the bio and the CTA copy

---

## Case 1: the leak I found in my own features

**The problem.** I was building a classifier on FlyRank's search warehouse to flag which
client sites were about to lose visibility. The first honest-looking version scored well
enough that I stopped and reread the feature list instead of celebrating. Something was off:
the model was too confident too early, on a problem where the signal is genuinely weak.

**What I did, and what I decided.** I went through the features one at a time and asked a
single question of each: could this column have been written after the outcome I am trying to
predict? Two of them could. Neither was obviously a label copy. The label was a threshold on a
ratio, and the two columns were the numerator and the denominator, sitting in different tables
with different names. Individually both were legal. Together they rebuilt the label.

That was the decision point. The easy fix is to blacklist those two column names and move on.
I did not do that, because the next person to add a feature would just reintroduce the same
pair under different names. Instead I wrote the rule as a time rule: no column may be computed
from any window that overlaps the outcome window, no matter what it is called. Then I applied
it to every feature, which cost me a few more columns I liked.

I also checked the population filter, which is the part people skip. The rows I was keeping
had been selected partly using information from the outcome window. That does not invalidate
the model, but it is a choice a reader deserves to know about, so it went into the writeup
rather than getting quietly dropped.

**What came of it.** The score went down and stayed down. That is the result. The honest
number is lower than the leaky one and it is the one I would defend, because it is the one
that would still be roughly true next month. The leakage rule outlived the model: it is written
as a window rule, so it still holds for features that did not exist when I wrote it.

---

## Case 2: the split that was lying to me

**The problem.** Same warehouse, different mistake. My evaluation used a random split. The
data has clients in it, and each client contributes many rows over many months. A random split
puts January and March of the same client on opposite sides of the wall. The model was not
generalizing to new clients, it was recognizing clients it had already seen.

**What I did, and what I decided.** I rebuilt the split twice. First grouped by client, so no
client appears on both sides. Then time aware, so the training window ends before the test
window starts, because the panel grows over time and a model that gets to see the future is
not being tested on anything.

The decision I actually had to make was what to report. It is tempting to publish only the
honest number and pretend the random split never happened. I published both, next to each
other, with the gap called out in the text. The gap is the finding. If a random split and a
grouped split give you the same answer, your entity effect is small. Mine did not, so it
wasn't.

I also had to fix the window itself. Client history depth varies a lot in this data, so I
checked when each client's data actually starts before fixing the boundaries, and accepted
that the usable set got smaller.

**What came of it.** Three numbers instead of one: random split, grouped split, time-aware
split, each with the rows behind it. The time-aware one is the number I quote. The other two
stay visible so a reader can see the size of the correction rather than taking my word for it.
Every quality metric in the writeup comes from the evaluation run that produced it, never
recomputed on a refit that trained on the rows it was scoring.

---

## Case 3: the prompt ladder

**The problem.** I was using AI badly and getting away with it. My prompts worked well enough
that I never found out which part of them was doing the work, so I could not repeat a good
result on purpose and could not fix a bad one except by rewriting the whole thing.

**What I did, and what I decided.** I took one weak prompt from my own track and rebuilt it
in five steps, changing exactly one thing per step and saving the output every time. One layer
per version, no bundling, because bundling is how you learn nothing.

The decision that mattered was to keep the version that made things worse. Adding worked
examples made the model imitate my examples instead of thinking, and the output got narrower.
The instinct is to quietly drop that step and present a clean upward line. I kept it, because
a ladder where every rung improves is a ladder that was not actually tested.

**What came of it.** A final prompt someone else on my track can pick up and run without me in
the room, and a clearer sense of which layers actually pay. Context and quality criteria did
most of the work. Politeness and role play did none.

---

## Bio

I am Emir Cabalak. I build machine learning models and then try to break my own results before
somebody else does. Most of my work so far is on search and analytics data at FlyRank, where I
spend more time on how a model is evaluated than on which model it is. I am the person on a
team who asks where the split came from.

## Contact and CTA copy

The single call to action, used on the home page below the claim:

> Read the leakage case. It is the one where my score went down and I kept the lower number.

Contact line, on the about page only:

> emircabalak1@gmail.com. If you want the code behind any number here, ask and I will send it.

Deliberately absent: a newsletter box, a "let's connect" button, social icons, and a contact
form. One audience, one action. Anything else on the page competes with it.

---

## Before and after

The generic line AI gave me first, when I asked it to write the case-study intro with no voice
card and no interview:

> **Before.** Leveraging cutting-edge machine learning techniques, I developed a robust
> predictive model that delivers actionable insights for stakeholders. Through rigorous data
> preprocessing and feature engineering, the solution achieved impressive performance while
> maintaining scalability and reliability.

My edit:

> **After.** I built a classifier to flag client sites about to lose visibility. It scored
> better than the problem deserved, so I reread my feature list and found two columns that
> together rebuilt the label. I removed them, the score dropped, and the lower number is the
> one I report.

What changed and why. The before has no subject: nothing in it says which project, which data,
or what happened. Every phrase in it would survive being pasted into a stranger's portfolio,
which is the actual test. It also only describes success, so there is nothing in it a reader
could disagree with, which sounds safe and reads as empty. The after names the task, the
mistake, and the cost, and it is the version I would say out loud in an interview.

---

## Notes on how these were written

I did the interview first, one question at a time, before any drafting. The useful questions
were not about results. They were about decisions: what did you almost do instead, what did you
throw away, what would have happened if you had shipped the first version. Those questions are
what turned "I checked for leakage" into the numerator and denominator sitting in two different
tables.

Then I read every line out loud and cut what I would not say. What went first: "leveraging,"
"robust," "actionable insights," "at scale," and every sentence that started by announcing
what the next sentence was going to do.
