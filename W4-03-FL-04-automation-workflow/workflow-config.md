# Study-notes pipeline: the configuration

This is the workflow itself, separated from the walkthrough so it can be copied and run. Four
steps. Every prompt below is the exact text in use.

## Step 0: the Claude Project standing instructions

Pasted once into the project's custom instructions. Every step inherits it.

```
You are helping me build source-grounded study notes on machine learning methodology.

RULES THAT ALWAYS APPLY
Never state anything as coming from the source unless it is in the text I gave you. If
you know something is true from general knowledge but it is not in this source, mark it
[outside source] and keep it in a separate section.
Never invent a page number, section number, equation number, or quotation. If you cannot
locate it, write "location not found in provided text".
Quote at most 15 words at a time, in quotation marks.
When the source hedges, keep the hedge. "Often" does not become "always" and "can" does
not become "does".
If two parts of the source appear to contradict each other, say so instead of picking one.

VOICE
Direct, plain, technical, no buzzwords. Short paragraphs. No em dashes. Say the thing
once. Assume I already know basic ML. Do not define train/test split for me.
```

## Step 1: gather (NotebookLM)

No prompt. Configuration only.

One NotebookLM notebook per source. The PDF or the saved page goes in as the single source,
and nothing else, because a notebook with five sources produces answers blended across all of
them and I lose the ability to say which one a claim came from.

The only thing done in NotebookLM is asking it for the source's own structure:

```
List the sections of this document in order, with one line each on what that section
claims. Use only this document. If a section makes no claim and is only setup, say so.
```

The output of step 1 is that outline plus the source text itself. Both go to step 2.

## Step 2: synthesize (Claude Project)

```
Here is a source and its section outline.

[outline from step 1]
[source text]

Produce a claim ledger. One row per claim the source actually makes, in the order it
makes them.

| # | claim, in your words, one sentence | where in the source | strength |

Strength is one of: stated (the source asserts it directly), supported (the source
asserts it and shows evidence for it in this document), or implied (I would be reading
it in).

Rules for this step:
Only claims about method. Skip claims about the authors' own experimental results
unless the method conclusion depends on them.
Do not merge two claims into one row because they are related.
Do not add a claim you know to be true from elsewhere. That belongs in step 3.
If the source states something I would find surprising, keep it, do not smooth it.

No preamble. Begin your response with the table header.
```

## Step 3: critique (Claude Project, new conversation)

Deliberately a fresh conversation with the source pasted again. If it runs in the same thread
it audits its own summary while still holding the reasoning that produced it, and it passes
everything.

```
Here is a source and a claim ledger somebody else produced from it. Audit the ledger.
Assume it contains errors, because it does.

[source text]
[ledger from step 2]

For every row, return a verdict:
SUPPORTED   the source says this
OVERSTATED  the source says something weaker, quote the weaker version
MISSING     this is not in the source at all
GARBLED     the source says something related but this row gets it wrong

Then, separately:
NOT CAPTURED  claims the source makes that the ledger left out. This is the most
              important part of your answer. Look hardest here.
HEDGE CHECK   any row where the source hedged and the ledger did not.

Do not be generous. A row that is roughly right is OVERSTATED, not SUPPORTED.
```

## Step 4: format (Claude Project, same conversation as step 3)

```
Using only the SUPPORTED rows and the corrected versions of the OVERSTATED and GARBLED
rows, produce two things.

First, notebook markdown. Three to six short paragraphs I could paste above a code cell.
Plain words. No headings. Every method claim carries its source in brackets like
[Kaufman 2012, sec 3].

Second, recall cards. One line per card, format:
Q: [question] || A: [answer, under 25 words] || SRC: [where in the source]
Only make a card for something I would actually need to recall while working. No
definitions of things I already know.

Anything from the NOT CAPTURED list that I should learn goes into both, marked the same
way. Anything marked [outside source] anywhere gets dropped entirely at this step.
```

## Handoffs

| From | To | What is passed | Format |
|---|---|---|---|
| 1 | 2 | section outline plus source text | plain text |
| 2 | 3 | the claim ledger | markdown table |
| 3 | 4 | verdicts plus the not-captured list | markdown |
| 4 | out | notebook markdown, recall cards | markdown |

Step 3 is the only handoff that crosses a conversation boundary, and that boundary is the
point.
