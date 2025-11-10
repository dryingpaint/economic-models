/**
 * IS-LM model simulation component with parameter controls and policy shocks
 */

'use client'

import React, { useState } from 'react'
import type {
  ISLMParameters,
  ISLMSimulationResult,
} from '@economic-models/core'

export interface ISLMSimulationProps {
  initialParams?: ISLMParameters
  onSimulationComplete?: (result: ISLMSimulationResult) => void
}

export function ISLMSimulation({
  initialParams,
  onSimulationComplete,
}: ISLMSimulationProps) {
  const defaultParams: ISLMParameters = {
    autonomous_consumption: 100,
    mpc: 0.8,
    autonomous_investment: 200,
    investment_sensitivity: 50,
    autonomous_money_demand: 50,
    income_money_demand: 0.2,
    interest_money_demand: 100,
    government_spending: 250,
    taxes: 200,
    money_supply: 1000,
    price_level: 1.0,
  }

  const [params, setParams] = useState<ISLMParameters>(
    initialParams || defaultParams
  )
  const [result, setResult] = useState<ISLMSimulationResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Shock configuration
  const [shockTime, setShockTime] = useState(10)
  const [shockType, setShockType] = useState<'G' | 'T' | 'M'>('G')
  const [shockSize, setShockSize] = useState(100)

  const handleParamChange = (key: keyof ISLMParameters, value: number) => {
    setParams((prev: ISLMParameters) => ({ ...prev, [key]: value }))
  }

  const runSimulation = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/islm/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          parameters: params,
          horizon: 30,
          shock_times: [shockTime],
          shock_types: [shockType],
          shock_sizes: [shockSize],
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const simResult = await response.json()
      setResult(simResult)
      onSimulationComplete?.(simResult)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Simulation failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h2>IS-LM Model Simulation</h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
        {/* Left Panel: Parameters */}
        <div>
          <h3>Consumption Function</h3>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Autonomous Consumption (c₀): {params.autonomous_consumption}
              <input
                type="range"
                min="50"
                max="200"
                step="10"
                value={params.autonomous_consumption}
                onChange={(e) =>
                  handleParamChange('autonomous_consumption', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              MPC (c₁): {params.mpc.toFixed(2)}
              <input
                type="range"
                min="0.5"
                max="0.95"
                step="0.05"
                value={params.mpc}
                onChange={(e) =>
                  handleParamChange('mpc', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <h3>Investment Function</h3>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Autonomous Investment (i₀): {params.autonomous_investment}
              <input
                type="range"
                min="100"
                max="400"
                step="50"
                value={params.autonomous_investment}
                onChange={(e) =>
                  handleParamChange('autonomous_investment', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Interest Sensitivity (i₁): {params.investment_sensitivity}
              <input
                type="range"
                min="10"
                max="100"
                step="10"
                value={params.investment_sensitivity}
                onChange={(e) =>
                  handleParamChange('investment_sensitivity', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <h3>Fiscal Policy</h3>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Government Spending (G): {params.government_spending}
              <input
                type="range"
                min="100"
                max="500"
                step="50"
                value={params.government_spending}
                onChange={(e) =>
                  handleParamChange('government_spending', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Taxes (T): {params.taxes}
              <input
                type="range"
                min="0"
                max="400"
                step="50"
                value={params.taxes}
                onChange={(e) =>
                  handleParamChange('taxes', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>
        </div>

        {/* Right Panel: Money Market & Shocks */}
        <div>
          <h3>Money Market</h3>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Money Supply (M): {params.money_supply}
              <input
                type="range"
                min="500"
                max="2000"
                step="100"
                value={params.money_supply}
                onChange={(e) =>
                  handleParamChange('money_supply', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Income Elasticity (L₁): {params.income_money_demand.toFixed(2)}
              <input
                type="range"
                min="0.05"
                max="0.5"
                step="0.05"
                value={params.income_money_demand}
                onChange={(e) =>
                  handleParamChange('income_money_demand', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Interest Elasticity (L₂): {params.interest_money_demand}
              <input
                type="range"
                min="50"
                max="200"
                step="10"
                value={params.interest_money_demand}
                onChange={(e) =>
                  handleParamChange('interest_money_demand', parseFloat(e.target.value))
                }
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <h3>Policy Shock Configuration</h3>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Shock Type:
              <select
                value={shockType}
                onChange={(e) => setShockType(e.target.value as 'G' | 'T' | 'M')}
                style={{ display: 'block', width: '100%', padding: '5px' }}
              >
                <option value="G">Government Spending (G)</option>
                <option value="T">Taxes (T)</option>
                <option value="M">Money Supply (M)</option>
              </select>
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Shock Time (period): {shockTime}
              <input
                type="range"
                min="1"
                max="25"
                step="1"
                value={shockTime}
                onChange={(e) => setShockTime(parseInt(e.target.value))}
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Shock Size: {shockSize}
              <input
                type="range"
                min="-200"
                max="200"
                step="50"
                value={shockSize}
                onChange={(e) => setShockSize(parseFloat(e.target.value))}
                style={{ display: 'block', width: '100%' }}
              />
            </label>
          </div>

          <button
            onClick={runSimulation}
            disabled={loading}
            style={{
              width: '100%',
              padding: '10px',
              fontSize: '16px',
              backgroundColor: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Running Simulation...' : 'Run Simulation with Shock'}
          </button>

          {error && (
            <div style={{ color: 'red', marginTop: '10px', padding: '10px', backgroundColor: '#fee' }}>
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Results Panel */}
      {result && (
        <div style={{ marginTop: '40px' }}>
          <h3>Simulation Results</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div>
              <h4>Income (Y)</h4>
              <SimplePlot
                data={result.time}
                values={result.income}
                color="#2563eb"
                shockTime={shockTime}
              />
            </div>
            <div>
              <h4>Interest Rate (r)</h4>
              <SimplePlot
                data={result.time}
                values={result.interest_rate}
                color="#dc2626"
                shockTime={shockTime}
              />
            </div>
            <div>
              <h4>Consumption (C)</h4>
              <SimplePlot
                data={result.time}
                values={result.consumption}
                color="#16a34a"
                shockTime={shockTime}
              />
            </div>
            <div>
              <h4>Investment (I)</h4>
              <SimplePlot
                data={result.time}
                values={result.investment}
                color="#9333ea"
                shockTime={shockTime}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// Simple SVG plot component
function SimplePlot({
  data,
  values,
  color,
  shockTime,
}: {
  data: number[]
  values: number[]
  color: string
  shockTime: number
}) {
  const width = 400
  const height = 200
  const padding = 40

  const minY = Math.min(...values)
  const maxY = Math.max(...values)
  const rangeY = maxY - minY || 1

  const points = data
    .map((x, i) => {
      const px = padding + ((x / Math.max(...data)) * (width - 2 * padding))
      const py = height - padding - (((values[i] - minY) / rangeY) * (height - 2 * padding))
      return `${px},${py}`
    })
    .join(' ')

  const shockX = padding + ((shockTime / Math.max(...data)) * (width - 2 * padding))

  return (
    <svg width={width} height={height} style={{ border: '1px solid #ddd', backgroundColor: '#fff' }}>
      {/* Shock line */}
      <line
        x1={shockX}
        y1={padding}
        x2={shockX}
        y2={height - padding}
        stroke="#ef4444"
        strokeWidth="2"
        strokeDasharray="4"
      />
      {/* Data line */}
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="2"
      />
      {/* Axes */}
      <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#000" />
      <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#000" />
      {/* Labels */}
      <text x={width / 2} y={height - 5} textAnchor="middle" fontSize="12">Time</text>
      <text x={5} y={padding} fontSize="12">{maxY.toFixed(1)}</text>
      <text x={5} y={height - padding} fontSize="12">{minY.toFixed(1)}</text>
    </svg>
  )
}
