"""Pydantic schemas for IS-LM model API requests/responses."""

from pydantic import BaseModel, Field
from typing import Dict, List


class ISLMParametersRequest(BaseModel):
    """Request schema for IS-LM model parameters."""

    # Consumption parameters
    autonomous_consumption: float = Field(gt=0, description="Autonomous consumption (c0)")
    mpc: float = Field(gt=0, lt=1, description="Marginal propensity to consume (c1)")

    # Investment parameters
    autonomous_investment: float = Field(gt=0, description="Autonomous investment (i0)")
    investment_sensitivity: float = Field(
        gt=0, description="Investment interest rate sensitivity (i1)"
    )

    # Money demand parameters
    autonomous_money_demand: float = Field(gt=0, description="Autonomous money demand (L0)")
    income_money_demand: float = Field(
        gt=0, description="Income sensitivity of money demand (L1)"
    )
    interest_money_demand: float = Field(
        gt=0, description="Interest rate sensitivity of money demand (L2)"
    )

    # Fiscal policy variables
    government_spending: float = Field(ge=0, description="Government spending (G)")
    taxes: float = Field(ge=0, description="Lump-sum taxes (T)")

    # Monetary policy variables
    money_supply: float = Field(gt=0, description="Money supply (M)")
    price_level: float = Field(gt=0, description="Price level (P)", default=1.0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "autonomous_consumption": 100,
                "mpc": 0.8,
                "autonomous_investment": 200,
                "investment_sensitivity": 50,
                "autonomous_money_demand": 50,
                "income_money_demand": 0.2,
                "interest_money_demand": 100,
                "government_spending": 250,
                "taxes": 200,
                "money_supply": 1000,
                "price_level": 1.0,
            }
        }
    }


class EquilibriumResponse(BaseModel):
    """Response schema for IS-LM equilibrium calculation."""

    income: float
    interest_rate: float
    consumption: float
    investment: float
    aggregate_demand: float
    real_money_supply: float
    multiplier: float


class PolicyEffectRequest(BaseModel):
    """Request schema for policy change effect calculation."""

    parameters: ISLMParametersRequest
    delta_g: float = Field(default=0.0, description="Change in government spending")
    delta_t: float = Field(default=0.0, description="Change in taxes")
    delta_m: float = Field(default=0.0, description="Change in money supply")

    model_config = {
        "json_schema_extra": {
            "example": {
                "parameters": {
                    "autonomous_consumption": 100,
                    "mpc": 0.8,
                    "autonomous_investment": 200,
                    "investment_sensitivity": 50,
                    "autonomous_money_demand": 50,
                    "income_money_demand": 0.2,
                    "interest_money_demand": 100,
                    "government_spending": 250,
                    "taxes": 200,
                    "money_supply": 1000,
                    "price_level": 1.0,
                },
                "delta_g": 100,
                "delta_t": 0,
                "delta_m": 0,
            }
        }
    }


class PolicyEffectResponse(BaseModel):
    """Response schema for policy change effects."""

    delta_income: float
    delta_interest_rate: float
    delta_consumption: float
    delta_investment: float


class SimulationRequest(BaseModel):
    """Request schema for IS-LM simulation with shocks."""

    parameters: ISLMParametersRequest
    horizon: int = Field(gt=0, le=100, description="Simulation horizon (periods)")
    shock_times: List[int] = Field(default_factory=list, description="Times when shocks occur")
    shock_types: List[str] = Field(
        default_factory=list, description="Shock types: 'G', 'T', or 'M'"
    )
    shock_sizes: List[float] = Field(default_factory=list, description="Size of each shock")

    model_config = {
        "json_schema_extra": {
            "example": {
                "parameters": {
                    "autonomous_consumption": 100,
                    "mpc": 0.8,
                    "autonomous_investment": 200,
                    "investment_sensitivity": 50,
                    "autonomous_money_demand": 50,
                    "income_money_demand": 0.2,
                    "interest_money_demand": 100,
                    "government_spending": 250,
                    "taxes": 200,
                    "money_supply": 1000,
                    "price_level": 1.0,
                },
                "horizon": 30,
                "shock_times": [10, 20],
                "shock_types": ["G", "M"],
                "shock_sizes": [100, 200],
            }
        }
    }


class SimulationResponse(BaseModel):
    """Response schema for IS-LM simulation results."""

    time: List[float]
    income: List[float]
    interest_rate: List[float]
    consumption: List[float]
    investment: List[float]
    metadata: Dict


class ImpulseResponseRequest(BaseModel):
    """Request schema for IS-LM impulse response."""

    parameters: ISLMParametersRequest
    shock_type: str = Field(description="Shock type: 'G', 'T', or 'M'")
    shock_size: float = Field(description="Size of shock")
    horizon: int = Field(gt=0, le=100, description="Simulation horizon")

    model_config = {
        "json_schema_extra": {
            "example": {
                "parameters": {
                    "autonomous_consumption": 100,
                    "mpc": 0.8,
                    "autonomous_investment": 200,
                    "investment_sensitivity": 50,
                    "autonomous_money_demand": 50,
                    "income_money_demand": 0.2,
                    "interest_money_demand": 100,
                    "government_spending": 250,
                    "taxes": 200,
                    "money_supply": 1000,
                    "price_level": 1.0,
                },
                "shock_type": "G",
                "shock_size": 100,
                "horizon": 30,
            }
        }
    }
