"""API routes for IS-LM model."""

from fastapi import APIRouter, HTTPException
from packages.models.src.macroeconomic.islm import ISLMModel, ISLMParameters
from packages.simulation.src.engine import SimulationEngine
from apps.api.src.schemas.islm import (
    ISLMParametersRequest,
    EquilibriumResponse,
    PolicyEffectRequest,
    PolicyEffectResponse,
    SimulationRequest,
    SimulationResponse,
    ImpulseResponseRequest,
)

router = APIRouter(prefix="/api/islm", tags=["islm"])


@router.post("/equilibrium", response_model=EquilibriumResponse)
async def calculate_equilibrium(params: ISLMParametersRequest):
    """Calculate IS-LM equilibrium.

    Args:
        params: Model parameters

    Returns:
        Equilibrium income, interest rate, consumption, investment, etc.
    """
    try:
        # Convert request schema to model parameters
        model_params = ISLMParameters(**params.model_dump())
        model = ISLMModel(model_params)

        # Calculate equilibrium
        eq = model.calculate_equilibrium()

        return EquilibriumResponse(**eq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fiscal-effect", response_model=PolicyEffectResponse)
async def calculate_fiscal_effect(request: PolicyEffectRequest):
    """Calculate effect of fiscal policy change.

    Args:
        request: Parameters and fiscal policy changes (delta_g, delta_t)

    Returns:
        Changes in income, interest rate, consumption, investment
    """
    try:
        # Create model
        model_params = ISLMParameters(**request.parameters.model_dump())
        model = ISLMModel(model_params)

        # Calculate fiscal expansion effect
        effect = model.fiscal_expansion_effect(
            delta_g=request.delta_g, delta_t=request.delta_t
        )

        return PolicyEffectResponse(**effect)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/monetary-effect", response_model=PolicyEffectResponse)
async def calculate_monetary_effect(request: PolicyEffectRequest):
    """Calculate effect of monetary policy change.

    Args:
        request: Parameters and monetary policy change (delta_m)

    Returns:
        Changes in income, interest rate, consumption, investment
    """
    try:
        # Create model
        model_params = ISLMParameters(**request.parameters.model_dump())
        model = ISLMModel(model_params)

        # Calculate monetary expansion effect
        effect = model.monetary_expansion_effect(delta_m=request.delta_m)

        return PolicyEffectResponse(**effect)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/simulate", response_model=SimulationResponse)
async def simulate_model(request: SimulationRequest):
    """Run simulation of IS-LM model with policy shocks.

    Args:
        request: Parameters, horizon, and shock specifications

    Returns:
        Time series of income, interest rate, consumption, investment
    """
    try:
        # Create model
        model_params = ISLMParameters(**request.parameters.model_dump())
        model = ISLMModel(model_params)

        # Create simulation engine
        engine = SimulationEngine(model)

        # Run simulation
        result = engine.simulate_islm(
            horizon=request.horizon,
            shock_times=request.shock_times,
            shock_types=request.shock_types,
            shock_sizes=request.shock_sizes,
        )

        # Convert to response format
        return SimulationResponse(
            time=result.time.tolist(),
            income=result.states["income"].tolist(),
            interest_rate=result.states["interest_rate"].tolist(),
            consumption=result.states["consumption"].tolist(),
            investment=result.states["investment"].tolist(),
            metadata=result.metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/impulse-response", response_model=SimulationResponse)
async def calculate_impulse_response(request: ImpulseResponseRequest):
    """Calculate impulse response to policy shock.

    Args:
        request: Parameters, shock type, shock size, and horizon

    Returns:
        Time series showing response to shock
    """
    try:
        # Create model
        model_params = ISLMParameters(**request.parameters.model_dump())
        model = ISLMModel(model_params)

        # Create simulation engine
        engine = SimulationEngine(model)

        # Calculate impulse response
        result = engine.islm_impulse_response(
            shock_type=request.shock_type,
            shock_size=request.shock_size,
            horizon=request.horizon,
        )

        # Convert to response format
        return SimulationResponse(
            time=result.time.tolist(),
            income=result.states["income"].tolist(),
            interest_rate=result.states["interest_rate"].tolist(),
            consumption=result.states["consumption"].tolist(),
            investment=result.states["investment"].tolist(),
            metadata=result.metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model": "islm"}
