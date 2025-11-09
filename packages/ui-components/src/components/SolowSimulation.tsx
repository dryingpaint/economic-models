/**
 * Solow model simulation component with parameter controls
 */

'use client'

import React, { useState } from 'react'
import type {
  SolowParameters,
  SimulationResult,
} from '@economic-models/core'
import { solowApi } from '@economic-models/core'
import { TimeSeriesChart } from './TimeSeriesChart'

export interface SolowSimulationProps {
  initialParams?: SolowParameters
  onSimulationComplete?: (result: SimulationResult) => void
}

export function SolowSimulation({
  initialParams,
  onSimulationComplete,
}: SolowSimulationProps) {
  // Use default params from core if not provided
  const defaultParams: SolowParameters = {
    savings_rate: 0.2,
    depreciation_rate: 0.05,
    population_growth: 0.01,
    tech_growth: 0.02,
    alpha: 0.33,
    initial_capital: 1.0,
  }

  const [params, setParams] = useState<SolowParameters>(
    initialParams || defaultParams
  )
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleParamChange = (key: keyof SolowParameters, value: number) => {
    setParams((prev: SolowParameters) => ({ ...prev, [key]: value }))
  }

  const runSimulation = async () => {
    setLoading(true)
    setError(null)

    try {
      const simResult = await solowApi.simulate({
        parameters: params,
        horizon: 100,
        time_step: 0.5,
      })

      setResult(simResult)
      onSimulationComplete?.(simResult)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Simulation failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="solow-simulation">
      <div className="parameters-panel">
        <h3>Model Parameters</h3>

        <div className="param-group">
          <label>
            Savings Rate (s): {params.savings_rate.toFixed(2)}
            <input
              type="range"
              min="0.01"
              max="0.99"
              step="0.01"
              value={params.savings_rate}
              onChange={(e) =>
                handleParamChange('savings_rate', parseFloat(e.target.value))
              }
            />
          </label>
        </div>

        <div className="param-group">
          <label>
            Depreciation Rate (δ): {params.depreciation_rate.toFixed(3)}
            <input
              type="range"
              min="0.001"
              max="0.2"
              step="0.001"
              value={params.depreciation_rate}
              onChange={(e) =>
                handleParamChange('depreciation_rate', parseFloat(e.target.value))
              }
            />
          </label>
        </div>

        <div className="param-group">
          <label>
            Population Growth (n): {params.population_growth.toFixed(3)}
            <input
              type="range"
              min="0"
              max="0.05"
              step="0.001"
              value={params.population_growth}
              onChange={(e) =>
                handleParamChange('population_growth', parseFloat(e.target.value))
              }
            />
          </label>
        </div>

        <div className="param-group">
          <label>
            Technology Growth (g): {params.tech_growth.toFixed(3)}
            <input
              type="range"
              min="0"
              max="0.05"
              step="0.001"
              value={params.tech_growth}
              onChange={(e) =>
                handleParamChange('tech_growth', parseFloat(e.target.value))
              }
            />
          </label>
        </div>

        <div className="param-group">
          <label>
            Capital Share (α): {params.alpha.toFixed(2)}
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.01"
              value={params.alpha}
              onChange={(e) =>
                handleParamChange('alpha', parseFloat(e.target.value))
              }
            />
          </label>
        </div>

        <div className="param-group">
          <label>
            Initial Capital: {params.initial_capital.toFixed(2)}
            <input
              type="range"
              min="0.1"
              max="10"
              step="0.1"
              value={params.initial_capital}
              onChange={(e) =>
                handleParamChange('initial_capital', parseFloat(e.target.value))
              }
            />
          </label>
        </div>

        <button onClick={runSimulation} disabled={loading}>
          {loading ? 'Running...' : 'Run Simulation'}
        </button>

        {error && <div className="error">{error}</div>}
      </div>

      {result && (
        <div className="results-panel">
          <TimeSeriesChart data={result} title="Solow Model Dynamics" />
        </div>
      )}
    </div>
  )
}
