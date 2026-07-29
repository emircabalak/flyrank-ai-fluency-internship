# The Prompt Ladder

Emir Cabalak, General AI Fluency track, Week 2
Assignment code CUSTOM-MRBSNHWC-B3701520

Six runs: one weak baseline plus five versions. Each version adds exactly one layer, chosen to
attack whatever was worst about the previous output. Outputs are shown as representative
excerpts, not in full, because the baseline alone ran past a thousand words of nothing.

The task behind all six runs is real. I have a monthly panel of client search data from the ML
track and I need to decide which columns are safe to use as features for a visibility-drop
label. Every version is trying to get useful help with that.

## Ladder at a glance

| Version | Layer added | Verdict |
|---|---|---|
| Baseline | none | useless, as expected |
| V1 | a clearer goal | first real improvement |
| V2 | real context | biggest single jump |
| V3 | a specified output format | small, but made it checkable |
| V4 | examples of what good looks like | made it worse |
| V5 | verification requirements | recovered and beat V3 |

---

## Baseline

**Prompt**

> Explain this data.

**Output, excerpt**

> Data analysis is a broad field with many approaches depending on your goals. To explain your
> data effectively, you should start by understanding its structure: the number of rows and
> columns, the data types present, and whether there are missing values. Common first steps
> include computing summary statistics such as mean, median, and standard deviation for
> numeric columns, and value counts for categorical ones. Visualization is also valuable.
> Histograms reveal distributions, scatter plots reveal relationships, and correlation
> matrices can surface potential dependencies between variables. If you can share more about
> your dataset, I can give more specific guidance.

Nine hundred more words in the same register. It never asked me a question and it never
mentioned that I had not attached any data, which is the part that surprised me.

---

## V1: a clearer goal

**Prompt**

> I have a monthly panel of client search data. I want to decide which columns are safe to use
> as features for a model that predicts whether a client's visibility will drop next month.
> Tell me how to decide that.

**Output, excerpt**

> To determine feature safety, the central concern is data leakage: features that contain
> information unavailable at prediction time. Work through your columns and ask, for each one,
> whether its value would have been known before the prediction window opens. Columns derived
> from the target, computed after the fact, or aggregated over a period that includes the
> target month should be excluded. A practical approach is to build a data dictionary that
> records, for every column, when it is computed and from what source. You should also
> consider whether train and test are split in a way that respects time ordering.

**What changed in the prompt.** A goal. The baseline had no task at all, this one names the
decision I am trying to make.

**What actually improved in the output.** It stopped teaching me what a histogram is and went
straight to leakage, which is the correct concept for the question. It also volunteered the
train/test ordering point, which I had not asked about and which is right.

**What still failed.** Every sentence was true of any panel dataset. It could not tell me
whether my `avg_position` column is safe because it did not know I had one. The advice
"exclude columns derived from the target" is exactly the sentence that fails on my real
problem, where the dangerous columns are not derived from the target individually.

**What I would try next.** Give it the actual columns and the actual label definition.

---

## V2: real context

**Prompt**

> I have a monthly panel of client search data. Grain is one row per client per month. Columns
> include `impressions`, `clicks`, `ctr_x100`, `avg_position`, `queries_with_data`,
> `total_queries`, `gsc_data_start`, and `is_ai_referral_available`.
>
> The label is: visibility dropped next month, defined as `queries_with_data / total_queries`
> falling below 0.6 in month M+1. I build features from months up to and including M.
>
> Notes on the data: rate columns are stored as percentages times 100, `avg_position == 0`
> means no data rather than rank zero, and availability flags can be NULL as well as true or
> false.
>
> I want to decide which columns are safe to use as features. Tell me how to decide that.

**Output, excerpt**

> Your label is a threshold on the ratio `queries_with_data / total_queries` at M+1. Both
> components of that ratio appear in your column list. If either is available at M+1 in your
> feature build, the label is trivially reconstructable. Confirm that your feature window
> closes at M with no bleed.
>
> Beyond the direct case, the pair is the risk: `queries_with_data` and `total_queries` are
> individually defensible as month-M features, but if any derived column combines them across
> a window that touches M+1, the ratio is rebuilt. Treat leakage as a property of the time
> window, not of a column name.
>
> Two data notes affect correctness rather than leakage. `avg_position == 0` as a missing
> marker means any mean over that column is biased toward zero unless you mask it first. NULL
> availability flags mean a filter written as `= FALSE` silently drops the NULL rows; use
> `IS NOT TRUE` if you want them.

