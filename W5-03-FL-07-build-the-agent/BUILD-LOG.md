# Build log: the leakage auditor

Emir Cabalak, General AI Fluency track, Week 5, FL-07

In build order, including the parts where I was wrong. The card asks for real iteration rather
than a clean retroactive story, so the four things that broke are the four longest entries here.

## What got built

```
agent/AGENT.md          the instructions, the actual agent
agent/audit_tools.py    the measurements it runs; these compute, they never judge
make_eval_data.py       generates the six eval datasets from one shared panel
data/                   six CSVs, 844 to 1081 rows each
evals/ground-truth.md   what is planted in each, verified before the agent ran
evals/results.md        what happened, scored 5 of 6
reports/case1_pair.md   one full end-to-end audit report
```

The split between `AGENT.md` and `audit_tools.py` is the one design decision I would defend
hardest. The tools measure and never decide. Every verdict is written by the model after
reading numbers, which means every verdict is a sentence I can argue with rather than a
threshold buried in code. When I disagree with the agent, I disagree with a claim, not with an
`if`.

## Order of work

Narrowest thing first, as the card asks. One file, one label, one verdict table, working end to
end before anything else was added. Everything below happened in that order.

## Break 1: my ground truth was 4% false

I generated case 1 by shifting the label ratio's numerator and denominator back one month under
new names, then checked that the pair really did reconstruct the label. It agreed on 95.65% of
rows.

It should have been 100%. I had planted an exact reconstruction, so anything below exact meant I
did not understand my own data.

The cause: `shift(-1)` inside each client produces a null on that client's last month, so the
leaking columns were empty on exactly the rows at the panel edge. Forty-seven of those rows had
a positive label, so they read as disagreements.

This mattered more than the number suggests. I was about to write "the pair reconstructs the
label" into a ground-truth file, and it was 95.65% true. An eval suite whose ground truth is
approximately right cannot tell me whether an agent is approximately right.

Fixed by dropping the null rows from case 1 and case 6. Agreement is now 1.0000 on 961 rows.

## Break 2: the clean file looked dirty

The pair check prints an agreement figure for every ordered pair of numeric columns. On the
clean file, the top pair came back at **0.6966**.

Nearly 70%. On a file with nothing wrong with it.

The label rate is 0.3034, so guessing "no drop" for every row scores 0.6966. The number was not
a weak signal, it was chance wearing a signal's clothes, and my own tool was presenting it with
no way to tell the difference.

This is the failure the whole agent exists to prevent, appearing inside the agent. A number that
looks like evidence, is not, and nothing on the page says so.

Fixed by computing the majority-class baseline and printing agreement and distance from baseline
side by side. The clean file now reads:

```
-- pair reconstruction, top 5 (majority-class baseline 0.6966) --
    numerator       denominator  agreement  over_baseline
total_queries queries_with_data     0.6966         0.0000
  impressions     total_queries     0.6966         0.0000
```

Every pair at exactly zero over baseline. Against case 1 at +0.2924. The separation is now
obvious and it was invisible twenty minutes earlier.

This is also the change that saved eval case 2, the false-positive test, which is the case I
said in the spec I cared about most.

## Break 3: two of my six eval cases do not test what I designed them to test

Found by running them, not by reading them.

**Case 4** plants a sentinel value, a zero in `avg_position` meaning "no data". It passes. It
also passes in the other five files, because `avg_position` comes from the shared base panel and
carries its zeros everywhere. A test that fires on every input is not a test. Scored as a pass
and marked worthless in the results.

**Case 6** plants a backfilled column under an innocent name, and I wrote in the spec that I
expected it to fail and wanted to see how honestly it failed. It passed easily, because I
generated the column with a correlation of -0.611 in a file where nothing else clears 0.06. It
is not testing whether an innocent name gets past the agent. It is testing whether an
implausibly predictive column gets noticed, which is a much easier question.

Both are written up as broken in `evals/results.md` rather than quietly counted. Fixing them
means regenerating the data, which I have not done.

## Break 4: the population check does not work, and I do not think tuning fixes it

Case 5 has no leaking columns. The rows were filtered on next month's activity, so the row set
itself was chosen using the outcome window.

I had written a detector for precisely this: correlate each client's row count with its label
rate, on the theory that outcome-driven dropping would show up there. On the filtered file it
returns **0.0309**. On the unfiltered file it returns **0.1374**. My detector points the wrong
way.

Other numbers do survive. Completeness falls to 77.4% from 81.9%, rows per client run 3 to 10
instead of 7 to 11, and `total_queries` has a floor of 133 instead of 27.

But that last one only exists because I had the unfiltered file open beside it. An auditor
holding only the filtered file sees a minimum of 133 and has nothing to compare it against. The
most that can honestly be concluded from the file alone is that rows were dropped unevenly, and
the case is about whether the filter reads the outcome window, which is a different question.

I scored it a fail. I could have called it a partial and moved on, and a partial would have let
me report six out of six with an asterisk.

What follows from it is an instruction change rather than a code change: step 4 asks the user
for the unfiltered row set, and if it is not available the answer is "not determinable", not a
verdict. That is a worse-looking agent and a more honest one.

## Cut from the spec, and why

The FL-06 spec listed these as out of scope for ten hours and they stayed out.

Multiple files joined together, a database connection, any user interface, persistence between
runs, and suggesting replacement features. Each is real and each is a second project.

One thing was cut that the spec did not anticipate. I had intended the agent to write its report
file itself, with a confirmation prompt before overwriting. In practice I wrote the report by
hand from the tool output, because the interesting failure modes were all in the reading and
none of them were in the file write. The write-back is a convenience feature that would have
consumed build hours the reading needed. `AGENT.md` still specifies it as the intended behaviour
and it is honestly not built.

## What deviates from the FL-06 spec

**Platform.** The spec chose Claude Desktop with a local filesystem MCP server. It was built and
run in Claude Code instead, which is the same shape of thing, an MCP client with real file
access, and the one already installed and authenticated on this machine. The instructions in
`AGENT.md` are platform independent and run unchanged in Claude Desktop once the filesystem
server is configured.

**Data.** The spec assumed real FlyRank feature tables. Every dataset here is generated. That
was not a shortcut, it was the only way to have ground truth: I cannot score an auditor on a
file where I do not already know the answer. It also means nothing client-identifying is in a
public repo.

**Eval count.** Six cases rather than five, because case 2 pulls against the other five and a
suite that only rewards finding things trains an agent to find things.

## What actually works

The pair check. On case 1 it found, in seconds and from a standing start, the class of leak that
took me three weeks to find by hand on the real data. The strongest single-column correlation in
that file is 0.151, which nobody investigates.

That is the whole justification for the build. Everything else here is either supporting work or
an honest account of what it does not do.

## What I would do next, in order

1. Regenerate cases 4 and 6 so they test what they were meant to test.
2. Test leaks expressed as differences and products, not only ratios. A three-column
   reconstruction would walk straight past the current check.
3. Ask for the unfiltered row set in step 4 and compare, since that is the only way population
   filtering becomes answerable.
4. Run it against a real feature table where I do not know the answer, which is the first run
   that would tell me anything the eval suite cannot.
