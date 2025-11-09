# Architecture

## Overview

Modular TypeScript monorepo enabling parallel development across teams.

## Package Structure

```
Layer 1: core (types, utilities)
Layer 2: models, data, visualization (domain logic)
Layer 3: simulation, ui-components (computation)
Layer 4: analysis (statistical methods)
Layer 5: web, api (applications)
```

**Rule:** Packages only depend on lower layers.

## Key Principles

1. **Framework-agnostic core** - Core packages work in any JS environment
2. **Clear interfaces** - Well-defined APIs between packages
3. **Type safety** - Strict TypeScript, runtime validation with Zod
4. **Independent development** - Teams can work in parallel

## Package Responsibilities

| Package | Purpose | Key Dependencies |
|---------|---------|------------------|
| `core` | Base types, utilities | None |
| `models` | Economic model implementations | core |
| `simulation` | Numerical solvers, simulation engine | core, models, data |
| `visualization` | Charts and graphs (D3/Plotly) | core |
| `data` | External data sources (FRED, etc.) | core |
| `analysis` | Statistical analysis, policy tools | core, models, simulation, data |
| `ui-components` | React components | core, visualization |
| `web` | Next.js application | All packages |
| `api` | Express REST API | All except ui-components |

## Development Workflow

1. Core team defines interfaces
2. Other teams build in parallel using those interfaces
3. Integration happens continuously via CI

## Build System

- **npm workspaces** for package management
- **Turbo** for incremental builds and caching
- **TypeScript project references** for fast rebuilds

## For More Details

See individual package READMEs for specific interfaces and usage.
