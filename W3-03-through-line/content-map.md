# The Through-Line: Map Content and CTAs

Emir Cabalak, General AI Fluency track, Week 3
Assignment code CUSTOM-MQWZXUQU-B5F087BE

## The one-line claim

> I build machine learning models and then try to break my own results before anyone else can.

That is the sentence a visitor should leave with. It goes directly under my name on the home
page, at the largest type size on the site, and it is the only sentence in that position.

### The ten options, and why this one

I asked for ten and got ten. Choosing was the work.

1. Machine learning you can check.
2. I build models whose numbers hold up when someone checks them.
3. Honest evaluation for models that have to survive production.
4. I find the leak in the pipeline, usually my own.
5. I build machine learning models and then try to break my own results before anyone else can.
6. Rigorous, reproducible ML evaluation for data teams.
7. The model is the easy part. The evaluation is the job.
8. I care more about the split than the algorithm.
9. Turning messy search data into models that do not lie to you.
10. ML engineer who reports the lower number.

Cuts, in order.

Six is dead on arrival. "Rigorous, reproducible" is the exact vocabulary of someone who has
never had to defend a number, and it could sit on any consultancy page.

Nine dies on "messy," which describes everyone's data and therefore describes nothing.

One and three are true and forgettable. They state a category, not a behavior. Nobody repeats
a category.

Seven and eight are the sharpest lines here and I nearly took eight. Both got cut for the same
reason: they are opinions about the field rather than claims about me. "I care more about the
split than the algorithm" is a good thing to say in an interview, once someone is already
listening. It is a bad first sentence, because a stranger has no reason to care what I care
about yet.

Ten is the closest runner up and it is very nearly right. I cut it because "the lower number"
needs a paragraph of setup before it makes sense, and the first sentence does not get a
paragraph of setup.

Four is the most human line on the list and it undersells. It makes me sound like an auditor
who reviews other people's work. I build the model too, and the claim has to say so.

Two is the claim from Week 1, unchanged. It survived a long way. What beat it: "hold up when
someone checks them" is passive about who does the checking, and the interesting part of my
actual practice is that I do the checking myself, first, on my own work. Five says that.

**Five wins.** It names both halves of the job, building and breaking. "Break my own results"
is specific and slightly uncomfortable, which is what makes it stick, and "before anyone else
can" tells the reader exactly what problem it solves for them. It could not be pasted onto
someone else's portfolio without becoming false.

**Sharpening pass.** Draft five originally read "I build ML models and then try to break my own
results before someone else does." Three changes. "ML" became "machine learning," because the
first sentence on the page should not need an acronym. "Someone else does" became "anyone else
can," because "can" carries the point that the breaking is possible and I got there first.
And I kept "try to," even though "and break" is punchier, because I do not always succeed and
the whole page is about not overstating.

## Content map

The one action from Week 1: **read one case study all the way to the end.** Every call to
action below has to ladder up to that, which means most pages point inward, not outward. Only
the last one in the chain points at my inbox.

### Home, `/`

| # | Section | Content | Notes |
|---|---|---|---|
| 1 | Name and claim | `Emir Cabalak` plus the one-line claim | largest type on the site, no navigation above it |
| 2 | Hero texture | `hero-texture.svg` | decoration, sits behind or under section 1, carries no information |
| 3 | The lead case | Case 1, the leak, with its icon, three sentences, and the accent link | this is the whole page, everything else is support |
| 4 | Two more cases | Case 2 and Case 3, one line each, icon plus title, plain links in ink | deliberately quieter than section 3 |
| 5 | One line about me | a single sentence plus a link to About | not a bio, a doorway |
| 6 | Footer | email, GitHub, the year | no social icons |

**Call to action:** "Read the leakage case. It is the one where my score went down and I kept
the lower number." Accent color, the only accent element on the page.

