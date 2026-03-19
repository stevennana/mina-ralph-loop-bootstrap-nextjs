# RELIABILITY.md

## Purpose
Define the reliability expectations and failure-handling rules for {{PROJECT_NAME}}.

## Core Reliability Rules
{{RELIABILITY_RULES_BULLETS}}

## Verification
{{RELIABILITY_VERIFICATION_BULLETS}}

## Test Strategy
Document which behaviors are protected by unit tests, which flows require end-to-end coverage, and which command failures block task promotion.
When tests cover subtle or business-critical behavior, capture why those tests exist so future loops do not weaken them casually.
If a user-visible behavior depends on an outside resource such as AI chat or a third-party service, require end-to-end coverage before promotion.

## Known Gaps
{{RELIABILITY_GAPS_BULLETS}}
