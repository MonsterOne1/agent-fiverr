# Structured Deliverables

Phase 1 requires document, table, and widget delivery surfaces. The local
packager creates downloadable files and a manifest under the order workroom.

## Implemented

- `document`: Markdown file plus manifest.
- `table`: CSV file plus manifest.
- `widget`: Self-contained HTML file plus manifest.
- Each package records order ID, surface, title, relative file path, MIME type,
  and metadata.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_deliverables.py'
Ran 3 tests
OK
```

## Remaining Work

- Connect package creation to every service agent delivery path.
- Add hosted file storage and signed download URLs.
- Add richer widget rendering beyond JSON-backed HTML previews.
