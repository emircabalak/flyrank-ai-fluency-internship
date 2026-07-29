# Agent Concepts and MCP Basics (FL-05)

Emir Cabalak, General AI Fluency track, Week 4

Evidence of the working connector and the three tool-calling tasks is in `mcp-evidence.md`
next to this file. This is the explainer, 888 words.

## Workflow or agent

Anthropic's *Building Effective Agents* draws the line at who decides the next step.

In a workflow, I decide. I write the steps, I fix their order, and the model fills each one in.
The path through the system is the same on every input. The model does the thinking inside a
step and none of the thinking about which step comes next.

In an agent, the model decides. I give it a goal, some tools, and a way to see what happened,
and it picks its own next action in a loop until it thinks it is finished. The path is
different on every input because the model chooses it as it goes.

The useful test is what happens when a step fails. In a workflow, a failed step produces bad
output and the next step runs anyway. In an agent, a failed step is information, and it picks
something else.

**My FL-04 pipeline is a workflow, not an agent, and not a close call.** Four fixed steps:
gather in NotebookLM, synthesize a claim ledger, critique it in a fresh conversation, format
the survivors. Every source goes through those four in that order. The model never chooses what
to do next. Even the interesting design decision in it, running the critique as a cold
conversation, is a routing choice I made and hardcoded, not one the system makes.

The word "agent" would sound better on a submission, and it would be wrong. The pipeline has no
loop, no tool selection, and no way to react to its own results. It is a chain of prompts with
defined handoffs, and that is a genuinely useful thing to have built. It is just not the other
thing.

## What MCP is

MCP, the Model Context Protocol, is a standard way for an AI application to talk to outside
software. The official docs call it a USB-C port for AI, and the analogy holds: before USB-C,
every device needed its own cable, and every AI tool integration used to need its own custom
glue. With a shared protocol, any client can talk to any server.

An MCP **client** lives inside the AI application, and an MCP **server** wraps some outside
capability: a browser, a database, a ticket tracker. One client can hold many servers, and one
server works in any client.

Servers expose three kinds of thing.

**Tools** are actions the model can call, and they can change the world. `resize_window` and
`navigate` are tools. This is the primitive that matters most, and it is the one that needs a
permission boundary, because a tool call is the model doing something rather than reading
something.

**Resources** are data the client can load into context, addressed like files. A resource is
read and does not act.

**Prompts** are reusable templates the server offers to the user, usually as slash commands.
The server author knows how their system should be asked about, so they ship the phrasing.

The distinction that took me longest: tools are for the model, prompts are for the person.

What connecting a server actually changed for me is smaller and more concrete than the
marketing suggests. Before, I could paste my CSS into a chat and get an opinion about what a
browser would do with it. After, I ran the page in a real browser at 375 pixels wide and read
back `horizontalOverflow: false` and a computed `18px`. The first is a prediction. The second
is a measurement. On my first attempt the measurement came back as default browser styling,
which told me my stylesheet had not loaded, and no amount of asking a model to read my CSS
would have produced that.

## What FL-04 would need to become an agent

One upgrade, and it is the failure I documented rather than a feature I want.

Right now the pipeline splits any source over roughly 6,000 words into halves, because I found
on run 5 that the claim ledger thins out toward the end of long documents. I found that by
eyeballing a table after the fact, and I apply the rule by hand.

The agent version replaces that with a loop. Give the model the source, the ledger, and one
tool that returns a slice of the source by section. Give it a goal: every section of this
document is represented in the ledger. Then let it decide. It reads the outline, sees which
sections have no rows, calls the tool for those sections, adds rows, and checks again. It stops
when coverage is complete or when a pass adds nothing new.

That is an agent by the definition above, because the number of passes and which sections get
reread are chosen by the model from what it observes, and they differ per document. A short API
reference would finish in one pass. Zinkevich's thirty-one-claim document might take four.

It also needs the things agents need and workflows do not: a stopping condition, a cap on
iterations so a bad run cannot spin forever, and a record of what it did so I can audit the
path afterward. A workflow's path is knowable in advance. An agent's has to be logged, because
otherwise I have output I cannot explain, which on a pipeline built to keep me honest about my
sources would defeat the point of building it.
