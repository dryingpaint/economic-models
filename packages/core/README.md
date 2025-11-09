# @economic-models/core

Core types, interfaces, and utilities for the economic models platform.

## Purpose

This package provides the foundational types and utilities used across all other packages. It defines:
- Base model interfaces and types
- Common economic data structures
- Utility functions
- Type validators and schemas
- Error handling patterns

## Key Exports

```typescript
// Model definitions
export interface EconomicModel { ... }
export interface ModelParameter { ... }
export interface ModelState { ... }

// Time series data
export interface TimeSeries { ... }
export interface DataPoint { ... }

// Validators
export const modelSchema: z.ZodSchema<EconomicModel>
```

## Dependencies

**None** - This is a foundational package with no internal dependencies.

## Dependents

All other packages depend on `@economic-models/core`.

## Getting Started

```bash
cd packages/core
npm install
npm run dev  # Start development mode with watch
npm run test # Run tests
```

## Directory Structure

```
src/
├── types/          # TypeScript type definitions
├── schemas/        # Zod validation schemas
├── utils/          # Utility functions
├── constants/      # Platform-wide constants
└── errors/         # Error classes and handling
```

## Development Guidelines

- **All types must be exported** from `src/index.ts`
- Use Zod for runtime validation schemas
- Keep utilities pure and well-tested
- Document all public APIs with JSDoc
- Breaking changes require major version bump

## Testing

Tests should cover:
- Type validation with Zod schemas
- Utility function edge cases
- Error handling behavior

## API Stability

⚠️ **Alpha** - API may change frequently. Coordinate with dependent teams before breaking changes.
