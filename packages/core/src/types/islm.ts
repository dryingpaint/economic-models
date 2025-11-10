/**
 * TypeScript types for IS-LM model.
 * These types match the Python Pydantic schemas in apps/api/src/schemas/islm.py
 */

import { z } from 'zod'

/**
 * IS-LM model parameters schema
 */
export const ISLMParametersSchema = z.object({
  autonomous_consumption: z.number().gt(0),
  mpc: z.number().gt(0).lt(1),
  autonomous_investment: z.number().gt(0),
  investment_sensitivity: z.number().gt(0),
  autonomous_money_demand: z.number().gt(0),
  income_money_demand: z.number().gt(0),
  interest_money_demand: z.number().gt(0),
  government_spending: z.number().gte(0),
  taxes: z.number().gte(0),
  money_supply: z.number().gt(0),
  price_level: z.number().gt(0).default(1.0),
})

export type ISLMParameters = z.infer<typeof ISLMParametersSchema>

/**
 * IS-LM equilibrium results
 */
export interface Equilibrium {
  income: number
  interest_rate: number
  consumption: number
  investment: number
  aggregate_demand: number
  real_money_supply: number
  multiplier: number
}

/**
 * Policy effect results
 */
export interface PolicyEffect {
  delta_income: number
  delta_interest_rate: number
  delta_consumption: number
  delta_investment: number
}

/**
 * Policy effect request
 */
export interface PolicyEffectRequest {
  parameters: ISLMParameters
  delta_g?: number
  delta_t?: number
  delta_m?: number
}

/**
 * Simulation request
 */
export interface ISLMSimulationRequest {
  parameters: ISLMParameters
  horizon: number
  shock_times?: number[]
  shock_types?: string[]
  shock_sizes?: number[]
}

/**
 * Simulation results
 */
export interface ISLMSimulationResult {
  time: number[]
  income: number[]
  interest_rate: number[]
  consumption: number[]
  investment: number[]
  metadata: {
    horizon: number
    initial_equilibrium: {
      income: number
      interest_rate: number
    }
    shock_times: number[]
    shock_types: string[]
    shock_sizes: number[]
    model_params: ISLMParameters
  }
}

/**
 * Impulse response request
 */
export interface ISLMImpulseResponseRequest {
  parameters: ISLMParameters
  shock_type: 'G' | 'T' | 'M'
  shock_size: number
  horizon: number
}

/**
 * Default IS-LM parameters (standard calibration)
 */
export const DEFAULT_ISLM_PARAMS: ISLMParameters = {
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
