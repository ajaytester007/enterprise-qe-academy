# Enterprise QE Academy v5

v5 introduces the first interactive platform layer on top of the v4 knowledge, quality, content, and JD readiness engines.

## Capabilities

- Interactive static web portal
- Interview simulator launch surface
- JD readiness review surface
- Quality intelligence review surface
- GitHub Pages-compatible build output
- Backend-ready session-state model

## Build

```powershell
python .\scripts\build_v5_static_platform.py
```

## Preview

```powershell
python -m http.server 8000 -d outputs/v5/site
```

## Output

```text
outputs/v5/site/index.html
outputs/v5/site/data/platform-data.json
```

## Next recommended v5 enhancements

- FastAPI backend
- Persistent SQLite/Postgres session store
- Monaco coding lab
- Mermaid whiteboard viewer
- AI coaching integration
