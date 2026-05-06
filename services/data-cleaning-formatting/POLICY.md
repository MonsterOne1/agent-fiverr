# Policy

Risk level: `low`

## Service-Specific Rules

- PII must be detected and handled according to buyer instruction.

## Authorization Gates

- External publishing, account mutation, ad spend, production deploys, payment
  actions, and email/social sends require explicit authorization from the buyer.
- Provider API keys are supplied by the owner later and must never be committed.
- Generated media must include provider/source notes in the asset manifest.

## Escalation

Escalate to human review when the task involves regulated advice, irreversible
account changes, unclear IP rights, safety-sensitive claims, or unresolved buyer
approval.
