# Agent as a Service is coming

I have been thinking about Fiverr from a different angle.

Not as a marketplace for freelancers.

As a catalog of work that can be turned into agents.

Look at the services people buy there:

- SEO audits
- blog posts
- landing page copy
- pitch decks
- data cleaning
- dashboards
- bug fixes
- Shopify tasks
- logo concepts
- image editing
- subtitles
- podcast notes
- voiceovers
- short videos

Most of these are not magic.

They are workflows.

A buyer gives context. The seller asks clarifying questions. They define scope.
They quote a price. They use tools. They produce something. They check quality.
The buyer asks for revisions. The order closes.

That shape is already very close to an agent workspace.

The mistake is thinking the future is "one general agent that does everything."

I think the more useful future is thousands of service agents, each with a
clear job, a clear input schema, a clear output schema, a price, a turnaround
time, a QA rubric, tool permissions, revision rules, and a trust ledger.

In other words:

Not just an agent.

A service.

## Freelancers taught us the interface

Fiverr, Upwork, and similar marketplaces solved something important.

They did not just sell labor. They packaged labor.

"I will design a logo."

"I will clean your spreadsheet."

"I will fix a React bug."

"I will turn your podcast into short clips."

The listing is the interface. The brief is the API. The delivery is the output.
The review is the quality signal.

Agents can inherit this shape.

But they need more structure than a chat box.

A real service agent should have:

- scope
- non-scope
- required buyer inputs
- deliverable schema
- tool permissions
- provider keys
- QA rubric
- policy rules
- revision rules
- human handoff
- audit trail

Without these, you do not have a service.

You have a prompt with a price tag.

## "Agent as a Service"

SaaS gave us software as a service.

The next layer is Agent as a Service.

You do not just subscribe to software.

You hire a capability.

Need a market research brief? Hire the market research agent.

Need 50 product images cleaned up? Hire the image editing agent.

Need a website bug diagnosed and patched? Hire the bug-fix agent.

Need a video cut into short clips with captions? Hire the repurposing agent.

Some of these agents will be fully automated.

Some will use external tools like image, video, music, voice, browser, code, or
deployment APIs.

Some will require human review.

Some should never be fully automated because the risk is too high: legal, tax,
medical, financial advice, security, or anything with irreversible account
actions.

That is fine.

The point is not "remove humans from everything."

The point is to turn repeatable work into a system with clear boundaries.

## The interesting part is not generation

Everyone focuses on generation.

Can the model write the blog post?

Can it make the image?

Can it create the video?

That matters, but it is not the whole product.

The hard part is fulfillment.

Can the agent understand the brief?

Can it know when the brief is incomplete?

Can it quote the job?

Can it decide which tools are allowed?

Can it avoid touching a production account without approval?

Can it produce a deliverable in a reusable format?

Can it check its own work against a rubric?

Can it escalate to a human?

Can the buyer replay what happened?

That is where most agent products are still weak.

They demo well.

They do not always close the loop.

## I open sourced an experiment

I built an open-source foundation for this idea:

Agent Fiverr.

It is not a production marketplace.

It is a working foundation for an agent-native services marketplace.

The repo includes:

- 20 MVP service agents
- 800 generated long-tail service specs
- structured briefs and deliverable schemas
- workspace templates
- provider/API matrix
- dry-run provider adapters
- mock escrow and Stripe Connect scaffold
- QA runtime and reviewer-pool scaffold
- trust ledger for replaying work
- document, table, and widget deliverable packaging
- local marketplace alpha UI
- eval fixtures and verification gates

The important thing is the contract around the agent.

Every service should answer:

- What do you need from the buyer?
- What will you deliver?
- What tools can you use?
- What actions require permission?
- What counts as good enough?
- What happens when the buyer asks for revisions?
- What gets logged?
- When does a human step in?

This is the difference between a toy agent and a service agent.

## The future marketplace may look different

Today, you hire people who use tools.

Tomorrow, you may hire agents that use tools, with humans supervising the parts
that need judgment, taste, trust, or liability.

The marketplace changes from:

"Find me a freelancer."

to:

"Find me the best agent workspace for this job."

And eventually:

"Find me the best agent owned by someone else, with a track record, a price, a
SLA, and a trust ledger."

That last part matters.

Agents will not only be internal productivity tools.

They will become economic actors that other people can hire.

Not in a sci-fi way.

In a very boring, practical way:

I need this done. This agent does it well. I can pay for the outcome.

## We are building toward this

This is also the direction of our second product.

We will launch it soon.

The idea is simple:

You can directly hire an agent for a job.

Not ask it to chat.

Not spend hours prompting it.

Hire it.

Give it the brief.

Let it work.

Get the result.

And unlike a normal service provider, these agents work 24/7.

They do not wait for timezone overlap.

They do not disappear between messages.

They can keep checking status, running tools, improving outputs, and handing
off to humans when the work needs judgment.

That is the product experience I want:

You do not buy software.

You hire outcomes.

If this is interesting to you, leave a comment.

I will add the first batch of people to the waitlist.

## What still needs to be real

There is a lot of work between a foundation and a real marketplace.

The remaining gates are not just code:

- real provider keys
- real generated assets
- real payments
- real QA reviewers
- real buyers
- real cancellation and refund rates
- real cost data
- real golden outputs

That is the next step.

But the direction feels clear to me.

Freelance marketplaces showed us the demand.

Agents give us a new supply layer.

The winning products will not be the ones that simply wrap a chat box around a
model.

They will be the ones that make agents hireable, measurable, reviewable, and
safe enough to trust with real work.

Agent as a Service is coming.

And I think a lot of Fiverr-style work will be the first place it shows up.
