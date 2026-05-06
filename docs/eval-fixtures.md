# Eval Fixtures

The plan requires every MVP service workspace to run five golden samples. The
initial service specs include named examples, while this artifact turns the
requirement into executable fixture data.

## Implemented

- Generates five eval fixtures for each of the 20 MVP services.
- Validates each fixture brief against the service `BRIEF_SCHEMA` fields.
- Validates each expected deliverable includes every service output field.
- Carries service QA checks, policy expectations, revision scenario, and
  minimum pass criteria.
- Adds the fixture artifact to catalog validation.

## Evidence

```text
python3 scripts/generate_eval_fixtures.py
Eval fixtures generated.
Total fixtures: 100
Services: 20
Fixtures per service: 5
Gate: PASS

python3 -m unittest discover -s tests -p 'test_eval_fixtures.py'
Ran 2 tests
OK
```

## Remaining Work

- Replace placeholder expected deliverable content with human-approved golden
  outputs for priority services.
- Attach real provider traces and generated assets once API keys are supplied.
- Add service-specific semantic scoring beyond required-field validation.
