# Economic Models Platform

A comprehensive platform for understanding, analyzing, and simulating economic models. Built to enable parallel development across research, engineering, and design teams.

## Overview

This platform provides:
- **Interactive Model Library** - Explore classic and modern economic models
- **Simulation Engine** - Run real-time simulations with custom parameters
- **Data Integration** - Connect to real-world economic data (FRED, World Bank, IMF, OECD)
- **Analysis Tools** - Policy analysis, comparative statics, welfare analysis
- **Educational Content** - Learn economic theory with interactive visualizations
- **Research Platform** - Build, test, and share your own models

## Architecture

**Hybrid Python/TypeScript stack** - Best tool for each job.

```
economic-models/
├── packages/
│   # Python packages (scientific computing)
│   ├── models/            # Economic models (Python + NumPy/SciPy)
│   ├── simulation/        # Simulation engine (Python)
│   ├── analysis/          # Statistical analysis (Python + Pandas)
│   ├── data/              # Data integration (Python)
│
│   # TypeScript packages (UI/visualization)
│   ├── core/              # Shared TypeScript types
│   ├── visualization/     # Charts (D3/Plotly)
│   └── ui-components/     # React components
│
├── apps/
│   ├── api/               # FastAPI server (Python)
│   └── web/               # Next.js frontend (TypeScript)
│
└── docs/
```

**Why hybrid?**
- Python for numerical computing (NumPy, SciPy, Pandas)
- TypeScript for type-safe UI development
- Best performance and ecosystem for each domain

## Quick Start

### Prerequisites

- **Python 3.11+** and `uv` ([install](https://github.com/astral-sh/uv))
- **Node.js 18+** and npm 9+
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd economic-models

# Install Python dependencies
uv pip install -e .

# Install TypeScript dependencies
npm install && npm run build

# Start development
# Terminal 1: Python API
uvicorn apps.api.src.main:app --reload  # http://localhost:8000

# Terminal 2: Next.js frontend
cd apps/web && npm run dev  # http://localhost:3000
```

## Development Workflow

### For Engineers Working in Parallel

Each package has clear interfaces and can be developed independently:

1. **Choose your component** - See package READMEs for ownership and interfaces
2. **Install dependencies** - `cd packages/[your-package] && npm install`
3. **Start development** - `npm run dev` (runs in watch mode)
4. **Write tests** - `npm run test`
5. **Check types** - `npm run type-check`

### Package Dependency Graph

```
core (no dependencies)
  ├─→ models
  ├─→ data
  └─→ visualization
       └─→ ui-components

models + data
  └─→ simulation
       └─→ analysis

All packages
  └─→ web, api
```

**Key principle:** Packages only depend on packages above them in the tree. This enables parallel development.

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes in your assigned package
cd packages/your-package

# Run tests
npm run test

# Type check
npm run type-check

# Build
npm run build

# From root - verify integration
cd ../..
npm run build
npm run test
```

### Creating Pull Requests

```bash
# Commit with conventional commits format
git add .
git commit -m "feat(models): add Solow growth model"

# Push your branch
git push -u origin feature/your-feature-name

# Create PR on GitHub targeting 'main' branch
```

**Commit format:** `<type>(<package>): <description>`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Package: `core`, `models`, `simulation`, etc.

**PR checklist:**
- [ ] Tests pass (`npm run test`)
- [ ] Types check (`npm run type-check`)
- [ ] Code formatted (`npm run format`)
- [ ] Package README updated if needed
- [ ] Clear description of changes

## Project Structure by Team

### Python Teams

**Economic Research** → `packages/models` (Python)
- Implement economic models using NumPy/SciPy
- Solow, DSGE, RBC, game theory models

**Computational Economics** → `packages/simulation` (Python)
- Numerical solvers, ODE/PDE
- Monte Carlo, calibration

**Economic Analysis** → `packages/analysis` (Python)
- Policy analysis, comparative statics
- Statistical tests with Pandas

**Data Engineering** → `packages/data` (Python)
- FRED, World Bank, IMF integrations
- Data preprocessing

**Backend Engineering** → `apps/api` (Python FastAPI)
- REST API endpoints
- Request validation

### TypeScript Teams

**Platform Infrastructure** → `packages/core` (TypeScript)
- Shared types and utilities

**Data Visualization** → `packages/visualization` (TypeScript)
- D3/Plotly chart implementations

**Frontend Engineering** → `packages/ui-components` (TypeScript)
- React component library

**Web Platform** → `apps/web` (TypeScript Next.js)
- User-facing web application

## Communication Channels

- **Slack Channels:** See individual package READMEs for team-specific channels
- **Sync Meetings:** Architecture Council (weekly), Team standups (daily)
- **Async:** GitHub Discussions for proposals, GitHub Issues for bugs/features

## Testing Strategy

### Unit Tests
Each package has its own tests:
```bash
cd packages/[package-name]
npm run test
```

### Integration Tests
Run from root to test package interactions:
```bash
npm run test
```

### E2E Tests
Test full application flows:
```bash
cd apps/web
npm run test:e2e
```

## Documentation

- **Architecture Docs:** `docs/architecture/`
- **API Reference:** Auto-generated from code
- **User Guides:** `docs/guides/`
- **Contributing:** `CONTRIBUTING.md`
- **Package Docs:** See individual `packages/*/README.md`

## Scripts

```bash
npm run dev          # Start all apps in development mode
npm run build        # Build all packages and apps
npm run test         # Run all tests
npm run lint         # Lint all packages
npm run type-check   # Type check all packages
npm run clean        # Clean all build artifacts
npm run format       # Format code with Prettier
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

Quick checklist:
- [ ] Create feature branch from `main`
- [ ] Write tests for new functionality
- [ ] Update relevant documentation
- [ ] Run `npm run type-check` and `npm run test`
- [ ] Create PR with clear description
- [ ] Request review from package owner
- [ ] Address feedback
- [ ] Squash and merge

## License

TBD

## Support

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** [team email]

## Roadmap

See [ROADMAP.md](./docs/ROADMAP.md) for planned features and timeline.

---

Built with love by economists and engineers who believe economic models should be accessible to everyone.