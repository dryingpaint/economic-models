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
- **Node.js 18+** and pnpm
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd economic-models

# Start everything with one command!
pnpm run dev
```

This will:
- Install all Python dependencies (via `uv`)
- Install all TypeScript dependencies (via `pnpm`)
- Build all TypeScript packages
- Start the FastAPI backend at http://localhost:8000
- Start the Next.js frontend at http://localhost:3000

**Alternative commands:**
```bash
# Just run setup without starting servers
pnpm run dev:setup

# Start frontend dev servers only (after setup)
pnpm run dev:frontend
```

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes in your assigned package
cd packages/your-package

# Run tests
pnpm run test

# Type check
pnpm run type-check

# Build
pnpm run build

# From root - verify integration
cd ../..
pnpm run build
pnpm run test
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
- [ ] Tests pass (`pnpm run test`)
- [ ] Types check (`pnpm run type-check`)
- [ ] Code formatted (`pnpm run format`)
- [ ] Package README updated if needed
- [ ] Clear description of changes

## Testing Strategy

### Unit Tests
Each package has its own tests:
```bash
cd packages/[package-name]
pnpm run test
```

### Integration Tests
Run from root to test package interactions:
```bash
pnpm run test
```

### E2E Tests
Test full application flows:
```bash
cd apps/web
pnpm run test:e2e
```

## Documentation

- **Architecture Docs:** `docs/architecture/`
- **API Reference:** Auto-generated from code
- **User Guides:** `docs/guides/`
- **Contributing:** `CONTRIBUTING.md`
- **Package Docs:** See individual `packages/*/README.md`

## Scripts

```bash
pnpm run dev          # Start all apps in development mode
pnpm run build        # Build all packages and apps
pnpm run test         # Run all tests
pnpm run lint         # Lint all packages
pnpm run type-check   # Type check all packages
pnpm run clean        # Clean all build artifacts
pnpm run format       # Format code with Prettier
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

Quick checklist:
- [ ] Create feature branch from `main`
- [ ] Write tests for new functionality
- [ ] Update relevant documentation
- [ ] Run `pnpm run type-check` and `pnpm run test`
- [ ] Create PR with clear description
- [ ] Request review from package owner
- [ ] Address feedback
- [ ] Squash and merge
