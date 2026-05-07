# Security

## Supported Status

This project is an experimental foundation. It is not production-ready and
should not be used with real buyer accounts, payment accounts, ad accounts, or
customer data without additional review.

## Reporting Issues

Please open a private security advisory on GitHub if available, or contact the
maintainer through the repository owner profile.

Do not include live credentials, private keys, customer exports, or exploitable
payloads in public issues.

## Credential Policy

- Real API keys must never be committed.
- `.env` is ignored.
- `.env.example` contains empty placeholders only.
- Provider names, env var names, scopes, and call plans may be committed.
- Live provider calls must be explicitly enabled in code.

## Side-Effect Policy

The runtime distinguishes dry-run, planned, read-only, asset-generation, and
explicit-authorization actions.

These actions must require explicit authorization:

- account mutation
- ad spend
- payment actions
- production deploys
- external publishing
- outbound email or social sends

## Data Policy

Do not commit:

- customer files
- buyer briefs from real orders
- payment records
- private account exports
- generated assets with unclear commercial rights
- access tokens or session cookies
