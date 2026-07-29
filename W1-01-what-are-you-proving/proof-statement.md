# What Are You Proving?

Emir Cabalak, General AI Fluency track, Week 1
Assignment code CUSTOM-MQWZHD18-5B447868

## The proof statement

I can build machine learning models whose numbers hold up when somebody checks them. That is
the one thing this portfolio is for. Not "I know Python," not "I'm interested in AI," and not
three skills stapled together with an "and." The specific skill is catching the reasons a
model looks better than it is: label leakage, a split that lets the same client sit on both
sides, a metric quoted from a run that trained on the rows it was scoring. I am writing this
for one kind of person, the one who decides on the hire for a small data or analytics team,
usually a lead who has already shipped a model that scored 0.94 in a notebook and then did
nothing useful in production. That person does not need another candidate who can call
`fit()`. They need to know whether my numbers can be trusted before they are the ones
defending them in a meeting. So the single action I want from them is this: read one case
study all the way to the end, the one where I found a leak in my own features and my score
dropped. Not email me, not download a CV, not book a call. Those come after, or they do not,
and either way they are downstream of the same fifteen minutes of reading.

## Why this needs to exist

A CV can say I did machine learning at an internship and LinkedIn can show the same line with
a logo next to it, but neither one can show the moment I deleted a feature that was making my
model look good, and that moment is the entire argument.

---

## Appendix: how the claim got narrowed

The brief asks for AI to be used as a thinking partner rather than an author, so this is the
short version of the interview. Each round killed a draft.

**Round 1.** First attempt: "I can build AI and machine learning solutions that solve real
business problems."

Question back: which part of that could a bootcamp graduate not also write? Fair. All of it.
"Real business problems" is filler and "AI and machine learning" is two claims. Killed.

**Round 2.** Second attempt: "I can build ML models on messy real-world data."

Question back: messy how, and what happens when the data is clean? Also, everyone's data is
messy, so this describes the input and not the skill. Killed.

**Round 3.** Third attempt: "I can find data leakage in ML pipelines."

Closer, but too small. That is a task, not a skill you hire for. It also implied I only audit
other people's work, when I actually build the model too. Pushed back on that one myself.

**Round 4.** "I can build ML models whose numbers hold up when somebody checks them."

This one survived. Leakage is the example, not the claim. It covers the split design and the
metric reporting as well, and it is falsifiable: hand me a model and check.

**On the audience.** I first wrote "hiring managers at tech companies," which is a category
and not a person. The narrowing question was: what has this person already lived through that
makes my claim land? The answer gave the version above. I am deliberately writing it as a role
rather than naming one individual, because FlyRank is the first reader but not necessarily the
last, and the wording has to keep working when it is passed on.

**On the action.** I wanted "email me," because that is the outcome I actually want. But an
email is what someone does after they believe you, not the thing that makes them believe you.
The reading is the work. The email is the receipt.
