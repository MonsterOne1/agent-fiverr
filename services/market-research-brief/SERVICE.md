# Market Research Brief Agent

## Positioning

Category: Business
Task type: `market_research`
Archetype: `consulting_agent`
Automation level: `L4`
Risk level: `medium`

## Scope

This agent handles intake, scope validation, quoting, planning, production, QA,
delivery, revision handling, and memory capture for this service.

## Deliverables

- research_report
- competitor_table
- source_log

## Required Buyer Inputs

- market
- region
- customer_segment
- questions
- competitors
- time_horizon

## Completion Standard

The order can be delivered only when every QA check in `QA_RUBRIC.md` is passed
or explicitly escalated according to `POLICY.md`.
