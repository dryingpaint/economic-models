/**
 * TypeScript types for Solow growth model.
 * These types match the Python Pydantic schemas in apps/api/src/schemas/solow.py
 */

import { z } from 'zod'

/**
 * Solow model parameters schema
 */
export const SolowParametersSchema = z.object({
  savings_rate: z.number().gt(0).lt(1),
  depreciation_rate: z.number().gt(0).lt(1),
  population_growth: z.number().gte(0).lt(0.1),
  tech_growth: z.number().gte(0).lt(0.1),
  alpha: z.number().gt(0).lt(1),
  initial_capital: z.number().gt(0),
})

export type SolowParameters = z.infer<typeof SolowParametersSchema>

/**
 * Steady state calculation results
 */
export interface SteadyState {
  capital: number
  output: number
  consumption: number
  investment: number
  growth_rate: number
}

/**
 * Simulation request
 */
export interface SimulationRequest {
  parameters: SolowParameters
  horizon: number
  time_step?: number
  initial_capital?: number
}

/**
 * Simulation results
 */
export interface SimulationResult {
  time: number[]
  capital: number[]
  output: number[]
  consumption: number[]
  investment: number[]
  metadata: {
    horizon: number
    time_step: number
    initial_capital: number
    steady_state: SteadyState
    model_params: SolowParameters
  }
}

/**
 * Impulse response request
 */
export interface ImpulseResponseRequest {
  parameters: SolowParameters
  shock_var: string
  shock_size: number
  horizon: number
  time_step?: number
}

/**
 * Default Solow parameters (standard calibration)
 */
export const DEFAULT_SOLOW_PARAMS: SolowParameters = {
  savings_rate: 0.2,
  depreciation_rate: 0.05,
  population_growth: 0.01,
  tech_growth: 0.02,
  alpha: 0.33,
  initial_capital: 1.0,
}
