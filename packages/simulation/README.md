# @economic-models/simulation

Simulation engine for running economic models and analyzing their dynamics.

## Ownership
**Team:** Computational Economics
**Lead:** TBD
**Slack:** #team-computational-econ

## Purpose

This package provides:
- Numerical solvers (ODE, PDE, difference equations)
- Monte Carlo simulation
- Impulse response functions
- Shock simulation
- Sensitivity analysis
- Calibration algorithms
- Parallel execution for complex models

## Key Exports

```typescript
// Simulation runner
export class SimulationEngine { ... }

// Solvers
export class ODESolver { ... }
export class MonteCarloSimulator { ... }

// Analysis
export function computeImpulseResponse(model, shock, horizon): TimeSeries
export function sensitivityAnalysis(model, parameters): SensitivityResult
```

## Dependencies

- `@economic-models/core` - Base types
- `@economic-models/models` - Model implementations
- `mathjs` - Mathematical operations

## Dependents

- `@economic-models/analysis` - Uses simulation results
- `apps/api` - Runs simulations on request
- `apps/web` - Interactive simulations

## Getting Started

```bash
cd packages/simulation
npm install
npm run dev
npm run test
```

## Directory Structure

```
src/
├── solvers/            # Numerical solvers
│   ├── ode.ts          # ODE solvers (Runge-Kutta, etc.)
│   ├── pde.ts          # PDE solvers
│   └── optimization.ts # Optimization algorithms
├── monte-carlo/        # Monte Carlo simulation
├── impulse-response/   # IRF computation
├── calibration/        # Calibration algorithms
├── sensitivity/        # Sensitivity analysis
└── engine/             # Main simulation orchestration
```

## Development Guidelines

### Adding a New Solver

1. Implement solver interface
2. Add numerical accuracy tests
3. Benchmark performance
4. Document algorithm and parameters
5. Add usage examples

### Performance Considerations

- Use typed arrays for large simulations
- Implement worker pool for parallel execution
- Cache intermediate results when possible
- Profile before optimizing

## Testing

- Test against known analytical solutions
- Verify numerical convergence
- Test edge cases (stability, convergence)
- Performance benchmarks for large simulations

## Examples

```typescript
import { SimulationEngine } from '@economic-models/simulation'
import { SolowGrowthModel } from '@economic-models/models'

const model = new SolowGrowthModel(params)
const engine = new SimulationEngine(model)

const result = await engine.simulate({
  horizon: 100,
  shocks: [{ period: 10, variable: 'technology', magnitude: 0.05 }]
})
```

## API Stability

⚠️ **Alpha** - API under active development.
