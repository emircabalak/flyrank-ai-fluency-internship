# DNS walkthrough

Emir Cabalak, General AI Fluency track, Week 5, PF-04

Written before I need it. When my FlyRank subdomain is granted, this is what I will already
understand.

## What DNS is for

Computers do not find each other by name. They find each other by number. So before any page
can load, the name somebody typed has to be turned into an address. Turning names into numbers
is the whole job of DNS.

## What happens when somebody types `emir.flyrank.ai`

**The browser asks a resolver.** The resolver is whichever lookup service that computer is set
to use, usually the internet provider's. Think of it as a directory service that takes the
question and does the running around.

It checks its own memory first. If anybody on that network asked recently, it already knows and
skips everything below. That memory is why a DNS change is not instant for everybody, and it is
the usual reason one person says a site is broken while it works fine for you.

**The resolver walks the name backwards.** It asks a root server who handles `.ai`, then asks
the `.ai` servers who handles `flyrank.ai`. Those answers point it at FlyRank's nameservers.

A nameserver is simply the machine holding the official list of records for a domain. FlyRank's
nameservers are the only place that knows the truth about any name ending in `flyrank.ai`.

**The nameserver answers with a record.** Mine will be a CNAME:

```
emir.flyrank.ai.   CNAME   emircabalak.github.io.
```

**A CNAME means "this name is an alias for that other name, go and ask about that one
instead."** It holds no address at all, only a forwarding instruction. So the response the
resolver gets back is another name, not a number. It repeats the lookup for
`emircabalak.github.io`, which does resolve to real addresses, and that final response goes to
the browser.

**Why an alias and not an address.** If I wrote GitHub's IP address in directly, the day GitHub
changes its addresses my site goes dark until I notice. Pointing at their name instead means
they keep the numbers behind it correct. The alias is maintenance I never have to do.

**The browser connects and asks by name.** GitHub serves thousands of sites from the same
addresses, so the browser tells the server which name it was looking for.

This is why DNS is only half the job. I also have to add the custom domain in the repo's own
settings, or GitHub will answer a request it does not recognise with a 404. That failure looks
exactly like a DNS problem and is not one, and it is the mistake I expect to make.

HTTPS is separate again. The certificate has to be issued for `emir.flyrank.ai` specifically.
GitHub requests one once it can see the record pointing at it, which takes minutes and
occasionally an hour. Until then the browser warns, which is expected and resolves itself.

## The order on the day

Ops adds the CNAME on `flyrank.ai`. I add `emir.flyrank.ai` under Settings, Pages, Custom
domain, which writes a `CNAME` file into my repo that I must not delete. I wait for the check to
go green, it goes red first, then I tick Enforce HTTPS once that box stops being greyed out.

Then I verify rather than assume: `nslookup emir.flyrank.ai` resolves, every page returns 200,
`http://` gives a 301 to `https://`, and it opens on my phone.

Nothing about the site changes. Same repo, same files, same host. A custom domain is a pointer,
not a move.

The longer version, with the full checklist and the four things I expect to go wrong, is in
`dns-checklist.md`.
