# Data Scraping + Enrichment Agent

## Positioning

Category: Data
Task type: `scraping`
Archetype: `data_agent`
Automation level: `L3`
Risk level: `medium`

## Scope

This agent handles intake, scope validation, quoting, planning, production, QA,
delivery, revision handling, and memory capture for this service.

## Deliverables

- dataset
- scraper_plan
- source_log

## Required Buyer Inputs

- target_sources
- fields
- volume
- refresh_frequency
- allowed_methods
- compliance_constraints

## Completion Standard

The order can be delivered only when every QA check in `QA_RUBRIC.md` is passed
or explicitly escalated according to `POLICY.md`.
