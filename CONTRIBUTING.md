# Contributing Guide

## Core Principles

**CLEAN, SIMPLE, MAINTAINABLE CODE**

1. **Keep files small** - Max 300-400 lines per file
2. **Single responsibility** - One function, one purpose
3. **Clear names** - Code should be self-documenting
4. **Minimal abstraction** - Don't over-engineer
5. **DRY but readable** - Prefer clarity over cleverness

## Setup

```bash
npm install
npm run build
npm run test  # Should pass
source .venv/bin/activate
```

## Workflow

```bash
# 1. Create branch
git checkout -b feature/your-feature

# 2. Make changes in your package
cd packages/your-package

# 3. Test as you go
npm run test
npm run type-check

# 4. Commit frequently (see commit guidelines below)
git add .
git commit -m "feat(models): add feature"

# 5. Push and create PR
git push -u origin feature/your-feature
```

### Commit Guidelines

**Commit frequently** - Make small, incremental commits as you work. Each commit should represent a logical unit of work.

**Commit message format:**
- Use conventional commit format: `type(scope): description`
- Keep messages concise and descriptive
- Write in imperative mood ("add feature" not "added feature")
- Be professional - focus on what changed and why
- Examples:
  - `feat(models): add Solow growth model implementation`
  - `fix(simulation): correct steady state calculation`
  - `refactor(core): simplify model initialization`
  - `test(models): add unit tests for growth calculation`
  - `docs(readme): update installation instructions`

**Common types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks

## Code Standards

### File Size
- **Max 300-400 lines per file**
- If longer, split into multiple files
- Each file should have one clear purpose

### Python Imports
**CRITICAL: Always use full path imports, keep `__init__.py` empty**

```python
# GOOD: Full path imports
from packages.models.src.macroeconomic.solow import SolowGrowthModel
from packages.simulation.src.engine import SimulationEngine

# BAD: Relative imports or __init__.py exports
from src.macroeconomic.solow import SolowGrowthModel  # ❌
from ..solow import SolowGrowthModel  # ❌
```

**Why?**
- Eliminates import ambiguity in monorepo
- Works consistently across tests, apps, and packages
- Avoids Python path manipulation
- Clear dependency tracking

**`__init__.py` files:**
```python
# All __init__.py files should be empty or contain only:
# Empty - use full path imports
```

### TypeScript
```typescript
// GOOD: Clean, simple, typed
export function calculateGrowth(
  capital: number,
  rate: number
): number {
  return capital * rate
}

// BAD: Over-engineered
export class GrowthCalculator {
  private readonly calculator: ICalculationStrategy
  constructor(strategy: ICalculationStrategy) {
    this.calculator = strategy
  }
  calculate(input: GrowthInput): GrowthOutput {
    return this.calculator.execute(input)
  }
}
```

### Naming
- **Functions:** `calculateSteadyState`, `fetchData`
- **Variables:** `savingsRate`, `gdpData`
- **Types/Interfaces:** `EconomicModel`, `SimulationConfig`
- **Files:** `solow-model.ts`, `data-fetcher.ts`

### Functions
- Keep functions short (< 50 lines)
- One level of abstraction per function
- Clear inputs and outputs
- No side effects unless necessary

### Imports
```typescript
// External
import { z } from 'zod'

// Internal packages
import { EconomicModel } from '@economic-models/core'

// Relative
import { helper } from './utils'
```

## Testing

```typescript
// Simple, focused tests
describe('SolowModel', () => {
  it('calculates steady state correctly', () => {
    const model = new SolowModel({ savingsRate: 0.2 })
    const steadyState = model.calculateSteadyState()
    expect(steadyState.capital).toBeCloseTo(4.0, 2)
  })
})
```

- Test one thing per test
- Clear test names
- No complex setup - keep it simple

## Pull Requests

**Before submitting:**
- [ ] Tests pass
- [ ] Types check
- [ ] Code formatted
- [ ] Files < 400 lines
- [ ] No unnecessary complexity
- [ ] Commits are small and logical
- [ ] Commit messages are clear and professional

**Creating the PR:**
1. Push your branch: `git push -u origin your-branch-name`
2. Open a pull request against `main`
3. Write a concise PR description that:
   - Summarizes what changed
   - Explains why the change was needed
   - Notes any breaking changes or important details
   - Keep it brief but informative

**PR should:**
- Focus on one thing
- Have clear description
- Include tests
- Update relevant docs

## What to Avoid

❌ Over-abstraction (factories, builders, strategies for simple tasks)
❌ Long files (> 400 lines)
❌ Deep nesting (> 3 levels)
❌ Clever code (be obvious instead)
❌ Premature optimization
❌ Unnecessary dependencies

## What to Do

✅ Write simple, readable code
✅ Split large files into smaller ones
✅ Use TypeScript types effectively
✅ Test your code
✅ Document complex logic
✅ Keep it maintainable

## Questions?

- Check your package README
- Ask in team Slack channel
- Create GitHub Discussion
