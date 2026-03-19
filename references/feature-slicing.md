# Feature Slicing

Use this reference when turning founder answers into product specs and executable task contracts.

## Core Rule

Do not collapse multiple user-visible features into one “first slice” unless the product truly has only one user-visible behavior.

Each distinct feature area should normally get:

- its own product spec under `docs/product-specs/`
- one or more small executable tasks under `docs/exec-plans/active/`

## What Counts As A Distinct Feature

Treat these as separate feature fronts unless there is a very strong reason to combine them:

- auth and invite acceptance
- note creation or editing
- source capture or attachment
- search or retrieval
- sharing or public read surfaces
- AI-powered behaviors
- uploads or media handling

## Task Sizing Rule

One task should cover at most:

- one user-visible feature slice
- plus the smallest enabling work required to make that slice real

Do not create a task that mixes several independent user-visible features just because they all belong to “v1”.

## Minimum Mapping Rule

Before writing executable tasks, create or update the feature-spec list.

If the repo has multiple in-scope user-visible features:

- the product-specs index should list them explicitly
- the active queue should sequence them explicitly
- the first executable task should not try to finish all of them at once

## External Resource Rule

If a feature depends on an outside resource such as auth, email invite delivery, AI tagging, or a third-party API:

- keep that feature in its own spec or task unless the dependency is trivial
- require its relevant end-to-end scenario before promotion

## Smell Checks

Your slicing is probably too broad if any one task:

- changes multiple major routes for different feature areas
- requires more than one product spec to understand its success condition
- has exit criteria that read like a mini-roadmap
- mixes account/auth work with content features and search/retrieval
- mixes sharing, search, and AI into one “core value” task
