# DNS walkthrough

Emir Cabalak, General AI Fluency track, Week 5, PF-04

Written before I need it, on purpose. When my FlyRank subdomain is granted, this is the
checklist I run. It is written so somebody non-technical on the team could follow the
explanation, and so I could follow the steps at eleven at night without thinking hard.

## What actually happens when somebody types my address

Six steps, and the whole thing usually takes under a tenth of a second.

**1. Somebody types `emir.flyrank.ai` into a browser.**

That name means nothing to the network. Computers do not find each other by name, they find
each other by number. So before anything can load, the name has to be turned into a number.
That translation is the entire job of DNS.

**2. The browser asks a resolver.**

The resolver is whichever DNS service the person's computer is set to use. Usually their
internet provider, sometimes one they chose like `1.1.1.1` or `8.8.8.8`. Think of it as a
directory service that takes the question and does the legwork.

The resolver checks its own memory first. If somebody else on the same network asked for
`emir.flyrank.ai` a minute ago, it already knows the answer and skips everything below. That
cache is why a DNS change is not instant for everyone, and it is the single most common reason
somebody says "it is not working for me" when it works fine for you.

**3. The resolver walks down the name, right to left.**

Names are read backwards by DNS. It asks a root server who handles `.ai`, then asks the `.ai`
servers who handles `flyrank.ai`. Those answers point it at FlyRank's nameservers.

A nameserver is just the machine that holds the official list of records for a domain. FlyRank's
nameservers are the only place that knows the truth about anything ending in `flyrank.ai`.

**4. The resolver asks FlyRank's nameserver about `emir.flyrank.ai`.**

This is where my record lives, and this is the half Ops does. They add one line to that list.

**5. The nameserver answers with a CNAME.**

A **CNAME record** means "this name is an alias for that other name, go ask about that one
instead". It does not contain an address. It contains a forwarding instruction.

Mine will read, in effect:

```
emir.flyrank.ai.   CNAME   emircabalak.github.io.
```

So the answer that comes back is not a number, it is another name. The resolver then repeats
steps 3 to 5 for `emircabalak.github.io`, which does resolve to real addresses, and hands those
back to the browser.

**Why a CNAME instead of an address.** If I put GitHub's IP address in directly with an A
record, then the day GitHub changes its IPs, my site goes dark and I have to notice and fix it.
With a CNAME I am pointing at GitHub's name, and GitHub keeps the numbers behind that name
correct. The alias is maintenance I never have to do.

**6. The browser connects, and asks for my site by name.**

Now it has an address, so it opens a connection to GitHub's servers. Two things then have to go
right, and they are the two that people forget are separate from DNS.

First, the browser tells the server which name it was looking for. GitHub serves thousands of
sites from the same addresses, so it needs to know which one. That is why I also have to add
the custom domain **on GitHub's side**. DNS pointing at GitHub is not enough on its own. If I
skip that half, DNS resolves perfectly and GitHub answers with a 404, which looks like a DNS
problem and is not one.

Second, HTTPS. The certificate has to be issued for `emir.flyrank.ai` specifically. GitHub
requests one automatically once it can see the DNS record pointing at it, which takes a few
minutes and sometimes up to an hour. Until it arrives the site loads over HTTP and the browser
warns. That is expected and it resolves itself. It is not something to panic and undo.

## The checklist, for the day it is granted

**Before Ops does anything**

1. Confirm the free URL still works: `https://emircabalak.github.io/` returns 200 over HTTPS.
2. Note which files are in the repo root, because a custom domain adds one more, `CNAME`.

**Ops half**

3. Ops adds the record on `flyrank.ai`:
   `emir.flyrank.ai. CNAME emircabalak.github.io.`
   The trailing dots matter in a zone file. The target is my GitHub Pages hostname, not a URL,
   so no `https://` and no trailing slash.

**My half, in GitHub**

4. Repo `emircabalak.github.io`, Settings, Pages, Custom domain, type `emir.flyrank.ai`, save.
   This writes a file called `CNAME` into the repo root containing that one line. That file is
   how GitHub remembers, so I must not delete it, and I must not overwrite it by force-pushing
   an older tree.
5. Wait for the DNS check on that page to go green. It goes red first. That is normal, it means
   the record has not reached GitHub's resolver yet.
6. Once green, tick **Enforce HTTPS**. This checkbox is greyed out until the certificate is
   issued, so if it is not clickable the answer is to wait, not to change anything.

**Verifying, not assuming**

7. Check the record resolves from outside my own machine:
   ```bash
   nslookup emir.flyrank.ai
   ```
   I expect to see it resolve through to GitHub's addresses. If it returns nothing, the record
   has not propagated yet or was typed wrong.
8. Check the site actually answers, and check the redirect:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://emir.flyrank.ai/
   curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" http://emir.flyrank.ai/
   ```
   I want 200 on the first, and a 301 to the HTTPS address on the second.
9. Check every page, not just the home page. I have five.
10. Open it on my phone on mobile data. Same reason as Week 4: my laptop and my router both
    cache, and a phone on a different network does not.
11. Confirm the padlock, or the certificate directly if the browser has stopped drawing padlocks.

**After**

12. The old URL keeps working. GitHub redirects `emircabalak.github.io` to the custom domain
    once one is set, so links I have already given people do not break. Worth confirming rather
    than assuming.
13. Update the URL on LinkedIn and on my CV. Both keep working either way, which is the point
    of using an alias.

## What I expect to go wrong

Writing these down now so that when one happens I recognise it instead of debugging blind.

**It works for me and not for somebody else.** Caching, step 2. Their resolver still holds the
old answer. Nothing is broken and there is nothing to fix, it expires on its own.

**DNS resolves but the site 404s.** DNS is fine and the GitHub side is missing. That is step 4
of my half. This is the one I would most likely misdiagnose as a DNS fault, because the symptom
is a broken site right after a DNS change.

**The certificate does not arrive.** Usually because the record points somewhere unexpected, or
because it was entered as an A record to a hardcoded address. GitHub needs to verify the domain
points at it before a certificate can be issued.

**The `CNAME` file disappears and the domain stops working.** This happens when the repo is
overwritten from an older local copy that never had the file. The lesson is the same one from
my working notes: never sync a whole tree over the remote, copy in only what changed.

## What this is not

A custom domain is a pointer, not a move. Nothing about my site changes: same repo, same files,
same host, same build. All that changes is one extra name that arrives at the same place. That
is worth saying because "moving to a custom domain" sounds like a migration and getting nervous
about it is how people break a working site.
