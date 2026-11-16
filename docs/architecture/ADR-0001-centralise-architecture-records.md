# ADR-0001 — Centralise architecture records in docs/architecture

- **Date:** 2026-11-16.
- **Status:** authorised documentation organisation; implemented by this documentation change.
- **Authority:** François’s current request to locate and group ADRs and recursively refactor dependent documentation.
- **Scope:** documentation paths, navigation and historical/current interpretation. Business rules, schemas, company states and release gates retain their owning authorities.

## Context

Architecture choices are embedded in the programme design, Sphere loopback and cross-repository audit. They sit in two directories and lack a common register. Current readers also encounter historical descriptions of capabilities that have since been implemented.

## Decision

Use the established `docs/architecture/` directory as the canonical location for architecture records. Move the three source documents with their original filenames and unchanged text. Keep short compatibility pages at their previous paths so historical handoffs and generated company dossiers remain navigable.

Maintain an [architecture register](README.md) that distinguishes current views, historical choices and this documentation decision. Link current behaviour to schemas, code and tests. Record later interpretation beside the historical material in the register, preserving the original source language and date.

## Options considered in this documentation pass

| Option | Effect | Assessment |
| --- | --- | --- |
| Leave records dispersed and add README links | Preserves paths; readers must distinguish history independently. | Weak discoverability and continued drift between summaries. |
| Centralise records, retain compatibility pages and add a register | One canonical collection with durable earlier paths. | Selected; introduces a small maintenance cost for the redirects. |
| Create a parallel `doc/architecture/` tree | Matches the singular spelling in the request. | Existing repository links and checks use `docs/`; a second tree would duplicate the navigation authority. |

## Consequences and boundaries

Readers can follow business intent → domain/data → rule → implementation → validation. Existing source and company artefact hashes remain stable. The register adds current annotations without retroactively accepting design proposals or claiming historical test results as current execution.

The compatibility pages must continue to resolve. Their continued existence is deliberate and makes literal references inside generated, hashed or external historical documents usable.

## Review trigger

Revisit the register when an architecture record is added outside this directory, a compatibility link breaks, or a successor changes a substantive recorded choice. The author of that change updates the register; the corresponding domain authority decides any business or runtime policy change.

## Sources

- [Programme design](PROGRAM_DESIGN.md).
- [Sphere loopback](LOOPBACK_SPHERE_V03.md).
- [Cross-repository audit](CROSS_REPO_AUDIT_AND_BOOTSTRAP_2026-11-04.md).
- [Current documentation guide](../README.md) and [industrialisation roadmap](../roadmap/industrialization-backlog.md).