**What changed in the prompt.** Real context: the grain, the column names, the label
definition, and the three data quirks.

**What actually improved in the output.** It found the numerator and denominator pair on its
own and said the sentence I most needed, that leakage is a window property rather than a
column blacklist. It also caught the `avg_position == 0` bias and the NULL filter bug, neither
of which I had asked about. This was the biggest jump on the whole ladder and it was not close.

**What still failed.** The answer was one long block of prose. I had to reread it three times
to pull out which columns were actually cleared and which were not. There was no verdict per
column, so I could not act on it directly.

**What I would try next.** Force it into a table with one row per column.

---

## V3: a specified output format

**Prompt**

Same as V2, with this appended:

> Answer as a markdown table with one row per column and these headers: `column`, `verdict`
> (safe, unsafe, or conditional), `reason`, `condition if conditional`. After the table, add
> at most three sentences on anything the table cannot express. No preamble.

**Output, excerpt**

> | column | verdict | reason | condition if conditional |
> |---|---|---|---|
> | `impressions` | safe | observed at M, no overlap with M+1 | |
> | `clicks` | safe | observed at M | |
> | `ctr_x100` | safe | ratio of two month-M quantities | remember the x100 scale |
> | `avg_position` | conditional | 0 encodes missing | mask zeros before any aggregation |
> | `queries_with_data` | conditional | numerator of the label ratio | only from months up to M, never M+1 |
> | `total_queries` | conditional | denominator of the label ratio | only from months up to M, never M+1 |
> | `gsc_data_start` | safe | static per client | |
> | `is_ai_referral_available` | conditional | NULL is a third state | filter with IS TRUE, do not use = FALSE |
>
> The table cannot express the pair rule: the two conditional ratio components are only
> dangerous together, so a derived column that combines them needs the same window check.

**What changed in the prompt.** An output format, plus a hard "no preamble."

**What actually improved in the output.** I could act on it. Every column got a verdict I
could argue with, which is the point, because a wrong cell is visible and a wrong paragraph is
not. The "no preamble" line also killed the two sentences of throat clearing that had opened
every previous run.

**What still failed.** The verdicts were confident and unsourced. `gsc_data_start` got marked
safe with no caveat, but in my data it varies a lot by client and shrinks the usable set once
you filter on it. The table made a shaky answer look settled, which is worse than a shaky
paragraph.

**What I would try next.** Show it what a good answer looks like.

---

## V4: examples of what good looks like

This is the version that made things worse.

**Prompt**

Same as V3, with two worked example rows added before the request:

> Here are two rows from a good version of this table on a different dataset, so you can see
> the level of reasoning I want:
>
> | `refund_amount` | unsafe | written during the outcome window, so it encodes the outcome | |
> | `signup_channel` | safe | fixed at account creation, cannot change after | |

**Output, excerpt**

> | `impressions` | safe | fixed at collection time, cannot change after | |
> | `clicks` | safe | fixed at collection time, cannot change after | |
> | `ctr_x100` | safe | fixed at collection time, cannot change after | |
> | `avg_position` | safe | fixed at collection time, cannot change after | |
> | `queries_with_data` | unsafe | written during the outcome window, so it encodes the outcome | |
> | `total_queries` | safe | fixed at collection time, cannot change after | |

**What changed in the prompt.** Two examples of a good row.

**What actually improved in the output.** Honestly, nothing. Formatting consistency, maybe.

**What made it worse.** It copied the reasoning of my examples instead of doing its own. Five
of eight columns got the identical phrase "fixed at collection time, cannot change after,"
including `avg_position`, which V3 had correctly flagged for the zero-as-missing problem. The
`conditional` verdict disappeared entirely, because neither of my examples used it, so the
whole middle category vanished from the model's answer. Worst of all it marked
`queries_with_data` unsafe and `total_queries` safe, which splits the pair and misses the
actual risk. My two examples came from a dataset where the danger was one column, so it went
looking for one column here too.

This is the moment on the ladder where I learned the most. Examples do not just show quality,
they narrow the search. On a task where I already knew the shape of the answer that would be
fine. On this task I was hoping the model would find something I had missed, and examples are
exactly the wrong tool for that.

**What I would try next.** Drop the examples. Add a requirement that it check its own work
instead of imitating mine.

---

## V5: verification requirements

**Prompt**

V3 plus a verification block, no examples:

