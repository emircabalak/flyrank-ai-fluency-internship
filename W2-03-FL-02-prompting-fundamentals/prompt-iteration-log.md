# Prompting Fundamentals on Real Tasks v2 (FL-02)

Emir Cabalak, General AI Fluency track, Week 2

## Tutorial notes first

I worked through the basics chapters of Anthropic's Prompt Engineering Interactive Tutorial
before touching my own task. Three things from it changed how I write prompts, and I am
listing them because they show up in the iterations below.

The first is that the system prompt and the user turn do different jobs. The system turn is
for who the model is and what rules always apply. The user turn is for this specific request.
I had been dumping everything into one blob.

The second is that models follow the last clear instruction more reliably than the first, so
the ordering of a prompt is not cosmetic. Putting the output format at the end works better
than putting it in the middle.

The third is prefilling the assistant turn. Starting the response for the model is the
bluntest way to kill preamble, and it worked on the first try where three rounds of "no
preamble, do not restate the question" had not.

## The task

From my FL-01 AI workflow audit, the task I do most often with AI and get the least reliable
results on: turning a finished experiment run into the markdown writeup that sits above the
code in my notebook.

This is a real recurring job. Every experiment I run in the ML track needs a few paragraphs
explaining what the cell below does, what came out, and what it means. I write several of
these a week. Getting them wrong is not a formatting problem, it is a claims problem: the
generic version always overstates the result, and an overstated result in a notebook is
something I have to defend later.

The input is the same every time: a metrics dict from the run, a one-line description of what
changed since the last run, and the split I used.

For all six runs I used the same real input so the comparison is fair:

```
run: grouped-cv-v3
change since last run: switched from random 5-fold to GroupKFold on client_id
metrics: roc_auc 0.71 (was 0.84 under random split), pr_auc 0.33, base rate 0.19,
         n_clients 412, n_rows 9,840, positives 1,870
split: GroupKFold(5) on client_id, time window 2024-03 to 2025-02
```

---

## V0: the naive prompt

This is what I would have typed a month ago.

**Prompt**

> Write a summary of these results.
> [metrics pasted]

**Output, excerpt**

> The grouped cross-validation experiment demonstrates strong model performance, achieving a
> ROC AUC of 0.71 across 412 clients and 9,840 observations. While this represents a decrease
> from the previous random split configuration (0.84), the grouped approach provides a more
> robust and realistic estimate of generalization performance. The PR AUC of 0.33 indicates
> meaningful precision-recall tradeoff behavior. Overall, these results suggest the model
> captures genuine signal and is well positioned for further refinement.

**What is wrong with it.** "Strong model performance" for a 0.71 is a claim I would have to
walk back. It calls the drop from 0.84 a decrease and then immediately reassures, which is the
opposite of the point: the drop is the finding. It says the 0.33 PR AUC "indicates meaningful
tradeoff behavior," which means nothing, and it never puts the 0.19 base rate next to it, so a
reader cannot tell that 0.33 is well above chance. The last sentence is pure filler.

---

## V1: role assignment

**Technique:** role assignment.

**Prompt**

> You are a machine learning engineer writing the notebook cell that a skeptical reviewer will
> read before they read your code. You care more about not being wrong than about sounding
> impressive.
>
> Write a summary of these results.
> [same metrics]

**Output, excerpt**

> Under GroupKFold on client_id, ROC AUC is 0.71. The previous random-split figure of 0.84 is
> not comparable: random folds allowed the same client to appear in both training and
> validation, so part of that score reflects client recognition rather than generalization.
> PR AUC is 0.33. Model performance should be judged against the base rate rather than in
> absolute terms.

**What changed in the prompt.** One role sentence, nothing else.

**What actually changed in the output.** "Strong performance" disappeared and the framing
flipped: the 0.84 went from a benchmark the model fell short of to a number that was never
valid. That is the correct reading and the naive version had it backwards. The role also cut
the closing filler sentence entirely.

**What still failed.** It said to judge PR AUC against the base rate and then did not do it,
even though 0.19 was sitting in the input. It also did not explain what GroupKFold is doing,
so the paragraph only works for a reader who already knows.

**Next.** Tell it who is reading and why the writeup exists.

---

## V2: context and motivation

**Technique:** context and motivation.

**Prompt**

