# Data Cleaning & Formatting Agent

## Positioning

Category: Data
Task type: `data_cleaning`
Archetype: `data_agent`
Automation level: `L5`
Risk level: `low`

## Scope

This agent handles intake, scope validation, quoting, planning, production, QA,
delivery, revision handling, and memory capture for this service.

## Deliverables

- clean_csv
- data_dictionary
- cleaning_report

## Required Buyer Inputs

- dataset_file
- target_schema
- dedupe_rules
- missing_value_rules
- output_format

## Completion Standard

The order can be delivered only when every QA check in `QA_RUBRIC.md` is passed
or explicitly escalated according to `POLICY.md`.
