Generates user-readable insights from OHLC data.

Analysis Logic
1. A cluster of exponential moving averages (EMAs) at spans 8-13-21 are computed for momentum comparisons.
2. The configuration and degree of spread from EMA cluster indicates potential momentum.
3. The alignment and distance of Open-High-Low-Close (OHLC) against EMA cluster validates trend assumptions.

Service Architecture
Dev site auto-request <-> FastAPI CRUD in K8s pod <-> Daily-updated Postgres DB <-> Python data workflow