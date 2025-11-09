"""
Simulation engine for running economic model simulations.

Provides time-path simulation capabilities for dynamic economic models.
"""

import numpy as np
from scipy.integrate import odeint
from typing import Callable, Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class SimulationResult:
    """Results from a model simulation.

    Attributes:
        time: Array of time points
        states: Dictionary mapping state variable names to their time paths
        metadata: Additional simulation metadata
    """

    time: np.ndarray
    states: Dict[str, np.ndarray]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization."""
        return {
            "time": self.time.tolist(),
            "states": {k: v.tolist() for k, v in self.states.items()},
            "metadata": self.metadata,
        }


class SimulationEngine:
    """Engine for simulating dynamic economic models.

    Supports ODE-based models with continuous time evolution.
    """

    def __init__(self, model: Any):
        """Initialize simulation engine with a model.

        Args:
            model: Economic model instance with capital_change method
        """
        self.model = model

    def simulate_solow(
        self,
        horizon: int,
        time_step: float = 0.1,
        initial_capital: Optional[float] = None,
    ) -> SimulationResult:
        """Simulate Solow model transition dynamics.

        Args:
            horizon: Number of time periods to simulate
            time_step: Time step for simulation (default: 0.1)
            initial_capital: Starting capital (uses model param if None)

        Returns:
            SimulationResult with time paths of capital, output, consumption
        """
        # Set initial capital
        k0 = initial_capital or self.model.params.initial_capital

        # Create time grid
        t = np.arange(0, horizon + time_step, time_step)

        # Define ODE function
        def dk_dt(k: float, t: float) -> float:
            """Capital accumulation differential equation."""
            return self.model.capital_change(k)

        # Solve ODE
        k_path = odeint(dk_dt, k0, t).flatten()

        # Calculate other variables
        y_path = np.array([self.model.production(k) for k in k_path])
        c_path = np.array(
            [(1 - self.model.params.savings_rate) * y for y in y_path]
        )
        i_path = np.array([self.model.investment(k) for k in k_path])

        # Calculate steady state for reference
        ss = self.model.calculate_steady_state()

        return SimulationResult(
            time=t,
            states={
                "capital": k_path,
                "output": y_path,
                "consumption": c_path,
                "investment": i_path,
            },
            metadata={
                "horizon": horizon,
                "time_step": time_step,
                "initial_capital": k0,
                "steady_state": ss,
                "model_params": self.model.params.model_dump(),
            },
        )

    def impulse_response(
        self,
        shock_var: str,
        shock_size: float,
        horizon: int,
        time_step: float = 0.1,
    ) -> SimulationResult:
        """Calculate impulse response to a parameter shock.

        Args:
            shock_var: Parameter to shock (e.g., 'savings_rate')
            shock_size: Size of shock (additive)
            horizon: Number of periods to simulate
            time_step: Time step for simulation

        Returns:
            SimulationResult showing response to shock
        """
        # Start from steady state
        ss = self.model.calculate_steady_state()
        k0 = ss["capital"]

        # Create shocked parameters
        shocked_params = self.model.params.model_copy(deep=True)
        current_value = getattr(shocked_params, shock_var)

        # Create new shocked parameters (Pydantic v2 style)
        shocked_params_dict = shocked_params.model_dump()
        shocked_params_dict[shock_var] = current_value + shock_size

        # Import the model class to create new instance
        from packages.models.src.macroeconomic.solow import (
            SolowGrowthModel,
            SolowParameters,
        )

        new_params = SolowParameters(**shocked_params_dict)
        shocked_model = SolowGrowthModel(new_params)

        # Create temporary engine with shocked model
        shocked_engine = SimulationEngine(shocked_model)

        # Simulate from old steady state with new parameters
        result = shocked_engine.simulate_solow(
            horizon=horizon, time_step=time_step, initial_capital=k0
        )

        # Add shock metadata
        result.metadata.update(
            {
                "shock_var": shock_var,
                "shock_size": shock_size,
                "initial_steady_state": ss,
            }
        )

        return result
