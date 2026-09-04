# DNS checklist, for the day the subdomain is granted

Not the submission. The submission is `dns-walkthrough.md`, which the card caps at half a page
to a page. This is the operational version, written the same day, because the day a subdomain is
granted is a bad day to be working out what a resolver does.

## Before Ops does anything

1. Confirm the free URL still works: `https://emircabalak.github.io/` returns 200 over HTTPS.
2. Note what is in the repo root, because a custom domain adds one more file, `CNAME`.

## Ops half

3. Ops adds the record on `flyrank.ai`:
   `emir.flyrank.ai. CNAME emircabalak.github.io.`
   The trailing dots matter in a zone file. The target is a hostname, not a URL, so no
   `https://` and no trailing slash.

## My half, in GitHub

4. Repo `emircabalak.github.io`, Settings, Pages, Custom domain, enter `emir.flyrank.ai`, save.
   This writes a `CNAME` file into the repo root containing that one line. That file is how
   GitHub remembers, so do not delete it and do not overwrite it by force-pushing an older tree.
5. Wait for the DNS check on that page to go green. It goes red first. That is normal and means
   the record has not reached GitHub's resolver yet.
6. Tick **Enforce HTTPS**. It is greyed out until the certificate exists, so if it will not click
   the answer is to wait, not to change anything.

## Verify, do not assume

7. `nslookup emir.flyrank.ai` resolves through to GitHub's addresses. Nothing back means the
   record has not propagated or was typed wrong.
8. Response codes:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://emir.flyrank.ai/
   curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" http://emir.flyrank.ai/
   ```
   Expect 200 on the first and a 301 to the HTTPS address on the second.
9. Check all five pages, not just the home page.
10. Open it on a phone on mobile data. My laptop and my router both cache; a phone on another
    network does not.
11. Confirm the certificate. Chrome on Android no longer draws a padlock, so check it from the
    laptop.

## After

12. The old address keeps working. GitHub redirects `emircabalak.github.io` to the custom domain
    once one is set, so links already given out do not break. Confirm rather than assume.
13. Update the URL on LinkedIn and in the CV. Both keep working either way, which is the point
    of using an alias.

## The four things I expect to go wrong

**It works for me and not for somebody else.** Their resolver still holds the old answer.
Nothing is broken, there is nothing to fix, it expires on its own.

**DNS resolves but the site 404s.** DNS is fine and step 4 is missing. This is the one I would
most likely misdiagnose, because the symptom is a broken site immediately after a DNS change.

**The certificate never arrives.** Usually because the record points somewhere unexpected, or
because it was entered as an A record to a hardcoded address. GitHub has to see the domain
pointing at it before it can request one.

**The `CNAME` file disappears and the domain stops working.** This happens when the repo gets
overwritten from an older local copy that never had the file. Copy in only what changed, never
sync a whole tree over the remote.
