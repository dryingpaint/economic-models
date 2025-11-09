# @economic-models/visualization

Visualization components and utilities for economic data and models.

## Purpose

This package provides visualization capabilities:
- Time series charts
- Phase diagrams
- Impulse response functions
- 3D parameter space visualization
- Network diagrams for multi-agent systems
- Geographic/spatial visualizations
- Interactive controls
- Export to publication-ready formats

## Key Exports

```typescript
// Chart components (framework-agnostic)
export class TimeSeriesChart { ... }
export class PhaseDiagram { ... }
export class ImpulseResponseChart { ... }

// Utilities
export function exportChart(chart, format: 'png' | 'svg' | 'pdf'): Blob
export function createInteractiveControls(parameters): ControlPanel
```

## Dependencies

- `@economic-models/core` - Base types
- `d3` - Data visualization
- `plotly.js` - Interactive charts

## Dependents

- `@economic-models/ui-components` - React wrappers
- `apps/web` - Main web application

## Getting Started

```bash
cd packages/visualization
npm install
npm run dev
npm run test
```

## Directory Structure

```
src/
├── charts/             # Chart implementations
│   ├── time-series.ts
│   ├── phase-diagram.ts
│   ├── impulse-response.ts
│   └── parameter-space.ts
├── network/            # Network visualizations
├── spatial/            # Geographic visualizations
├── controls/           # Interactive controls
├── export/             # Export utilities
└── themes/             # Visualization themes
```

## Development Guidelines

### Chart Design Principles

- Framework-agnostic core (vanilla JS/D3)
- Responsive by default
- Accessibility compliant (WCAG 2.1 AA)
- Publication-ready output
- Performant for large datasets

### Adding a New Chart Type

1. Create chart class with standard interface
2. Implement responsive behavior
3. Add accessibility features (labels, alt text)
4. Support multiple export formats
5. Add usage examples
6. Write visual regression tests

## Testing

- Visual regression tests
- Accessibility tests (color contrast, screen readers)
- Performance tests for large datasets
- Export format validation

## Examples

```typescript
import { TimeSeriesChart } from '@economic-models/visualization'

const chart = new TimeSeriesChart({
  container: '#chart',
  data: simulationResult,
  variables: ['output', 'capital', 'consumption'],
  theme: 'publication'
})

chart.render()
chart.export('svg') // For publication
```

## API Stability

⚠️ **Alpha** - Chart APIs may evolve based on user feedback.
