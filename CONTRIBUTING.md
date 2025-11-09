# Contributing Guide

Thank you for contributing to the Economic Models Platform! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Package Structure](#package-structure)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Review Guidelines](#review-guidelines)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## Getting Started

### Prerequisites

- Node.js 18+ and npm 9+
- Git
- TypeScript knowledge
- Familiarity with the relevant domain (economics, data viz, etc.)

### Initial Setup

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/YOUR_USERNAME/economic-models.git
cd economic-models

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/economic-models.git

# Install dependencies
npm install

# Build all packages
npm run build

# Run tests to ensure everything works
npm run test
```

## Development Workflow

### 1. Pick an Issue or Feature

- Browse GitHub Issues for open tasks
- Comment on the issue to claim it
- If no issue exists, create one first to discuss your idea
- Get approval from package owner before starting large changes

### 2. Create a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/fixes

### 3. Make Changes

- Work in the appropriate package directory
- Follow coding standards (see below)
- Write tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# In your package directory
npm run test        # Unit tests
npm run type-check  # Type checking
npm run lint        # Linting

# From root - test integration
npm run build       # Ensure builds work
npm run test        # Run all tests
```

### 5. Commit Your Changes

We use conventional commits:

```bash
git add .
git commit -m "feat(models): add Ramsey growth model"
```

Commit message format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting, missing semicolons, etc.
- `refactor` - Code restructuring
- `test` - Adding tests
- `chore` - Maintenance

Scopes (package names):
- `core`, `models`, `simulation`, `visualization`, `data`, `analysis`, `ui-components`, `web`, `api`

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Package Structure

Each package should follow this structure:

```
package-name/
├── src/
│   ├── index.ts        # Main exports
│   ├── types/          # Type definitions
│   └── ...
├── tests/              # Test files
├── package.json
├── tsconfig.json
└── README.md           # Package documentation
```

## Coding Standards

### TypeScript

- **Strict mode enabled** - No `any` types unless absolutely necessary
- **Explicit types** - Type function parameters and return values
- **JSDoc comments** - Document all public APIs
- **Interfaces over types** - Use interfaces for object shapes

Example:
```typescript
/**
 * Calculates the steady state of the Solow growth model.
 *
 * @param params - Model parameters
 * @returns Steady state values for capital and output
 */
export function calculateSteadyState(
  params: SolowParameters
): SteadyState {
  // Implementation
}
```

### Code Style

- Use Prettier for formatting (run `npm run format`)
- 2 spaces for indentation
- Single quotes for strings
- Semicolons required
- Max line length: 100 characters

### File Naming

- `kebab-case` for files: `solow-model.ts`
- `PascalCase` for classes: `class SolowModel`
- `camelCase` for functions/variables: `calculateGrowthRate`
- `UPPER_SNAKE_CASE` for constants: `DEFAULT_SAVINGS_RATE`

### Imports

Order imports:
1. External packages
2. Internal packages (from workspace)
3. Relative imports

```typescript
import { z } from 'zod'                          // External
import { EconomicModel } from '@economic-models/core'  // Internal
import { calculateSteadyState } from './utils'   // Relative
```

## Testing Requirements

### Unit Tests

- **Required** for all new functionality
- Use Vitest
- Aim for >80% coverage
- Test edge cases and error conditions

Example:
```typescript
import { describe, it, expect } from 'vitest'
import { SolowModel } from './solow-model'

describe('SolowModel', () => {
  it('should calculate steady state correctly', () => {
    const model = new SolowModel({
      savingsRate: 0.2,
      depreciationRate: 0.05,
      // ...
    })

    const steadyState = model.calculateSteadyState()

    expect(steadyState.capital).toBeCloseTo(expectedValue, 5)
  })

  it('should throw error for invalid parameters', () => {
    expect(() => {
      new SolowModel({ savingsRate: -0.1 })
    }).toThrow()
  })
})
```

### Integration Tests

- Test interactions between packages
- Ensure APIs work as documented

### Documentation Tests

- Code examples in README should work
- Keep examples up to date

## Pull Request Process

### Before Creating PR

- [ ] All tests pass (`npm run test`)
- [ ] Type checking passes (`npm run type-check`)
- [ ] Code is formatted (`npm run format`)
- [ ] Linting passes (`npm run lint`)
- [ ] Documentation is updated
- [ ] CHANGELOG is updated (for significant changes)

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2

## Testing
Describe testing performed

## Screenshots (if applicable)

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Type checking passes
- [ ] All tests pass
```

### PR Size

- Keep PRs focused and reasonably sized
- Large changes should be discussed first
- Break down large features into smaller PRs

## Review Guidelines

### For Authors

- Respond to feedback promptly
- Be open to suggestions
- Ask for clarification if needed
- Mark resolved conversations

### For Reviewers

- Review within 48 hours
- Be constructive and respectful
- Test the changes locally if needed
- Approve when satisfied

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are comprehensive
- [ ] Documentation is clear
- [ ] No unnecessary dependencies added
- [ ] Performance considerations addressed
- [ ] Security implications considered
- [ ] Backwards compatibility maintained (or breaking change noted)

## Package-Specific Guidelines

### @economic-models/models

- Include references to papers/textbooks
- Provide mathematical equations in comments
- Test against analytical solutions when available
- Add model to catalog

### @economic-models/simulation

- Benchmark performance for new solvers
- Document numerical methods used
- Test convergence properties

### @economic-models/visualization

- Ensure accessibility (color blindness, screen readers)
- Test on multiple screen sizes
- Provide export functionality

### @economic-models/data

- Never commit API keys
- Implement proper rate limiting
- Add caching for external API calls

### @economic-models/ui-components

- Add Storybook stories
- Test accessibility
- Ensure responsive design

## Questions?

- Check existing Issues and Discussions
- Ask in relevant Slack channel (see package READMEs)
- Create a GitHub Discussion for general questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to making economic models more accessible!
