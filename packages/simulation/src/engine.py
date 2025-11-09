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
        k0 = initial_capital if initial_capital is not None else self.model.params.initial_capital

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
        new_value = current_value + shock_size

        # Create new shocked parameters (Pydantic v2 style)
        shocked_params_dict = shocked_params.model_dump()
        shocked_params_dict[shock_var] = new_value

        # Import the model class to create new instance
        from packages.models.src.macroeconomic.solow import (
            SolowGrowthModel,
            SolowParameters,
        )

        # Validate shocked parameter will be accepted by Pydantic model
        try:
            new_params = SolowParameters(**shocked_params_dict)
        except ValueError as e:
            raise ValueError(
                f"Shock of {shock_size} to {shock_var} results in invalid value "
                f"{new_value}. Parameter constraints violated: {str(e)}"
            )
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

    def simulate_islm(
        self,
        horizon: int,
        shock_times: Optional[List[int]] = None,
        shock_types: Optional[List[str]] = None,
        shock_sizes: Optional[List[float]] = None,
    ) -> SimulationResult:
        """Simulate IS-LM model with optional policy shocks.

        Args:
            horizon: Number of periods to simulate
            shock_times: Time periods when shocks occur
            shock_types: Types of shocks ('G', 'T', 'M')
            shock_sizes: Size of each shock

        Returns:
            SimulationResult with time paths of income, interest rate, etc.
        """
        # Initialize arrays
        time = np.arange(0, horizon + 1)
        n = len(time)

        # Arrays to store results
        income = np.zeros(n)
        interest_rate = np.zeros(n)
        consumption = np.zeros(n)
        investment = np.zeros(n)

        # Initialize at equilibrium
        eq = self.model.calculate_equilibrium()
        income[0] = eq["income"]
        interest_rate[0] = eq["interest_rate"]
        consumption[0] = eq["consumption"]
        investment[0] = eq["investment"]

        # Store current parameters
        current_G = self.model.params.government_spending
        current_T = self.model.params.taxes
        current_M = self.model.params.money_supply

        # Process shocks
        if shock_times is None:
            shock_times = []
        if shock_types is None:
            shock_types = []
        if shock_sizes is None:
            shock_sizes = []

        # Import IS-LM model classes
        from packages.models.src.macroeconomic.islm import ISLMModel, ISLMParameters

        # Simulate period by period
        current_model = self.model
        for t in range(1, n):
            # Check for shocks at this time
            for shock_idx, shock_time in enumerate(shock_times):
                if t == shock_time:
                    shock_type = shock_types[shock_idx]
                    shock_size = shock_sizes[shock_idx]

                    if shock_type == "G":
                        current_G += shock_size
                    elif shock_type == "T":
                        current_T += shock_size
                    elif shock_type == "M":
                        current_M += shock_size

                    # Create new model with updated parameters
                    new_params = ISLMParameters(
                        autonomous_consumption=self.model.params.autonomous_consumption,
                        mpc=self.model.params.mpc,
                        autonomous_investment=self.model.params.autonomous_investment,
                        investment_sensitivity=self.model.params.investment_sensitivity,
                        autonomous_money_demand=self.model.params.autonomous_money_demand,
                        income_money_demand=self.model.params.income_money_demand,
                        interest_money_demand=self.model.params.interest_money_demand,
                        government_spending=current_G,
                        taxes=current_T,
                        money_supply=current_M,
                        price_level=self.model.params.price_level,
                    )
                    current_model = ISLMModel(new_params)

            # Calculate equilibrium for this period
            eq = current_model.calculate_equilibrium()
            income[t] = eq["income"]
            interest_rate[t] = eq["interest_rate"]
            consumption[t] = eq["consumption"]
            investment[t] = eq["investment"]

        return SimulationResult(
            time=time,
            states={
                "income": income,
                "interest_rate": interest_rate,
                "consumption": consumption,
                "investment": investment,
            },
            metadata={
                "horizon": horizon,
                "initial_equilibrium": {
                    "income": income[0],
                    "interest_rate": interest_rate[0],
                },
                "shock_times": shock_times,
                "shock_types": shock_types,
                "shock_sizes": shock_sizes,
                "model_params": self.model.params.model_dump(),
            },
        )

    def islm_impulse_response(
        self, shock_type: str, shock_size: float, horizon: int
    ) -> SimulationResult:
        """Calculate impulse response to a policy shock in IS-LM model.

        Args:
            shock_type: Type of shock ('G', 'T', 'M')
            shock_size: Size of shock
            horizon: Number of periods to simulate

        Returns:
            SimulationResult showing response to shock
        """
        # Simulate with shock at t=1
        return self.simulate_islm(
            horizon=horizon,
            shock_times=[1],
            shock_types=[shock_type],
            shock_sizes=[shock_size],
        )
