# @economic-models/analysis

Analysis tools and methods for economic models and empirical data.

## Ownership
**Team:** Economic Analysis
**Lead:** TBD
**Slack:** #team-economic-analysis

## Purpose

This package provides analytical tools:
- Comparative statics
- Policy analysis and scenario comparison
- Welfare analysis
- Counterfactual simulation
- Statistical testing
- Model validation
- Forecasting

## Key Exports

```typescript
// Analysis tools
export class ComparativeStaticsAnalyzer { ... }
export class PolicyAnalyzer { ... }
export class WelfareAnalyzer { ... }

// Statistical methods
export function runGrangerCausality(data): TestResult
export function structuralBreakTest(data): TestResult

// Validation
export function validateModel(model, empiricalData): ValidationResult
```

## Dependencies

- `@economic-models/core` - Base types
- `@economic-models/models` - Model implementations
- `@economic-models/simulation` - Run simulations
- `@economic-models/data` - Empirical data
- `simple-statistics` - Statistical functions

## Dependents

- `apps/api` - Analysis endpoints
- `apps/web` - Analysis UI

## Getting Started

```bash
cd packages/analysis
npm install
npm run dev
npm run test
```

## Directory Structure

```
src/
├── comparative-statics/ # Comparative statics analysis
├── policy/              # Policy analysis tools
├── welfare/             # Welfare analysis
├── counterfactual/      # Counterfactual simulations
├── validation/          # Model validation
├── forecasting/         # Forecasting methods
└── statistics/          # Statistical tests
```

## Development Guidelines

### Adding a New Analysis Method

1. Implement analysis class or function
2. Add theoretical documentation (what method does)
3. Include references to academic literature
4. Write comprehensive tests
5. Add usage examples
6. Document assumptions and limitations

### Statistical Rigor

- Always report confidence intervals
- Document assumptions clearly
- Provide diagnostic tests
- Include sensitivity analysis

## Testing

- Test against known results from academic papers
- Validate statistical properties
- Test edge cases and robustness
- Integration tests with real models

## Examples

```typescript
import { PolicyAnalyzer } from '@economic-models/analysis'
import { DSGEModel } from '@economic-models/models'

const model = new DSGEModel(params)
const analyzer = new PolicyAnalyzer(model)

const comparison = await analyzer.compareScenarios({
  baseline: { taxRate: 0.2 },
  policy: { taxRate: 0.25 }
})

console.log(comparison.welfareEffect)
```

## API Stability

⚠️ **Alpha** - Analysis methods being refined based on research needs.
