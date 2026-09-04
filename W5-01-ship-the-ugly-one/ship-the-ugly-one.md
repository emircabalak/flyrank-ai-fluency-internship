# Ship the Ugly One

Emir Cabalak, General AI Fluency track, Week 5
Assignment code CUSTOM-MQX0BLWA-0E956776

**Live URL:** <https://emircabalak.github.io/>

Every page in my sitemap is up and reachable. The navigation works from any page to any other.

| Page | Address | State |
|---|---|---|
| Home | `/` | claim, hero, lead case, two more cases, one line about me |
| Case 1 | `/leak.html` | full writeup, real numbers, one screenshot slot still empty |
| Case 2 | `/split.html` | full writeup, three-split table, one screenshot slot still empty |
| Case 3 | `/ladder.html` | full writeup, six-version table, one screenshot slot still empty |
| About | `/about.html` | real photo, bio, how I work, other repositories, contact |

Complete enough to understand, not polished. The real cases are in, with real figures from the
runs that produced them, not placeholder text.

## The one real person

I sent the bare link to a friend with no note about what it was, because the site's job is to
explain itself and I would have contaminated the test by doing it for it. They are not in AI or
data, which turned out to matter.

Their first message back, before opening it, was **"ne işe yarıyor"**, which is "what is it
for". I have thought about that one more than about the answers I actually asked for. I sent a
personal site and the first instinct was to ask what it does. That is a reasonable question and
my home page does not answer it directly. It says what I do. It does not say what a reader
gets.

Then the three answers.

**What they saw, in their words:** *"Bir ml modeli yapmışsın ama hatalarını başkaları bulmadan
önce kendin çözmüşsün."* You built an ML model, but you found its mistakes yourself before
anyone else did.

That is my one-line claim, almost word for word, from somebody who has never worked in this
field and who read no more than two pages. The claim landed. That is the single most useful
thing in this feedback and it is the part of the site I was least sure about.

**Where they got stuck:** case 1. Not immediately, and not at the structure. At the vocabulary.
They said they struggled with some of the terms because they are not in the AI field, went and
looked a few up, and then started to follow it.

Worth being precise about what that does and does not tell me. My audience is a data lead who
already knows what a split is, so a non-specialist bouncing off `ROC AUC` and `GroupKFold` is
not a failure of the page. Those terms are the shortest true way to say what I mean, and
removing them would make the page worse for the person it is for. But somebody caring enough to
go and look up two words is a real signal, and I would rather earn that than assume it.

**Where they stopped reading:** case 2. Their words: *"cümlelere tam anlam veremediğim için
sıkıldım."* I could not fully make sense of the sentences, so I got bored.

This is the finding. My whole call-to-action chain assumes a reader goes home to case 1 to case
2 to case 3, and this reader left in the middle of case 2. So the chain is longer than the
attention it earns. Case 3 might as well not be on the site for this reader, and case 3 is
where the only outward CTA lives.

**Did the work land:** yes for the claim, partly for the evidence. They came away able to say
what I am good at, which is what the home page is for. They did not come away able to say why
they should believe it, which is what the cases are for. One page did its job, the other did
not finish.

## What I am changing because of this, and what I am not

**Changing.** Case 2 needs to be readable further in. The problem is not the numbers, they are
in a table and the table is fine. It is the paragraphs around them, which are long and assume
you are still holding case 1 in your head. Shorter sentences, and a plain first line in each
section saying what the section is about before it starts arguing.

**Changing.** The home page should answer "what is this for" somewhere. One line, near the
claim, aimed at the reader rather than at me.

**Not changing.** The technical vocabulary in the cases. My reader knows those words, and
writing around them would cost precision to serve somebody I am not writing for. The honest
version of this feedback is "this reader is not my reader", and pretending otherwise would be
the wrong lesson to take from a sample of one.

**Not changing yet, and worth saying.** This is one person, not in my target audience, reading
for five minutes as a favour. The claim landing is a real result. Everything else is a
direction to look, not a conclusion. The next test should be somebody who does work with data,
because their boredom would mean something different from this boredom.

## Still ugly

Honest list. All of these are things I already know are rough, written before anybody points
them out.

**Three empty screenshot boxes.** One on each case page, saying a screenshot goes here. They
are dashed grey rectangles admitting a gap. Every number they would show is already on the page
as text, so nothing is missing except corroboration, but a visitor sees three boxes announcing
unfinished work.

**Case 2 loses people.** Established above by the only person who has read it.

**Case 3 is barely visited.** It sits at the end of a chain nobody has finished, and it holds
the only outward call to action on the entire site. If the chain does not survive case 2, the
email link may as well not exist.

**The home page has no answer to "what is this for".** Diagnosed by the first message my one
tester sent.

**The three case pages are copy-paste siblings.** Same nav, same footer, same shape, all
duplicated across five files. That is a deliberate choice from my stack decision and it is fine
at five pages. It is also the thing that will rot first: I have already had to edit the footer
in five places twice, once for LinkedIn and once for the CV.

**Case 2 admits an unfinished experiment.** It says the held-out future month does not exist
yet. That is honest and I stand by publishing it, and it is still a case study whose best number
has not been computed.

**No analytics.** I have no idea whether anybody reads any of this. My only reader data is one
friend on WhatsApp.

**The hero is decorative.** It is a scatter split by a dashed wall. Somebody who knows what a
train and test split looks like reads it instantly. Everybody else sees a quiet chart. That was
a deliberate call and it is still an image doing very little work for most visitors.

**Mobile is verified, not designed.** I checked it does not overflow and that the type scales.
I have not thought about whether a five-column table is a good experience on a phone, only that
it fits.

**The CV and the site disagree.** The CV lists a different email address from the one in the
site footer. Small, and exactly the kind of thing a careful reader notices and quietly counts
against you.
