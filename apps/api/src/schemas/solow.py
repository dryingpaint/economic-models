"""Pydantic schemas for Solow model API requests/responses."""

from pydantic import BaseModel, Field
from typing import Dict, List


class SolowParametersRequest(BaseModel):
    """Request schema for Solow model parameters."""

    savings_rate: float = Field(gt=0, lt=1, description="Savings rate (s)")
    depreciation_rate: float = Field(gt=0, lt=1, description="Depreciation rate (δ)")
    population_growth: float = Field(ge=0, lt=0.1, description="Population growth (n)")
    tech_growth: float = Field(ge=0, lt=0.1, description="Technology growth (g)")
    alpha: float = Field(gt=0, lt=1, description="Capital share (α)")
    initial_capital: float = Field(gt=0, description="Initial capital k(0)")

    model_config = {"json_schema_extra": {
        "example": {
            "savings_rate": 0.2,
            "depreciation_rate": 0.05,
            "population_growth": 0.01,
            "tech_growth": 0.02,
            "alpha": 0.33,
            "initial_capital": 1.0,
        }
    }}


class SteadyStateResponse(BaseModel):
    """Response schema for steady state calculation."""

    capital: float
    output: float
    consumption: float
    investment: float
    growth_rate: float


class SimulationRequest(BaseModel):
    """Request schema for time-path simulation."""

    parameters: SolowParametersRequest
    horizon: int = Field(gt=0, le=500, description="Simulation horizon (periods)")
    time_step: float = Field(gt=0, le=1, default=0.1, description="Time step")
    initial_capital: float | None = Field(None, description="Override initial capital")

    model_config = {"json_schema_extra": {
        "example": {
            "parameters": {
                "savings_rate": 0.2,
                "depreciation_rate": 0.05,
                "population_growth": 0.01,
                "tech_growth": 0.02,
                "alpha": 0.33,
                "initial_capital": 1.0,
            },
            "horizon": 100,
            "time_step": 0.5,
        }
    }}


class SimulationResponse(BaseModel):
    """Response schema for simulation results."""

    time: List[float]
    capital: List[float]
    output: List[float]
    consumption: List[float]
    investment: List[float]
    metadata: Dict


class ImpulseResponseRequest(BaseModel):
    """Request schema for impulse response calculation."""

    parameters: SolowParametersRequest
    shock_var: str = Field(description="Parameter to shock")
    shock_size: float = Field(description="Size of shock (additive)")
    horizon: int = Field(gt=0, le=500, description="Simulation horizon")
    time_step: float = Field(gt=0, le=1, default=0.1)

    model_config = {"json_schema_extra": {
        "example": {
            "parameters": {
                "savings_rate": 0.2,
                "depreciation_rate": 0.05,
                "population_growth": 0.01,
                "tech_growth": 0.02,
                "alpha": 0.33,
                "initial_capital": 1.0,
            },
            "shock_var": "savings_rate",
            "shock_size": 0.1,
            "horizon": 100,
        }
    }}
