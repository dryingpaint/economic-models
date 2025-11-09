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

This is a TypeScript monorepo using npm workspaces and Turbo for build orchestration.

```
economic-models/
├── packages/              # Shared packages (can be developed in parallel)
│   ├── core/              # Base types and utilities
│   ├── models/            # Economic model implementations
│   ├── simulation/        # Simulation engine and solvers
│   ├── visualization/     # Visualization library (framework-agnostic)
│   ├── data/              # Data integration and management
│   ├── analysis/          # Analysis tools and methods
│   └── ui-components/     # React UI components
│
├── apps/                  # Applications
│   ├── web/               # Next.js web application
│   └── api/               # Express.js REST API
│
└── docs/                  # Documentation
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm 9+
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd economic-models

# Install dependencies
npm install

# Build all packages
npm run build

# Start development
npm run dev
```

This will start:
- Web app on `http://localhost:3000`
- API server on `http://localhost:3001`

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

### Team: Platform Infrastructure
**Package:** `@economic-models/core`
**Responsibilities:** Base types, utilities, validation schemas

### Team: Economic Research
**Package:** `@economic-models/models`
**Responsibilities:** Implement economic models, maintain model catalog

### Team: Computational Economics
**Package:** `@economic-models/simulation`
**Responsibilities:** Numerical solvers, simulation engine, optimization

### Team: Data Visualization
**Package:** `@economic-models/visualization`
**Responsibilities:** Chart implementations, export tools, themes

### Team: Data Engineering
**Package:** `@economic-models/data`
**Responsibilities:** Data source integrations, caching, preprocessing

### Team: Economic Analysis
**Package:** `@economic-models/analysis`
**Responsibilities:** Analysis methods, statistical tests, validation

### Team: Frontend Engineering
**Package:** `@economic-models/ui-components`
**Responsibilities:** React components, hooks, Storybook

### Team: Web Platform
**App:** `apps/web`
**Responsibilities:** Next.js web application, UX, pages

### Team: Backend Engineering
**App:** `apps/api`
**Responsibilities:** REST API, authentication, data persistence

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