/**
 * Plotly configuration and theme utilities
 */

import type { Config, Layout } from 'plotly.js'

/**
 * Default Plotly configuration
 */
export const DEFAULT_CONFIG: Partial<Config> = {
  responsive: true,
  displayModeBar: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d'],
}

/**
 * Default layout for economic charts
 */
export const DEFAULT_LAYOUT: Partial<Layout> = {
  font: {
    family: 'system-ui, -apple-system, sans-serif',
    size: 12,
  },
  paper_bgcolor: 'white',
  plot_bgcolor: '#f8f9fa',
  margin: {
    l: 60,
    r: 40,
    t: 40,
    b: 60,
  },
  hovermode: 'x unified',
  showlegend: true,
  legend: {
    orientation: 'h',
    yanchor: 'bottom',
    y: 1.02,
    xanchor: 'right',
    x: 1,
  },
}

/**
 * Color palette for economic variables
 */
export const ECONOMIC_COLORS = {
  capital: '#2563eb', // blue
  output: '#16a34a', // green
  consumption: '#dc2626', // red
  investment: '#ea580c', // orange
  steady_state: '#6b7280', // gray
}
