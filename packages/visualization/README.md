# @economic-models/visualization

Framework-agnostic visualization library for economic data.

## Purpose

Visualization capabilities for economic models:
- Time series charts
- Impulse response functions
- Phase diagrams
- 3D parameter spaces
- Network diagrams (agent-based models)
- Export to publication formats (PNG, SVG, PDF)

## Tech Stack

**Hybrid approach for best-in-class results:**

- **Plotly.js** - Standard economic charts (90% of use cases)
  - Time series, IRFs, surface plots
  - Interactive out of the box
  - Publication quality

- **D3.js** - Custom visualizations (10% of use cases)
  - Network diagrams for ABMs
  - Custom economic diagrams
  - Maximum flexibility

## Key Exports

```typescript
// Plotly-based charts
export class TimeSeriesChart { ... }
export class ImpulseResponseChart { ... }
export class ParameterSpaceChart { ... }

// D3-based charts
export class NetworkDiagram { ... }
export class PhaseDiagram { ... }

// Utilities
export function exportChart(chart, format: 'png' | 'svg' | 'pdf'): Blob
```

## Dependencies

- `plotly.js` - Interactive charts
- `d3` - Custom visualizations
- `@economic-models/core` - Types

## Structure

```
src/
├── plotly/             # Plotly.js charts
│   ├── time-series.ts
│   ├── impulse-response.ts
│   └── surface-plot.ts
├── d3/                 # D3 charts
│   ├── network.ts
│   └── phase-diagram.ts
├── export/             # Export utilities
└── themes/             # Chart themes
```

## Development

```bash
cd packages/visualization
npm install
npm run dev
npm run test
```

## Code Standards

- **Max 300-400 lines per file**
- Framework-agnostic (vanilla TypeScript)
- Accessible (WCAG 2.1 AA)
- Responsive by default
- Type-safe APIs

## Examples

### Time Series (Plotly)

```typescript
import { TimeSeriesChart } from '@economic-models/visualization'

const chart = new TimeSeriesChart({
  container: document.getElementById('chart'),
  data: {
    time: [0, 1, 2, 3, 4],
    series: {
      gdp: [100, 102, 104, 106, 108],
      consumption: [60, 61, 62, 63, 64]
    }
  },
  options: {
    title: 'GDP Growth',
    xLabel: 'Time',
    yLabel: 'Level'
  }
})

chart.render()
chart.export('svg')  // Publication ready
```

### Network Diagram (D3)

```typescript
import { NetworkDiagram } from '@economic-models/visualization'

const network = new NetworkDiagram({
  container: document.getElementById('network'),
  nodes: [...],
  links: [...],
  options: {
    nodeSize: d => d.degree,
    nodeColor: d => d.type
  }
})

network.render()
```

## Design Principles

1. **Simple API** - Easy to use, hard to misuse
2. **Performance** - Handle large datasets efficiently
3. **Accessibility** - Screen readers, keyboard navigation
4. **Publication ready** - High-quality exports
5. **Interactive** - Zoom, pan, hover by default

## Testing

```bash
npm run test           # Unit tests
npm run test:visual    # Visual regression
npm run test:a11y      # Accessibility
```

## Why Plotly + D3?

- **Plotly**: Best for standard charts, minimal code, great defaults
- **D3**: Best for custom visualizations, maximum control
- Use the right tool for each job
- Both are industry standards with strong TypeScript support
