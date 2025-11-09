/**
 * Time series chart component using Plotly
 */

'use client'

import React, { useEffect, useRef } from 'react'
import type { SimulationResult } from '@economic-models/core'
import {
  createTimeSeriesTraces,
  createTimeSeriesLayout,
  getPlotlyConfig,
} from '@economic-models/visualization'

// Dynamic import of Plotly to avoid SSR issues
let Plotly: typeof import('plotly.js-basic-dist-min')

export interface TimeSeriesChartProps {
  data: SimulationResult
  title?: string
  showSteadyState?: boolean
  height?: number
}

export function TimeSeriesChart({
  data,
  title = 'Simulation Results',
  showSteadyState = true,
  height = 500,
}: TimeSeriesChartProps) {
  const plotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Dynamically import Plotly
    import('plotly.js-basic-dist-min').then((plotlyModule) => {
      Plotly = plotlyModule.default || plotlyModule

      if (!plotRef.current) return

      // Prepare data
      const timeSeriesData = {
        time: data.time,
        series: {
          capital: data.capital,
          output: data.output,
          consumption: data.consumption,
          investment: data.investment,
        },
        steadyState: showSteadyState ? data.metadata.steady_state : undefined,
      }

      // Create traces and layout
      const traces = createTimeSeriesTraces(timeSeriesData, {
        showSteadyState,
      })
      const layout = createTimeSeriesLayout({
        title,
        xLabel: 'Time (periods)',
        yLabel: 'Level',
        height,
      })

      // Render plot
      Plotly.newPlot(plotRef.current, traces, layout, getPlotlyConfig())
    })

    // Cleanup
    return () => {
      if (plotRef.current && Plotly) {
        Plotly.purge(plotRef.current)
      }
    }
  }, [data, title, showSteadyState, height])

  return <div ref={plotRef} />
}
