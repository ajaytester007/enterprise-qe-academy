# Enterprise QE Academy v4

Enterprise QE Academy v4 introduces a platform-core layer above the existing catalog and practice scripts.

## Modules

- Knowledge Engine: converts catalog rows into structured knowledge nodes.
- Domain Packs: groups scenarios by business domain.
- Adaptive Interview Simulator: asks one question, scores the answer, and recommends follow-up improvement.
- Coding Lab Scaffold: creates starter-code manifests for future Monaco/editor integration.
- Whiteboard Studio Scaffold: creates architecture/design exercise manifests.
- Learning Analytics: summarizes coverage by domain, role, category, and difficulty.

## Local generation

```powershell
python .\scripts\generate_v4_platform_core.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --limit 250
python .\scripts\generate_v4_portal_pages.py
```
