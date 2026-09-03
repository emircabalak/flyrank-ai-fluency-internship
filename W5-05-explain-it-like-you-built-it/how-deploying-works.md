# Explain It Like You Built It

Emir Cabalak, General AI Fluency track, Week 5
Assignment code CUSTOM-MQX0CE9V-B5BB265F

**The piece I picked:** how `git push` actually turns into a website other people can open.

I picked this one because it is the part that broke, and because until it broke I did not really
know what was happening. I thought "push and it goes live" was one action. It is three, and the
middle one is where my site fell over.

Written as if explaining to a friend who has never built a site.

---

## The short version

There are three separate things going on, and I had them mushed into one in my head.

1. My files go to GitHub.
2. GitHub takes those files and builds a website out of them.
3. GitHub keeps that website on a server and hands it out when somebody asks.

Step 1 is `git push`. Steps 2 and 3 happen without me, which is exactly why I did not know they
existed until step 2 quietly ate one of my files.

## Step 1: getting the files to GitHub

On my laptop there is a folder with eleven files in it: five pages, one stylesheet, some
pictures. Nothing clever. If you open `index.html` by double-clicking it, your browser shows my
home page. It works, and only I can see it, because the file is on my hard drive.

`git push` copies that folder to GitHub. That is the whole job. GitHub now has a copy.

An important thing I did not appreciate: pushing does not publish anything. GitHub has millions
of folders that are not websites. Having my files there is like handing somebody a stack of
paper. Nobody has agreed to put it on a noticeboard yet.

## Step 2: GitHub builds a site out of them

This is the step I did not know about.

When you turn on the feature called GitHub Pages, GitHub starts watching that folder. Every time
you push, it takes your files, runs them through a program, and puts the result on a web server.

The program is called Jekyll. It exists because a lot of people want a blog, and writing a blog
by hand means copying the same header into forty pages. Jekyll lets you write the header once and
have it stamped into every page for you, and it turns simple text files into proper HTML. It is
genuinely useful if that is what you want.

I did not want that. My five pages are already finished HTML. I wrote them myself. But GitHub
runs Jekyll by default, because most people do want it, so my files went through a machine that
was trying to be helpful and was not needed.

And it lost my stylesheet.

## What that looked like

I pushed, waited a minute, opened the address on my phone, and got a page that looked like
1998. Times New Roman, white background, blue underlined links.

That is what a web page looks like with no styling at all. My HTML was fine, all the words were
there in the right order. The file that says "the background is dark, the headings use this
font, this one link is orange" was not being delivered.

I checked, and `style.css` was giving back "404 not found", which means the server saying
"there is nothing here by that name". Meanwhile every other file, all five pages and every
image, came back fine.

The file was definitely there. I could see it on GitHub. I had just pushed it.

The confusing part, and the bit I want to remember: **GitHub said the build succeeded.** Green
tick, no errors. So the thing that reports whether it worked was telling me it worked, while the
site was visibly broken.

## The fix

One empty file, in the folder, named `.nojekyll`.

That is it. The name is the instruction. It means "do not run Jekyll on this". GitHub sees that
file and skips step 2 entirely, and just serves my files exactly as I wrote them, which is all I
ever wanted.

I pushed it, waited a minute, and the site came back with its fonts and colours.

## Step 3: handing the files out

Now my files sit on a GitHub server. When somebody types `emircabalak.github.io`, their browser
opens a connection to that server and says, roughly, "give me the home page".

The server sends back `index.html`. The browser starts reading it, hits the line that says "I
need a file called style.css", and asks for that one too. Then it hits the pictures, and asks
for those. Five separate requests for my home page, and the whole thing is done in well under a
second.

This is why my site was still readable while it was broken. The words arrive first, in the HTML.
The styling is a second, separate request. If that second request fails, you still get the
page, it just looks like nothing.

## What I actually learned

**"It works on my machine" is not a joke, it is a category of bug.** My local copy had been
fine for an hour. Nothing about my code was wrong. The difference was entirely in what sat
between my files and the browser, and there is no way to see that from my own machine, because
on my machine there is nothing in between.

**A green build is not a working site.** The build status answers "did the program finish
without crashing", which is not the same question as "does the site work". Now I check the
actual files: ask the server for each one and look at whether it says 200, meaning here it is,
or 404, meaning there is nothing here. That takes ten seconds and it does not lie.

**Defaults are decisions somebody else made for you.** Jekyll was not a bug. It was a sensible
default for a different kind of user. Most of the time defaults are doing you a favour and you
never notice. When something breaks for no reason, a good early question is "what is running
here that I did not ask for".

I would not have found any of this if I had only ever opened the file on my laptop. The whole
lesson lives in the gap between my folder and a URL, and the only way to see the gap is to put
something on a URL.
