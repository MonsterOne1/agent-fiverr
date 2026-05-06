# Tools

## Required Providers

- openai_responses
- github
- vercel

## Credential Handling

Provider IDs are committed here; keys are not. Expected key delivery options:

- `.env` for local development.
- Secret manager for hosted workspaces.
- Per-workspace provider authorization for buyer-owned accounts.

## Side-Effect Discipline

Read-only analysis may run automatically. Account changes, deployments,
publishing, payments, ad spend, and outbound communication require explicit
authorization in the order trace.
