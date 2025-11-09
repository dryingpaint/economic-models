# Architecture

## Overview

**Hybrid Python/TypeScript stack** - Python for scientific computing, TypeScript for UI.

## Stack Rationale

### Python (Backend/Computation)
- **NumPy/SciPy** - Industry standard for numerical computing
- **Pandas** - Data manipulation
- **FastAPI** - Modern, fast Python API framework
- **Performance** - Better than JS for numerical work
- **Ecosystem** - Rich scientific/economic libraries

### TypeScript (Frontend)
- **Type safety** - Catch errors at compile time
- **Next.js** - Modern React framework
- **D3/Plotly** - Best-in-class visualization
- **Rich UI ecosystem**

## Package Structure

```
Layer 1: core (TypeScript types)
Layer 2: models, data, simulation, analysis (Python)
         visualization (TypeScript)
Layer 3: ui-components (TypeScript)
Layer 4: api (Python FastAPI), web (TypeScript Next.js)
```

## Package Responsibilities

| Package | Language | Purpose |
|---------|----------|---------|
| `core` | TypeScript | Shared types |
| `models` | Python | Economic models (NumPy/SciPy) |
| `simulation` | Python | Numerical solvers |
| `data` | Python | Data sources (FRED, etc.) |
| `analysis` | Python | Statistical analysis (Pandas) |
| `visualization` | TypeScript | Charts (D3/Plotly) |
| `ui-components` | TypeScript | React components |
| `api` | Python | FastAPI server |
| `web` | TypeScript | Next.js app |

## Communication

**Python ←→ TypeScript:** FastAPI REST endpoints

```
TypeScript Frontend → HTTP → FastAPI Backend → Python Models
```

## Development Workflow

1. Python teams build models/analysis independently
2. TypeScript teams build UI independently
3. Integration via API contracts

## Build System

- **Python:** `uv` for fast dependency management
- **TypeScript:** npm workspaces + Turbo
- **Testing:** pytest (Python), vitest (TypeScript)
- **Linting:** ruff + mypy (Python), eslint (TypeScript)

## Key Principles

1. **Simple over clever** - Clean, readable code
2. **Small files** - Max 300-400 lines
3. **Type safety** - Python type hints, TypeScript strict mode
4. **Test everything** - Unit tests required
5. **No over-engineering** - Use language idioms
