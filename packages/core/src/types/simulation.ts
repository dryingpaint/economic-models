/**
 * General simulation types
 */

/**
 * Time series data point
 */
export interface DataPoint {
  time: number
  value: number
}

/**
 * Time series
 */
export interface TimeSeries {
  label: string
  data: DataPoint[]
  color?: string
}

/**
 * Simulation state
 */
export type SimulationState = 'idle' | 'loading' | 'success' | 'error'

/**
 * API error response
 */
export interface ApiError {
  detail: string
  status?: number
}
