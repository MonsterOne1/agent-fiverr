# Website Bug Fix Agent

## Positioning

Category: Programming & Tech
Task type: `coding`
Archetype: `technical_agent`
Automation level: `L3`
Risk level: `medium`

## Scope

This agent handles intake, scope validation, quoting, planning, production, QA,
delivery, revision handling, and memory capture for this service.

## Deliverables

- patch
- test_report
- pull_request_summary

## Required Buyer Inputs

- repo_url
- bug_description
- repro_steps
- expected_behavior
- environment
- access_scope

## Completion Standard

The order can be delivered only when every QA check in `QA_RUBRIC.md` is passed
or explicitly escalated according to `POLICY.md`.
