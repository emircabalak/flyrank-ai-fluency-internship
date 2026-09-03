# Design Your Personal Agent (FL-06)

Emir Cabalak, General AI Fluency track, Week 5

## The job

**A leakage auditor.** Point it at a dataset file and a label definition. It reads the actual
data, works through the columns, and hands back a verdict on every one: safe, unsafe, or
conditional, with a reason it can defend and a counter-scenario for each safe verdict.

One job. It does not clean data, does not train anything, does not suggest features. It answers
one question: which of these columns am I allowed to use, and what would have to be true for
that to change.

I picked this because it is the thing I actually do by hand and get wrong. Case 1 on my site is
a leak I found after three weeks of not finding it. The two columns were the numerator and the
denominator of the ratio my label was thresholded from, sitting in different tables under
different names. Nothing in my process would have caught that except reading every column and
asking the same question of each, which is exactly the kind of patient, boring, repeatable work
worth handing to an agent.

I considered building the coverage loop I named at the end of FL-05, the one that reruns my
study-notes pipeline until every section of a source is represented. It is a good agent and it
is a smaller idea. The leakage auditor has something the other does not: a ground truth I can
check. I have datasets where I know which columns are dirty, so I can tell whether it is right,
which makes real evals possible instead of vibes.

## The user

Me, and one other kind of person later.

I use it at one specific moment: after I have assembled a feature table and before I train
anything on it. In practice that is two to four times a month, in bursts. It is not a daily
tool and I do not want it to be one, because if I am running it daily something has gone wrong
with how I build feature tables.

The second user is whoever reviews my work. The output has to be a document I can hand over,
not a chat log I have to summarise.

## Tools and data, with access plan

| What it needs | How it gets it | Already available? |
|---|---|---|
| The dataset file | filesystem MCP server, read only, scoped to one folder | yes, copy-paste config in the MCP docs |
| Column names, types, null counts | reads the file and computes them | yes, via the same connection |
| Value samples and distributions | computed on demand, only for columns it decides to look at | yes |
| My label definition | I type it in at the start of the run | yes, no tooling needed |
| Data dictionary if one exists | same folder, same read-only connection | sometimes, and it must work without one |
| Writing the report | writes one markdown file into an output folder | yes, and it is the only write it may do |

The access plan is deliberately small. One folder, read only for the data, one file it may
write. No database credentials, no cloud, no API keys, nothing to rotate. The data never leaves
my machine except as the columns and the samples that go into the model's context, and I decide
which folder that is.

**What it does not get.** No write access to the data. No network. No ability to run arbitrary
shell commands. It can read, compute, and produce one report.

## Draft instructions

```
You audit feature tables for label leakage. You are read-only on the data.

INPUT
A dataset file and a label definition stated as a rule over a time window.

BEFORE YOU JUDGE ANYTHING
1. Restate the label definition in your own words and name every column that appears in it,
   including columns that appear inside a ratio, a difference or a threshold.
2. List the columns whose values could only be known after the outcome window opens.
3. List every pair or group of columns that is individually harmless but together
   reconstructs the label or the quantity it is thresholded from. Look hardest here. This
   is the failure that cost me three weeks and it does not look like leakage from any
   single column.
4. Check the population filter. If the rows in this table were selected using anything from
   the outcome window, say so. That is a disclosure, not a crime, and it is not a column
   problem so nothing above will catch it.

THEN, ONE ROW PER COLUMN
column | verdict (safe / unsafe / conditional) | reason | condition if conditional

RULES
Treat leakage as a property of the time window, not a list of column names. A blacklist
protects me only from the columns I already found.
For every column you mark safe, name one scenario in which it would actually be unsafe. If
you cannot construct one, say so plainly.
Do not guess a value you cannot compute from the file. Write "not determinable from the
data provided".
Watch for sentinel values. A zero that means "no data" is not a zero, and any mean over
that column is wrong before leakage is even a question.
Watch for three-state flags. A column that can be true, false or null will silently drop
rows if it is filtered with = FALSE.
Keep the hedge. If the evidence is weak, the verdict is conditional, not safe.

FINISH WITH
The rule, written as a time-window rule rather than a column list, so it still holds for
columns that do not exist yet.
A short list of what you could not determine and what I would have to check.
```

## Five eval cases, written before the build

Ground truth is known for all of these because I built or broke them myself. Case 2 is the one
I care about most.

**1. The pair that rebuilt my label.** The real FlyRank feature table. Label is a ratio
thresholded at 0.6, and both components are present under different names in different tables.
*Pass:* it names the pair as a pair. Naming only one half is a fail, because that is what my
V4 prompt did in the ladder and it is worse than saying nothing, since it looks like an answer.

