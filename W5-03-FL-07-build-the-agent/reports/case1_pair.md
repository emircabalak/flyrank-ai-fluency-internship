# Leakage audit: case1_pair.csv

961 rows, 13 columns. Label: `label_visibility_drop`.

## Step 1: the label, restated

At month M the label is true when, at month M+1, the ratio of `queries_with_data` to
`total_queries` falls below 0.6.

Columns appearing in the label: **`queries_with_data`** and **`total_queries`**. Both appear
inside the ratio rather than in the final expression, which is why a check that only reads the
label's name would miss them.

## Step 2: what could only be known later

`month` and `gsc_data_start` are fixed at or before M. `client_id` is an identifier.

`tracked_terms_returning` and `term_universe_size` are the two I cannot place. Nothing in their
names says when they were computed, and there is no data dictionary in the folder. Step 3
answers it a different way.

For every other column, whether the value was written during the outcome window is **not
determinable from the data provided**. It is a question about the pipeline, not about the file.

## Step 3: the pair

Single-column signal first. The strongest correlation with the label of any column is
`tracked_terms_returning` at **-0.151**, and everything else sits under 0.06. Read on its own,
this table says the file is clean.

Then every ordered pair, tested as a ratio against the 0.6 threshold. Guessing the majority
class scores 0.7076 here, so that is the number to beat.

| numerator | denominator | agreement | over baseline |
|---|---|---|---|
| `tracked_terms_returning` | `term_universe_size` | **1.0000** | **+0.2924** |
| `tracked_terms_returning` | `total_queries` | 0.8356 | +0.1280 |
| `tracked_terms_returning` | `queries_with_data` | 0.7846 | +0.0770 |
| `total_queries` | `queries_with_data` | 0.7076 | +0.0000 |

The first row reproduces the label on all 961 rows. Not approximately. Exactly.

So `tracked_terms_returning` is the numerator of the label ratio and `term_universe_size` is the
denominator, both taken from month M+1 and renamed. A model given these two is not predicting
the drop, it is reading it.

The second and third rows are the same leak partially expressed: one leaking column paired with
a clean one still carries most of the signal.

This is the whole reason the pair check exists. The strongest single-column correlation in this
file is 0.151, which nobody would investigate.

## Step 4: population

120 clients, 10 distinct months, 961 rows against 1200 if the panel were rectangular, so 80.1%
complete. Rows per client range from 6 to 10.

The correlation between a client's row count and its label rate is 0.1757, which is mild and
consistent with clients starting at different months rather than with a filter that reads the
outcome. Nothing here looks like an outcome-driven population filter, but this test is weak and
I would not stake much on it.

## Verdicts

| column | verdict | reason | condition if conditional |
|---|---|---|---|
| `client_id` | conditional | an identifier, not a feature; carries client-level label rate spread of 0.667 | drop it, or use it only as a grouping key for the split |
| `month` | conditional | a time index, usable as a feature only if the model will see the same months in production | never one-hot it across the train and test boundary |
| `total_queries` | conditional | the denominator of the label ratio | only from months up to and including M, never M+1 |
| `queries_with_data` | conditional | the numerator of the label ratio | only from months up to and including M, never M+1 |
| `impressions` | safe | observed at M, no overlap with the outcome window | |
| `clicks` | safe | observed at M | |
| `ctr_x100` | safe | a ratio of two month-M quantities; note the values run to 1721, so the scale is x100 of a percentage and not a fraction | |
| `avg_position` | conditional | 96 zeros, 10.0% of rows, and the smallest non-zero value is 3.01. A rank of exactly zero next to a floor of 3.01 is a missing marker, not a rank | mask the zeros before any mean, or treat them as a separate category |
| `gsc_data_start` | safe | static per client, fixed before the window | |
| `is_ai_referral_available` | conditional | true, false **and** null, 217 nulls | filter with `IS TRUE`; a filter written `= FALSE` will silently drop 217 rows |
| `tracked_terms_returning` | **unsafe** | the label ratio numerator from M+1, renamed | |
| `term_universe_size` | **unsafe** | the label ratio denominator from M+1, renamed | |

### Counter-scenarios for every safe verdict

`impressions` becomes unsafe if any upstream job backfills month M after M+1 closes. I cannot
verify that from the file.

`clicks` has the same exposure, from the same job.

`ctr_x100` is safe only if it was computed from month-M impressions and clicks at the time. If
it is ever restated later from corrected figures, it inherits the outcome window.

`gsc_data_start` becomes unsafe the moment it is used to filter rows rather than as a feature,
because filtering on history depth changes which clients are in the population.

## The rule

> No feature may be computed from any window that overlaps the outcome window, whatever the
> column is called and whatever table it lives in. This applies to combinations as well as to
> single columns: if two individually legal columns together reconstruct the label or the
> quantity it is thresholded from, the pair is a leak even though neither half is.

Written as a window rule on purpose. A blacklist of `tracked_terms_returning` and
`term_universe_size` would protect against exactly these two names and nothing else.

## What I could not determine

**When each column was actually computed.** The file has values, not timestamps of when the
values were written. The backfill question is unanswerable from here. Check the job that
populates each column and confirm its schedule closes before the outcome window opens.

**Whether `ctr_x100` is restated.** If the pipeline ever recomputes it from corrected
impressions, it stops being a month-M quantity.

**Whether the 80.1% completeness is benign.** My population test says probably, on weak
evidence. Compare this row set against the unfiltered panel to be sure.

**Whether the two unsafe columns exist anywhere else under other names.** I tested ratios of
numeric column pairs. A leak expressed as a difference, a product, or across three columns would
not appear in that search.
