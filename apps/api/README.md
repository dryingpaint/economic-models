# economic-models-api

FastAPI server exposing Python backend to frontend.

## Purpose

REST API for:
- Running simulations
- Fetching data
- Policy analysis
- Model catalog

## Tech Stack

- **FastAPI** - Modern Python API framework
- **Pydantic** - Request/response validation
- **Uvicorn** - ASGI server

## Structure

```
src/
├── routes/
│   ├── models.py       # GET /api/models
│   ├── simulate.py     # POST /api/simulate
│   ├── data.py         # GET /api/data
│   └── analyze.py      # POST /api/analyze
├── schemas/            # Pydantic models
└── main.py             # App entry
```

## Development

```bash
# Install
uv pip install -e .

# Run server
uvicorn src.main:app --reload

# Visit http://localhost:8000/docs for API docs
```

## Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SimulateRequest(BaseModel):
    model_id: str
    parameters: dict[str, float]
    horizon: int

@app.post("/api/simulate")
async def simulate(request: SimulateRequest):
    # Run simulation
    return {"result": [...]}
```

## Code Standards

- Max 300-400 lines per file
- Pydantic for all validation
- Async where beneficial
- Clear error responses
- API versioning via routes

## API Documentation

Auto-generated at `/docs` (Swagger UI) and `/redoc`