**2. A clean table.** A feature set I have already audited by hand and believe is clean.
*Pass:* it reports no leakage and does not invent one. This is the false-positive test and it is
the case most likely to fail, because an auditor rewarded for finding problems will find
problems. An agent that flags something here is useless, since I will stop trusting every
verdict it gives.

**3. A single obvious leak.** A column that is a direct arithmetic transform of the label,
dropped in on purpose. *Pass:* found immediately, marked unsafe, and the reason names the
transform. This is the easy case and it exists to catch total failure.

**4. The sentinel trap.** A table where `avg_position == 0` means "no data" rather than rank
zero, and there is no data dictionary to say so. *Pass:* it notices the zeros are implausible
as ranks and flags the column as conditional. This is not leakage at all, which is the point:
I want to know whether it only looks for the thing it was asked about.

**5. The population filter.** A table with no leaky columns at all, where the rows were
selected using a minimum-activity threshold computed over the outcome window. *Pass:* it says
the columns are clean and separately flags how the rows were chosen. Failing this is the
subtlest failure available, because every column really is safe and the answer really is wrong.

**6. Time-shifted innocence.** A column with a completely innocent name whose values were
backfilled after the outcome month closed. *Pass:* it marks it conditional and says it cannot
verify when the column was computed, rather than assuming. I expect it to fail this one from the
data alone, and I want to see whether it fails honestly.

Scoring is per case, pass or fail, no partial credit, and I write down what it actually said
before deciding. Six cases rather than five because case 2 pulls in the opposite direction from
all the others, and a suite that only rewards finding things teaches the agent to find things.

## Risks and guardrails

**Must confirm before acting**

- Writing the report file, if a file of that name already exists.
- Reading anything outside the folder I pointed it at.

**Must never**

- Modify, move, or delete a data file. The connection is read-only and that is enforced in the
  MCP server configuration, not just asked for in the instructions. An instruction is a
  preference, a config is a boundary.
- Send data anywhere. No network access at all.
- Report a column verdict without a reason, or a safe verdict without a counter-scenario.
- Invent a statistic. If it cannot compute something, the answer is "not determinable", never a
  plausible number.
- Print raw rows of client data into the report. Column names, types, null counts and value
  ranges are fine. Actual rows are not, because the report gets shared.

**The risk I take most seriously.** A false "all clean" is worse than a false alarm. If it
misses a leak I train on poisoned features and publish a number I will have to walk back. If it
raises a false alarm I lose an hour. So every ambiguous case resolves to conditional, and the
report ends with what it could not determine rather than pretending the list is complete.

**The second risk.** I stop reading the output and start trusting it. The guardrail there is
not technical: I keep case 2 in the suite and rerun the whole suite whenever I change the
instructions, so I always know its current false-positive behaviour rather than remembering how
it behaved last month.

## Platform

**Chosen: Claude Desktop with a local filesystem MCP server.**

The job needs three things: read a real file on my disk, compute things about it, and loop,
because the agent should decide which columns deserve a closer look and go back for samples. The
MCP filesystem server is a copy-paste config in the official docs, no programming, and it gives
exactly the read-only, folder-scoped access this needs. It is also the connection type I already
proved I can drive, in FL-05, against my own site.

**Rejected: a Claude Project with the files uploaded.** This was my first instinct and it is
close, since a Project holds standing instructions well and my draft instructions above would
live there happily. It fails on the data. Uploading a file freezes it, so auditing a new
version means re-uploading, and the agent cannot go back and compute a null count on a column it
became suspicious about halfway through. The whole point of the design is that it looks at the
data rather than at a description of the data.

**Rejected: n8n.** Good for scheduled, unattended, many-step flows. This is neither scheduled
nor unattended, and its shape is a loop with a judgment call in it, which is the thing n8n is
worst at expressing.

**Rejected: a custom GPT.** Needs a paid plan, and the constraint I set in Week 4 was free
paths only. I am not going to break that for one card.

## Scope, against ten build hours

**In:** one CSV or Parquet file at a time, a label definition typed in at the start, the verdict
table, the pair check, the population-filter question, the written window rule, one markdown
report out. The six eval cases run and their results recorded.

**Out, deliberately:** multiple files joined together, a database connection, any user interface,
persistence between runs, remembering previous audits, and suggesting replacement features. Each
of those is a real want and each is a second project.

The narrowest thing that is still worth running is: one file, one label, one verdict table.
That is what gets built first and demonstrated end to end before anything else is added, which
is what FL-07 asks for anyway.
