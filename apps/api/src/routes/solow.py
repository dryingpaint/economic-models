"""API routes for Solow growth model."""

from fastapi import APIRouter, HTTPException
from packages.models.src.macroeconomic.solow import SolowGrowthModel, SolowParameters
from packages.simulation.src.engine import SimulationEngine
from apps.api.src.schemas.solow import (
    SolowParametersRequest,
    SteadyStateResponse,
    SimulationRequest,
    SimulationResponse,
    ImpulseResponseRequest,
)

router = APIRouter(prefix="/api/solow", tags=["solow"])


@router.post("/steady-state", response_model=SteadyStateResponse)
async def calculate_steady_state(params: SolowParametersRequest):
    """Calculate steady-state values for Solow model.

    Args:
        params: Model parameters

    Returns:
        Steady-state capital, output, consumption, investment, growth rate
    """
    try:
        # Convert request schema to model parameters
        model_params = SolowParameters(**params.model_dump())
        model = SolowGrowthModel(model_params)

        # Calculate steady state
        ss = model.calculate_steady_state()

        return SteadyStateResponse(**ss)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/simulate", response_model=SimulationResponse)
async def simulate_model(request: SimulationRequest):
    """Run time-path simulation of Solow model.

    Args:
        request: Simulation parameters including model params and horizon

    Returns:
        Time series of capital, output, consumption, investment
    """
    try:
        # Create model
        model_params = SolowParameters(**request.parameters.model_dump())
        model = SolowGrowthModel(model_params)

        # Create simulation engine
        engine = SimulationEngine(model)

        # Run simulation
        result = engine.simulate_solow(
            horizon=request.horizon,
            time_step=request.time_step,
            initial_capital=request.initial_capital,
        )

        # Convert to response format
        return SimulationResponse(
            time=result.time.tolist(),
            capital=result.states["capital"].tolist(),
            output=result.states["output"].tolist(),
            consumption=result.states["consumption"].tolist(),
            investment=result.states["investment"].tolist(),
            metadata=result.metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/impulse-response", response_model=SimulationResponse)
async def calculate_impulse_response(request: ImpulseResponseRequest):
    """Calculate impulse response to parameter shock.

    Args:
        request: Parameters including which parameter to shock and shock size

    Returns:
        Time series showing response to shock
    """
    try:
        # Create model
        model_params = SolowParameters(**request.parameters.model_dump())
        model = SolowGrowthModel(model_params)

        # Create simulation engine
        engine = SimulationEngine(model)

        # Calculate impulse response
        result = engine.impulse_response(
            shock_var=request.shock_var,
            shock_size=request.shock_size,
            horizon=request.horizon,
            time_step=request.time_step,
        )

        # Convert to response format
        return SimulationResponse(
            time=result.time.tolist(),
            capital=result.states["capital"].tolist(),
            output=result.states["output"].tolist(),
            consumption=result.states["consumption"].tolist(),
            investment=result.states["investment"].tolist(),
            metadata=result.metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model": "solow"}
