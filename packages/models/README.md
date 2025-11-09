# @economic-models/models

Economic model implementations and library.

## Ownership
**Team:** Economic Research
**Lead:** TBD
**Slack:** #team-economic-research

## Purpose

This package contains implementations of economic models including:
- Macroeconomic models (Solow, IS-LM, DSGE)
- Microeconomic models (Supply/Demand, Market equilibrium)
- Game theory models (Nash equilibrium, evolutionary games)
- Behavioral economics models
- Agent-based models (ABM)

## Key Exports

```typescript
// Model classes
export class SolowGrowthModel implements EconomicModel { ... }
export class ISLMModel implements EconomicModel { ... }
export class DSGEModel implements EconomicModel { ... }

// Model factory
export function createModel(type: ModelType, config: ModelConfig): EconomicModel

// Model catalog
export const MODEL_CATALOG: ModelCatalogEntry[]
```

## Dependencies

- `@economic-models/core` - Base types and interfaces

## Dependents

- `@economic-models/simulation` - Runs these models
- `@economic-models/analysis` - Analyzes model outputs
- `apps/web` - Displays model information

## Getting Started

```bash
cd packages/models
npm install
npm run dev
npm run test
```

## Directory Structure

```
src/
├── macroeconomic/      # Macro models (Solow, RBC, DSGE, etc.)
├── microeconomic/      # Micro models (supply/demand, etc.)
├── game-theory/        # Game theoretic models
├── behavioral/         # Behavioral economics models
├── agent-based/        # ABM implementations
├── catalog/            # Model metadata and catalog
└── factory/            # Model creation utilities
```

## Development Guidelines

### Adding a New Model

1. Create model class implementing `EconomicModel` interface
2. Add comprehensive JSDoc documentation
3. Include mathematical equations in comments
4. Write unit tests with known analytical solutions
5. Add model to catalog with metadata
6. Update this README

### Model Implementation Checklist

- [ ] Implements `EconomicModel` interface from `@economic-models/core`
- [ ] Parameters validated with Zod schemas
- [ ] Initial state computation
- [ ] Step/update function for dynamics
- [ ] Steady-state calculation (if applicable)
- [ ] Unit tests with analytical benchmarks
- [ ] JSDoc with references to papers/textbooks

## Testing

- Test against known analytical solutions
- Verify steady-state calculations
- Test parameter boundary conditions
- Validate numerical stability

## Examples

```typescript
import { SolowGrowthModel } from '@economic-models/models'

const model = new SolowGrowthModel({
  savingsRate: 0.2,
  depreciationRate: 0.05,
  populationGrowth: 0.01,
  technologyGrowth: 0.02,
  alpha: 0.33
})

const steadyState = model.computeSteadyState()
```

## API Stability

⚠️ **Alpha** - API may change. Each model should maintain backward compatibility when possible.
