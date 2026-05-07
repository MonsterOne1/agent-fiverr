# Contributing

Agent Fiverr is an early open-source foundation for agent-native service
workspaces. Contributions should make service agents more auditable,
repeatable, safe, and useful.

## Good First Contributions

- Add or improve service workspace specs.
- Improve QA rubrics and eval fixtures.
- Add provider adapter scaffolds.
- Improve marketplace, escrow, or trust-ledger tests.
- Improve docs and examples.
- Add real-world case studies without secrets or private customer data.

## Development

Run all local gates before opening a PR:

```bash
python3 scripts/run_all_gates.py
```

For focused work:

```bash
python3 scripts/validate_catalog.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Rules

- Do not commit real API keys, customer data, private account exports, or
  generated assets with unclear rights.
- Keep provider integrations behind explicit credential and side-effect gates.
- Add tests for new runtime behavior.
- Update docs when changing acceptance evidence.
- Preserve the service workspace file contract unless a migration is included.

## Pull Request Checklist

- [ ] `python3 scripts/run_all_gates.py` passes.
- [ ] No secrets or private customer data are committed.
- [ ] New behavior has tests.
- [ ] Relevant docs are updated.
- [ ] Provider side effects require explicit authorization.