> You are an ML engineer writing the notebook cell a skeptical reviewer reads before the code.
> You care more about not being wrong than about sounding impressive.
>
> Context: this notebook is public and gets graded. The reader is a data lead who has seen a
> lot of inflated notebook metrics and is specifically checking whether my evaluation is
> honest. Any number I quote has to be traceable to the run that produced it, and any
> precision-style number has to appear next to its base rate or the reader will assume I am
> hiding it. Negative results count as results here. If the honest number is worse than the
> old number, saying so plainly is the point of the cell.
>
> Write the summary.
> [same metrics]

**Output, excerpt**

> Switching from random 5-fold to GroupKFold on client_id dropped ROC AUC from 0.84 to 0.71.
> The drop is the result, not a regression. Random folds split a single client's months across
> train and validation, so the earlier score partly measured the model's ability to recognize
> clients it had already seen. The grouped number is the one that estimates performance on a
> client the model has never met.
>
> PR AUC is 0.33 against a base rate of 0.19, so precision is roughly 1.7x better than
> guessing at the same recall. That is a real but modest lift, and on 1,870 positives across
> 412 clients it is not a number I would bet a production decision on without a holdout month.

**What changed in the prompt.** Who reads it, why, and what the standard is.

**What actually changed in the output.** It finally did the base rate comparison instead of
recommending it, and it gave the ratio, which is the part a reader can sanity check. "The drop
is the result, not a regression" is a sentence I would actually write. It also added its own
caveat about the holdout month, which nothing asked for and which is correct.

The motivation half of the layer did more work than the context half. Telling it the reader is
a data lead changed the vocabulary. Telling it the reader is specifically hunting for inflated
metrics changed the argument.

**What still failed.** The voice is close but not mine. "Roughly 1.7x better than guessing"
is a phrase I would not say, and "bet a production decision" is a little dramatic. It also
varies its structure run to run, so two consecutive cells in the same notebook do not look
like they came from the same person.

**Next.** Show it two of my own writeups.

---

## V3: few-shot examples

**Technique:** few-shot examples.

**Prompt**

V2 plus two real writeups I had already written by hand, pasted in full as examples of the
target voice, with their input metrics above each so the mapping is visible.

**Output, excerpt**

> GroupKFold on client_id, five folds, months 2024-03 through 2025-02. ROC AUC 0.71. The
> random-split run gave 0.84 and that number is not a fair comparison: random folds put the
> same client on both sides of the wall, so it was scoring recognition as well as prediction.
> I am keeping both numbers visible because the gap is itself the finding. A large gap means
> the client effect is large.
>
> PR AUC 0.33, base rate 0.19. Above chance, not by a lot. 412 clients, 9,840 rows, 1,870
> positives.

**What changed in the prompt.** Two worked examples of my own writing.

**What actually changed in the output.** Sentence length dropped and the numbers moved to the
front of the clauses, which is how I actually write. "The gap is itself the finding" came from
my examples and is the framing I want. It stopped explaining concepts to me and started
recording facts, because my examples do not explain concepts. Consecutive cells now look like
one author.

Worth noting against my Week 2 prompt-ladder result, where few-shot examples clearly hurt.
That task was exploratory and I wanted the model to find something I had missed, so examples
narrowed the search and cost me. Here the task is voice and format on content I already know,
which is the case where examples are the right tool. Same technique, opposite outcome, and the
difference is whether I am asking for discovery or for imitation.

**What still failed.** It dropped things. The V2 version had a caveat about needing a holdout
month, and this one has no caveat at all, because neither of my two examples happened to have
one. The examples set the ceiling as well as the floor.

**Next.** Name the sections explicitly so nothing can silently go missing.

---

## V4: output structure

**Technique:** output structure.

**Prompt**

V3 plus:

> Structure. Four labeled parts in this order, no extras, no headings beyond these:
>
> What changed: one sentence on what differs from the previous run.
> What came out: the numbers, each with the split or population it came from.
> What it means: at most three sentences of interpretation. Every precision-style figure gets
> its base rate in the same sentence.
> What I would not claim from this: at least one sentence. If you genuinely cannot find a
> limitation, write "none identified" and I will treat that as a bug in the prompt.
>
> Prefill: begin your response with "What changed:" and nothing before it.

**Output, excerpt**

