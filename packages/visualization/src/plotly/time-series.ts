/**
 * Time series chart using Plotly
 */

import type { Data, Layout } from 'plotly.js'
import { DEFAULT_CONFIG, DEFAULT_LAYOUT, ECONOMIC_COLORS } from './config'

export interface TimeSeriesData {
  time: number[]
  series: Record<string, number[]>
  steadyState?: Record<string, number>
}

export interface TimeSeriesOptions {
  title?: string
  xLabel?: string
  yLabel?: string
  showSteadyState?: boolean
  height?: number
}

/**
 * Create Plotly traces for time series data
 */
export function createTimeSeriesTraces(
  data: TimeSeriesData,
  options: TimeSeriesOptions = {}
): Data[] {
  const traces: Data[] = []

  // Create trace for each series
  Object.entries(data.series).forEach(([name, values]) => {
    traces.push({
      x: data.time,
      y: values,
      name: name.charAt(0).toUpperCase() + name.slice(1),
      type: 'scatter',
      mode: 'lines',
      line: {
        color: ECONOMIC_COLORS[name as keyof typeof ECONOMIC_COLORS] || '#000',
        width: 2,
      },
    })
  })

  // Add steady state lines if provided
  if (options.showSteadyState && data.steadyState) {
    Object.entries(data.steadyState).forEach(([name, value]) => {
      if (name in data.series) {
        traces.push({
          x: data.time,
          y: Array(data.time.length).fill(value),
          name: `${name.charAt(0).toUpperCase() + name.slice(1)} (SS)`,
          type: 'scatter',
          mode: 'lines',
          line: {
            color: ECONOMIC_COLORS[name as keyof typeof ECONOMIC_COLORS] || '#000',
            width: 1,
            dash: 'dash',
          },
          showlegend: true,
        })
      }
    })
  }

  return traces
}

/**
 * Create Plotly layout for time series
 */
export function createTimeSeriesLayout(
  options: TimeSeriesOptions = {}
): Partial<Layout> {
  return {
    ...DEFAULT_LAYOUT,
    title: options.title || 'Simulation Results',
    xaxis: {
      title: options.xLabel || 'Time',
      gridcolor: '#e5e7eb',
    },
    yaxis: {
      title: options.yLabel || 'Value',
      gridcolor: '#e5e7eb',
    },
    height: options.height || 400,
  }
}

/**
 * Get default Plotly config
 */
export function getPlotlyConfig() {
  return DEFAULT_CONFIG
}
