# Eval results

Six cases, run after the build was working. Pass or fail, no partial credit. Ground truth was
written and verified before any of this ran, in `ground-truth.md`.

**Score: 5 of 6.**

| Case | What was planted | Result |
|---|---|---|
| 1 | the renamed label pair from M+1 | **pass** |
| 2 | nothing | **pass** |
| 3 | a direct transform of the label | **pass** |
| 4 | a sentinel zero, no leakage | **pass**, but the case is broken |
| 5 | an outcome-driven population filter | **fail** |
| 6 | a backfilled column with an innocent name | **pass**, for the wrong reason |

## Case 1, pass

Found the pair at 1.0000 agreement against a majority-class baseline of 0.7076, and named both
halves. The strongest single-column correlation in the file is 0.151, so nothing in a
column-by-column pass would have raised it. Full report in `reports/case1_pair.md`.

## Case 2, pass, and this is the one I cared about

No leakage reported and nothing invented. Every pair in the file scores 0.6966 agreement against
a baseline of 0.6966, so the entire table comes out at exactly zero over baseline.

This case nearly failed, and not because of the agent. See the build log: before I added the
baseline column, the top pair in this clean file printed as `0.6966`, which reads like a finding
if you do not know that guessing the majority class scores the same. I built the number that
makes a clean file look clean.

## Case 3, pass

`risk_score` correlates with the label at 1.0000. Found immediately. This case exists to catch
total failure and it did its job by not being interesting.

## Case 4, pass, but the case is broken

The sentinel in `avg_position` was flagged: 96 zeros over 10.0% of rows with a smallest non-zero
value of 3.01, so the zeros sit apart from the distribution rather than inside it.

The problem is that `avg_position` comes from the shared base panel, so those zeros are in all
six datasets and get flagged in all six. Case 4 is supposed to test whether the auditor notices
a correctness problem it was not asked about. It cannot test that, because there is no case
where the sentinel is absent. The pass is real and the case is worthless, and I would rather say
that than count it.

Fix, not done: regenerate case 4 as the only file with the sentinel and strip the zeros from the
other five.

## Case 5, fail

Nothing leaks in the columns, and rows were kept only where `total_queries` at M+1 reached 150.
Correct answer: no leaking columns, plus a disclosure that the row set was selected on the
outcome window.

The population test I designed for exactly this returned `corr_rows_vs_label_rate = 0.0309`,
which is lower than the same number on the unfiltered file, 0.1374. The detector I wrote for
this case points the wrong way on it.

Two signals do survive. Completeness drops to 77.4% from 81.9%, and rows per client run 3 to 10
instead of 7 to 11. Comparing against the clean file, `total_queries` has a minimum of 133 rather
than 27, which is a truncated distribution and a real tell.

That is enough to say **a filter was applied**. It is not enough to say the filter read the
outcome window, and that distinction is the entire case. Worse, the min-of-133 tell only exists
because I had the unfiltered file next to it. An auditor holding this file alone sees 133 and has
nothing to compare it to.

I am scoring this a fail rather than a partial. The honest conclusion is that outcome-driven
population filtering is not detectable from the filtered file on its own, which is a limitation
of the approach rather than a bug I can fix by tuning a number. The instruction that follows
from it is to always ask for the unfiltered row set, and to treat step 4 as a question for the
user rather than a check the agent can close.

## Case 6, pass, for a reason I did not intend

`content_quality_index` was written from the M+1 ratio. The agent flagged it, so the case passes.

It passes because the column correlates with the label at -0.611 in a file where nothing else
exceeds 0.06. That gap is loud enough that the innocent name never mattered.

I wrote in the spec that I expected this case to fail and wanted to see whether it failed
honestly. It did not fail, because I made the backfill too strong when I generated the data.
The case as built tests "does the agent notice an implausibly predictive column", which it does.
It does not test what I meant it to test, which is a backfilled column that is only mildly
predictive and therefore looks like an ordinary good feature.

Fix, not done: regenerate with the correlation dialled down to around 0.2, in the range where a
real feature would live.

## What the suite says overall

The pair check works and is the reason to have built this. It found in seconds a class of leak
that took me three weeks by hand, and it separates cleanly from a clean file once the baseline
is on the page.

Column-level leakage is handled. Population-level leakage is not, and pretending otherwise would
be the exact failure this agent exists to prevent.

Two of the six cases do not test what I designed them to test. I found that by running them,
which is the argument for writing eval cases you can actually score rather than a list of things
you hope the agent does.
