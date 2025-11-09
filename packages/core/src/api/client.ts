/**
 * API client for economic models backend
 */

import type {
  SolowParameters,
  SteadyState,
  SimulationRequest,
  SimulationResult,
  ImpulseResponseRequest,
} from '../types/solow'
import type { ApiError } from '../types/simulation'

/**
 * Base API URL - can be overridden via environment variable
 */
const API_BASE_URL =
  typeof process !== 'undefined' && process.env.NEXT_PUBLIC_API_URL
    ? process.env.NEXT_PUBLIC_API_URL
    : 'http://localhost:8000'

/**
 * API client for Solow model endpoints
 */
export class SolowApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  /**
   * Calculate steady state values
   */
  async calculateSteadyState(params: SolowParameters): Promise<SteadyState> {
    const response = await fetch(`${this.baseUrl}/api/solow/steady-state`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    })

    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.detail || 'Failed to calculate steady state')
    }

    return response.json()
  }

  /**
   * Run simulation
   */
  async simulate(request: SimulationRequest): Promise<SimulationResult> {
    const response = await fetch(`${this.baseUrl}/api/solow/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.detail || 'Simulation failed')
    }

    return response.json()
  }

  /**
   * Calculate impulse response
   */
  async impulseResponse(
    request: ImpulseResponseRequest
  ): Promise<SimulationResult> {
    const response = await fetch(`${this.baseUrl}/api/solow/impulse-response`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.detail || 'Impulse response calculation failed')
    }

    return response.json()
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; model: string }> {
    const response = await fetch(`${this.baseUrl}/api/solow/health`)

    if (!response.ok) {
      throw new Error('Health check failed')
    }

    return response.json()
  }
}

/**
 * Default API client instance
 */
export const solowApi = new SolowApiClient()