> What changed: the split moved from random 5-fold to GroupKFold on client_id, same feature
> set and same model.
>
> What came out: ROC AUC 0.71 under GroupKFold(5), 412 clients, 9,840 rows, 1,870 positives,
> months 2024-03 to 2025-02. The prior random-split run gave 0.84 on the same rows.
>
> What it means: the 0.13 gap is a client effect, not a model regression, because random folds
> let a client's own months train the fold that scores them. PR AUC 0.33 against a base rate
> of 0.19 is above chance and modest. The grouped figure is the one to quote.
>
> What I would not claim from this: this is cross-validation, not a held-out future month, so
> it says nothing about whether the model survives a time shift. Client count is 412 and I
> have not checked whether a handful of large clients dominate the folds.

**What changed in the prompt.** A fixed four-part structure with a named slot for limitations,
plus a prefill.

**What actually changed in the output.** The caveats came back and got better, because the
structure made their absence visible. Making "what I would not claim" a required slot with an
explicit escape hatch is what did it: the model would rather fill the slot than write "none
identified" under a line saying I will treat that as a bug. The fold-concentration point is a
real gap in my evaluation that I had not thought about, and it came out of a slot I created
purely as a formality.

The prefill removed the last of the preamble on the first try.

**What still failed.** It still claims the 0.13 gap is a client effect. That is my hypothesis
and it is probably right, but nothing in this run tested it. The output is stating my
assumption as a conclusion in a document whose whole point is not doing that.

**Next.** Force the reasoning apart from the conclusion so I can see which claims are derived
and which are assumed.

---

## V5: step decomposition

**Technique:** step decomposition.

**Prompt**

V4 plus a working section before the answer:

> Work through these steps in a section titled "working" before the four-part answer. Keep it
> short, it is for me, not for the reader of the notebook.
>
> 1. List every number I gave you and, for each, name the run and split it came from. If I did
>    not tell you, write "source not given."
> 2. List every claim you are about to make. Mark each one derived (it follows from the numbers
>    in step 1) or assumed (it is a plausible explanation that this run did not test).
> 3. Any claim marked assumed must appear in the final text with hedging language, or move to
>    "what I would not claim." Never present an assumed claim as derived.
>
> Then write the four-part answer.

**Output, excerpt**

> working
>
> 1. 0.71 roc_auc, grouped-cv-v3, GroupKFold(5) on client_id. 0.84 roc_auc, previous run,
>    random 5-fold, source given as "was". 0.33 pr_auc, grouped-cv-v3, split not separately
>    stated, assuming same. 0.19 base rate, population not stated, assuming all 9,840 rows.
> 2. Claims: the grouped number is the honest one (derived, follows from the split
>    definitions). The gap is caused by client recognition (assumed, no ablation was run). PR
>    AUC exceeds base rate (derived). The model would not survive a time shift (assumed, not
>    tested either way).
> 3. Claim 2 gets hedged. Claim 4 moves to what I would not claim.
>
> What changed: the split moved from random 5-fold to GroupKFold on client_id, feature set and
> model unchanged.
>
> What came out: ROC AUC 0.71 under GroupKFold(5) on 412 clients, 9,840 rows, 1,870 positives,
> 2024-03 to 2025-02. The earlier random-split run on the same rows gave 0.84. PR AUC 0.33,
> base rate 0.19 over the same 9,840 rows.
>
> What it means: the 0.13 gap is most likely a client effect, since random folds let a client's
> own months train the fold that scores it, but this run did not test that and an ablation
> would be needed to say so. PR AUC 0.33 against a 0.19 base rate is above chance and modest.
> The grouped figure is the one to quote.
>
> What I would not claim from this: that the model holds under a time shift, since this is
> cross-validation and not a held-out future month. That the client effect is the only cause of
> the gap. That the 0.19 base rate applies to any subpopulation, since I computed it over all
> rows and have not checked it by client size.

**What changed in the prompt.** A visible working section that separates sourcing, claim
classification, and hedging into three steps before any prose is written.

**What actually changed in the output.** Step 1 caught something I had not noticed in my own
input: I never said which split the PR AUC came from, and I never said what population the base
rate was over. Both are real holes in how I record runs, and every earlier version had silently
papered over them with a confident sentence.

