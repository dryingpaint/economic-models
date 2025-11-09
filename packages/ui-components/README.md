# @economic-models/ui-components

Reusable React UI components for the economic models platform.

## Ownership
**Team:** Frontend Engineering
**Lead:** TBD
**Slack:** #team-frontend

## Purpose

This package provides React components:
- Model parameter controls
- Chart components (React wrappers for `@economic-models/visualization`)
- Model selector and browser
- Data input forms
- Results display components
- Educational content components

## Key Exports

```typescript
// Model components
export const ModelSelector: React.FC<ModelSelectorProps>
export const ParameterControl: React.FC<ParameterControlProps>

// Chart wrappers
export const TimeSeriesChart: React.FC<TimeSeriesChartProps>
export const PhaseDiagram: React.FC<PhaseDiagramProps>

// Layout components
export const ModelLayout: React.FC<ModelLayoutProps>
```

## Dependencies

- `@economic-models/core` - Base types
- `@economic-models/visualization` - Core visualization
- `react` - UI framework

## Dependents

- `apps/web` - Main web application

## Getting Started

```bash
cd packages/ui-components
npm install
npm run dev
npm run test
```

## Directory Structure

```
src/
├── model/              # Model-related components
├── charts/             # Chart wrapper components
├── controls/           # Input controls
├── layout/             # Layout components
├── educational/        # Educational content components
└── hooks/              # Custom React hooks
```

## Development Guidelines

### Component Design Principles

- Follow React best practices
- Fully typed with TypeScript
- Accessible (WCAG 2.1 AA)
- Composable and reusable
- Well-documented with Storybook
- Test with React Testing Library

### Adding a New Component

1. Create component with TypeScript
2. Add prop types and JSDoc
3. Implement accessibility features
4. Write unit tests
5. Add Storybook story
6. Update this README

## Testing

- Unit tests with React Testing Library
- Accessibility tests with axe
- Visual regression tests with Storybook
- Integration tests

## Examples

```typescript
import { ModelSelector, ParameterControl } from '@economic-models/ui-components'

function App() {
  return (
    <>
      <ModelSelector
        onSelect={(model) => setSelectedModel(model)}
      />
      <ParameterControl
        parameter={params.savingsRate}
        onChange={(value) => updateParam('savingsRate', value)}
      />
    </>
  )
}
```

## API Stability

⚠️ **Alpha** - Component APIs evolving based on UX research.
