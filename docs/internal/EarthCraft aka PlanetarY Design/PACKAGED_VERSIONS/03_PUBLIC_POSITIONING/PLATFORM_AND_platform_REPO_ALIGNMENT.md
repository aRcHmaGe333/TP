# TTP Repo: What's What

## Repository Roles
1. `C:\Users\archm\code\TP\docs\internal`
- Strategy, source materials, design documents, concept evolution.

2. `C:\Users\archm\code\TP`
- Running implementation prototype (FastAPI + web UI).

3. `C:\Users\archm\code\TP\docs\internal_P`
- Public-facing positioning package (business-safe language).

## Alignment Summary
- Concept direction in `ThePlatform` broadly aligns with implemented MVP primitives in `platform`.
- `platform` implements: identity, signed submissions, merge, voting, comments, sortable feed.
- `ThePlatform` docs include additional scope not yet implemented: lifecycle governance, richer audit/reporting, geo boards, stronger compliance surfaces.

## Segment File Note
- `segment_000.md` exists in both `ThePlatform\EarthCraft aka PlanetarY Design` and `platform`.
- Both currently have `2621` lines, but hashes differ due to encoding/text normalization differences.
- Operationally, they represent the same source conversation lineage.

## Recommended Working Model
1. Keep `ThePlatform` as internal strategy/doctrine workspace.
2. Treat `platform` as implementation track.
3. Use `docs/public` as external communication and partner onboarding track.
4. Sync via periodic alignment notes so narrative and implementation do not drift.