Step 2 is what fixed the V4 problem. "Most likely a client effect, but this run did not test
that" is the honest version, and it got there mechanically rather than by luck.

**What still failed.** It costs tokens and time. For a routine cell where nothing surprising
happened, running the full working section is more ceremony than the cell deserves. In
practice I run V5 for any result I plan to quote outside the notebook and V4 for the rest.

---

## Cross-model comparison

Same V5 prompt, same input, run once on Claude and once on ChatGPT. What differed, specifically.

**Sourcing step.** Claude wrote "source not given" twice, on the PR AUC split and the base rate
population. ChatGPT filled both in as "GroupKFold(5), all rows" without flagging that I had not
said so. It guessed correctly, which is worse than guessing wrong, because a correct guess
trains me to stop checking. This was the largest single difference and it is the reason I run
this task on Claude by default.

**Claim classification.** Both classified the client-effect claim as assumed. ChatGPT then
hedged it in the prose more weakly, "likely reflects a client effect," while Claude carried the
"this run did not test that" clause into the sentence. Same classification, different follow
through.

**Tone.** ChatGPT's prose is smoother and I like reading it more. It also drifts upward: it
described 0.33 PR AUC as "solid separation," which is the kind of phrase this whole prompt
exists to prevent. Claude's prose is flatter and occasionally clipped to the point of being
terse, which fits a notebook cell better than it would fit a blog post.

**Structure.** ChatGPT added a fifth section, "Next steps," which I did not ask for and had
explicitly forbidden with "no extras." It did this on two of three runs. Claude kept to four
parts every time. On the other hand ChatGPT's tables, when I asked for one in a side test, were
cleaner.

**Failure points.** Claude's failure mode is going too short and dropping context a reader
needs, for example writing "the gap" without restating what the gap is between. ChatGPT's
failure mode is adding an unrequested optimistic sentence at the end. Both are predictable,
which means both are manageable, but they need opposite corrections: Claude needs the reader
described more fully, ChatGPT needs a harder ban on closing statements.

**What I actually do.** Claude for the writeup, because sourcing discipline is the thing I am
buying. If I need the same content as prose for a non-technical reader, I take Claude's version
and ask ChatGPT to rewrite it without changing any number, then diff the numbers to confirm it
did not.

---

## Final reusable template

No personal context in it. Fill the brackets.

```
SYSTEM
You are a [practitioner role] writing [the artifact] that a skeptical reviewer reads
before they see the underlying work. You care more about not being wrong than about
sounding impressive.

CONTEXT
This [artifact] is [public / graded / sent to a client / reviewed by peers]. The reader is
[who they are and what they have seen too much of]. Every figure must be traceable to the
run that produced it. Any precision-style figure must appear in the same sentence as its
base rate or denominator. Negative results are results: if the honest number is worse than
the previous number, say so plainly, that is the point.

INPUT
[the raw numbers or facts, with the run, split, and population each came from]
[what changed since the previous version]

WORKING (write this first, in a section titled "working", keep it short, it is for me)
1. List every number I gave you and name the run, split, and population it came from.
   If I did not tell you, write "source not given". Do not fill the gap yourself.
2. List every claim you are about to make. Mark each derived (follows from step 1) or
   assumed (a plausible explanation this work did not test).
3. Every assumed claim must either carry hedging language naming what was not tested, or
   move into the limitations section. Never present an assumed claim as derived.

OUTPUT
Four labeled parts, this order, no extras, no other headings:
What changed: one sentence.
What came out: the figures, each with its source.
What it means: at most three sentences.
What I would not claim from this: at least one sentence. If you genuinely cannot find a
limitation, write "none identified" and I will treat that as a bug in this prompt.

STYLE
[two to six words for the voice you want]
Do not add a closing or next-steps section.

Begin your response with "working" and nothing before it.
```

Optional sixth block, for when the voice matters more than the discovery: paste two examples
of your own finished writeups above the input. Add it for tone and format. Leave it out when
you want the model to surface something you have not already thought of, because examples pull
the answer toward their own shape and quietly delete any category they do not contain.

**Reuse check.** I gave the template to someone whose work I know nothing about, filled for a
marketing report on campaign results rather than an ML run. The working section caught that
their conversion figure had no denominator attached and wrote "source not given" instead of
inventing one, which is the behavior the template exists for.