> Before you answer, do this and show it:
>
> 1. Restate the label definition in your own words and name every column that appears in it.
> 2. For each column you mark `safe`, name one scenario in which it would actually be unsafe.
>    If you cannot construct one, say so.
> 3. After the table, list any column where your confidence is low and say what you would need
>    to check in the data to resolve it.
>
> Do not guess a value you cannot derive from what I gave you. Say "not determinable from the
> given information" instead.

**Output, excerpt**

> Label restated: for client c, the label at month M is true when, at month M+1, the ratio of
> `queries_with_data` to `total_queries` is under 0.6. Columns appearing in the label:
> `queries_with_data`, `total_queries`.
>
> [table as in V3, with `gsc_data_start` changed from safe to conditional]
>
> Counter-scenarios for safe verdicts. `impressions` becomes unsafe if any upstream job
> backfills month M after M+1 closes, which I cannot verify from what you gave me.
> `clicks` has the same exposure. `ctr_x100` is safe only if it is computed from month-M
> impressions and clicks rather than restated later.
>
> Low confidence. `gsc_data_start`: I marked it conditional rather than safe because you told
> me client history depth varies. Whether it is safe depends on whether you filter on it, and
> filtering on it changes which clients are in the population, which is a population choice and
> not a leakage question. Not determinable from the given information.

**What changed in the prompt.** Verification requirements: restate the label, argue against
your own safe verdicts, flag low confidence, and refuse to guess.

**What actually improved in the output.** The counter-scenario step is what earned the layer.
Asking it to attack its own "safe" verdicts produced the backfill scenario, which is a real
failure mode in our warehouse and which nothing else on the ladder surfaced. It also self
corrected `gsc_data_start` from safe to conditional, the exact cell that was wrong in V3, and
it did so because it was forced to justify the verdict rather than just state it. The
"not determinable" instruction stopped it inventing a population rule.

**What still failed.** It is now long. The verification section is roughly the same length as
the answer, which is fine when I am auditing features and annoying when I am not. It also
still cannot see my actual data, so half the low-confidence items resolve to "go look," which
is correct but is work it handed back to me.

**What I would try next.** Give it a sample of rows so the low-confidence items can be
resolved instead of listed.

---

## What the ladder actually taught me

Context did the heavy lifting. V2 was the only step where the answer changed category rather
than degree, and everything after it was refinement. If I could keep one layer, it is that one.

Format is cheap and worth it. It converts a vague answer into a set of specific claims that
can be individually wrong, which is what makes review possible.

Examples backfired on an exploratory task. They pulled the answer toward the shape of the
example instead of the shape of the problem, and they silently deleted a whole verdict
category. I would still use examples for a formatting or tone task. Not for a task where I want
to be told something I did not already know.

Verification was the second best layer and the one I nearly skipped, because on paper it looks
like politeness. Asking a model to argue against its own answer is not politeness, it is the
only step that changed a wrong cell into a right one.

---

## Final prompt

Cleaned up so someone else on the track can use it. Replace the bracketed parts. No examples
layer, because it made things worse.

```
I need to decide which columns in a dataset are safe to use as model features, given a
label defined over a future window.

DATA
Grain: [one row per X per Y].
Columns: [list every column name, with its type if not obvious].
Data quirks you must respect: [scale encodings, sentinel values that mean missing,
columns that can be NULL as well as true/false, anything else that would fool a naive read].

LABEL
[Definition in one sentence, including the exact time window it is computed over.]
Features are built from [window] and must not use anything from [outcome window].

TASK
Give a verdict on every column.

BEFORE YOU ANSWER
1. Restate the label definition in your own words and name every column that appears in it.
2. Name any pair or group of columns that is individually safe but together reconstructs
   the label or its threshold.
3. For each column you mark safe, name one scenario in which it would actually be unsafe.
   If you cannot construct one, say so.

OUTPUT
A markdown table, one row per column, headers: column | verdict (safe / unsafe /
conditional) | reason | condition if conditional.
Then, at most three sentences on anything the table cannot express.
Then a short list of columns where your confidence is low and what I would have to check
in the data to resolve each one.
No preamble.

RULES
Do not guess a value you cannot derive from what I gave you. Write "not determinable from
the given information" instead.
Treat leakage as a property of the time window, not of a column name.
```

Tested on a second dataset I did not design the prompt around, a support-ticket table with a
"resolved within SLA" label. It found the created-at and resolved-at pair without being told
to look for a pair, and it flagged the assignee column as conditional because reassignment can
happen after the outcome. Both were right. That is the check that it works without me in the
room.
