# ARCHITECTURE.md

## Goal
Build {{PROJECT_NAME}} as an agent-legible codebase with strong boundaries, a short instruction surface, and enough extension seams to support future change without overbuilding v1.

## System Overview
{{PROJECT_NAME}} is a web application with:
{{SYSTEM_OVERVIEW_BULLETS}}

## Architectural Priorities
{{ARCHITECTURAL_PRIORITIES_BULLETS}}

## Layered Domain Model
Use a strict forward-only dependency shape inside each domain:

`Types -> Config -> Repo -> Service -> Runtime -> UI`

### Why this matters
The repository is intended to work well with long-running agent loops. Strict boundaries reduce accidental coupling and make failure analysis easier.

## Primary Domains
{{PRIMARY_DOMAINS_MARKDOWN}}

## Frontend / Backend Shape
### Frontend
{{FRONTEND_SHAPE_BULLETS}}

### Server
{{SERVER_SHAPE_BULLETS}}

## Persistence Strategy
{{PERSISTENCE_STRATEGY_BULLETS}}

## Verification Shape
{{VERIFICATION_SHAPE_BULLETS}}

## Long-Running Agent Readiness
- docs are the system of record
- plans are executable, not aspirational
- domain boundaries are explicit
- repeated issues should be upgraded into tests or static checks