**Why case 1 leads.** It is the strongest of the three and it is the one that proves the claim
directly, because it is the case where I broke my own result. Case 2 is a close second on
technical substance but it is a correction to a method, which is a smaller story than finding
a leak. Case 3 is the AI-fluency piece and it is real work, but it is the least load bearing
for a data lead deciding on a hire, so it goes last on purpose.

### Case 1, `/leak`

| # | Section | Content |
|---|---|---|
| 1 | Title and icon | "The two columns that rebuilt my label" |
| 2 | The problem | why the model looked too good, in three sentences |
| 3 | What I did | the column-by-column pass, and the moment the pair showed up |
| 4 | The decision | why I wrote a window rule instead of blacklisting two names |
| 5 | The population caveat | the filter choice I disclosed rather than dropped |
| 6 | What came of it | the numbers, before and after, with the base rate |
| 7 | Screenshot | the feature verdict table, real capture |

**Call to action:** "Case 2 is the other half of this: the split that was still lying to me
after the leak was gone." Points to the next case, not to my inbox. A reader who finishes case
1 has already done the one action from Week 1, so the job of this CTA is to let them keep
going rather than to convert them.

### Case 2, `/split`

Same seven-section shape, with sections 4 and 5 replaced by "why I published all three numbers"
and "how client history depth shrank the usable set."

**Call to action:** "Case 3 is the same discipline applied to prompting instead of models."

### Case 3, `/ladder`

Same shape. Section 4 is the version that made things worse.

**Call to action:** "If you want the code behind any number on this site, email me." This is
the only outward CTA, and it sits at the end of the third case, where a reader has read
everything and has an actual reason.

### About, `/about`

| # | Section | Content |
|---|---|---|
| 1 | Portrait and bio | the real photo, four sentences, from the Week 2 bio |
| 2 | How I work | five or six lines: window rules over blacklists, grouped and time-aware splits, both numbers published, held-out figures only |
| 3 | Tools | short and unglamorous: Python, pandas, scikit-learn, SQL, notebooks. No logo wall |
| 4 | Contact | email, plain text, and GitHub |

**Call to action:** "Start with the leakage case." Sends people back into the cases. Somebody
who lands on About first has arrived out of order and the page should fix that rather than ask
them to email me on no evidence.

### Ladder check

Home points at case 1. Case 1 points at case 2. Case 2 points at case 3. About points back at
case 1. Only case 3, at the end of the reading path, points at my inbox. Every arrow either
starts the one action or continues it, and nothing on the site interrupts it with a competing
ask. There is no newsletter, no "let's connect," no contact form, and no social row.

## Still to gather

Honest list, so build week is not blocked. Nothing here blocks a first deploy, because every
item has a text fallback already written.

**Blocking nothing, needed for polish**

- Portrait photo. About page section 1. Placeholder: a text-only About page, which is fine.
- Three case screenshots. One per case page, section 7. Placeholder: the numbers as an HTML
  table, which is more accessible anyway and is what ships first.

**Numbers I need to pull from the actual runs rather than from memory**

- Case 1: the before and after scores, the exact count of features removed, and the base rate.
  These exist in the metrics JSON from that run and have to be quoted from it, not recalled.
- Case 2: all three split numbers with their row counts and client counts, and the date window.
- Case 3: which of the six ladder outputs I quote, saved as text rather than screenshots so
  they can be corrected later.

**Repo and links**

- A public repo for the site itself.
- A per-case link to the specific notebook, not the repo root. A grader and a hiring lead both
  need the exact file.
- Public-safety pass on every notebook before it goes public: no client names, no domains, no
  private queries, no tokens.

**Not yet finished, and I will say so on the page**

- The held-out future month for case 2. Case 2 currently reports cross-validation only, and its
  own limitations section says the time-shift question is untested. When that run exists the
  case gets a fourth number. Until then the page says the work is unfinished, because a
  portfolio that only contains finished things is a portfolio that stopped early.
