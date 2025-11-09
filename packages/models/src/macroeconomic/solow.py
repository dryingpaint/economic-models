"""
Solow-Swan Growth Model

Classic macroeconomic model of long-run economic growth.
Analyzes capital accumulation, technological progress, and population growth.

References:
- Solow, R. M. (1956). "A Contribution to the Theory of Economic Growth"
- Swan, T. W. (1956). "Economic Growth and Capital Accumulation"
"""

import numpy as np
from pydantic import BaseModel, Field
from typing import Dict


class SolowParameters(BaseModel):
    """Parameters for the Solow growth model.

    Attributes:
        savings_rate: Fraction of output saved/invested (s), 0 < s < 1
        depreciation_rate: Capital depreciation rate (δ), 0 < δ < 1
        population_growth: Population growth rate (n), typically 0.01-0.03
        tech_growth: Technology growth rate (g), typically 0.01-0.02
        alpha: Capital share of output (α), typically 0.3-0.4
        initial_capital: Starting capital per effective worker
    """

    savings_rate: float = Field(gt=0, lt=1, description="Savings rate (s)")
    depreciation_rate: float = Field(gt=0, lt=1, description="Depreciation rate (δ)")
    population_growth: float = Field(ge=0, lt=0.1, description="Population growth (n)")
    tech_growth: float = Field(ge=0, lt=0.1, description="Technology growth (g)")
    alpha: float = Field(gt=0, lt=1, description="Capital share (α)")
    initial_capital: float = Field(gt=0, description="Initial capital k(0)")

    model_config = {"frozen": True}  # Immutable parameters


class SolowGrowthModel:
    """
    Solow-Swan growth model implementation.

    Production function: Y = K^α (AL)^(1-α)
    Capital accumulation: k̇ = s·f(k) - (n + g + δ)·k

    Where:
    - k = K/(AL) is capital per effective worker
    - f(k) = k^α is production per effective worker
    - s is savings rate
    - n is population growth
    - g is technology growth
    - δ is depreciation rate
    """

    def __init__(self, params: SolowParameters):
        """Initialize model with parameters.

        Args:
            params: Model parameters (immutable)
        """
        self.params = params

    def production(self, capital: float) -> float:
        """Calculate output per effective worker.

        Args:
            capital: Capital per effective worker (k)

        Returns:
            Output per effective worker: y = k^α
        """
        return capital ** self.params.alpha

    def investment(self, capital: float) -> float:
        """Calculate investment per effective worker.

        Args:
            capital: Capital per effective worker (k)

        Returns:
            Investment: i = s·k^α
        """
        return self.params.savings_rate * self.production(capital)

    def effective_depreciation(self) -> float:
        """Calculate effective depreciation rate.

        Returns:
            Effective depreciation: (n + g + δ)
        """
        return (
            self.params.population_growth
            + self.params.tech_growth
            + self.params.depreciation_rate
        )

    def capital_change(self, capital: float) -> float:
        """Calculate change in capital per effective worker.

        Args:
            capital: Current capital per effective worker (k)

        Returns:
            Change in capital: dk/dt = s·k^α - (n + g + δ)·k
        """
        return self.investment(capital) - self.effective_depreciation() * capital

    def calculate_steady_state(self) -> Dict[str, float]:
        """Calculate steady-state values analytically.

        At steady state: s·k*^α = (n + g + δ)·k*
        Solving: k* = [s / (n + g + δ)]^(1/(1-α))

        Returns:
            Dictionary with steady-state values:
            - capital: k* (capital per effective worker)
            - output: y* (output per effective worker)
            - consumption: c* (consumption per effective worker)
            - investment: i* (investment per effective worker)
            - growth_rate: Steady-state growth rate of output per worker
        """
        s = self.params.savings_rate
        n = self.params.population_growth
        g = self.params.tech_growth
        delta = self.params.depreciation_rate
        alpha = self.params.alpha

        # Steady-state capital per effective worker
        k_star = (s / (n + g + delta)) ** (1 / (1 - alpha))

        # Steady-state output per effective worker
        y_star = k_star ** alpha

        # Steady-state investment per effective worker
        i_star = s * y_star

        # Steady-state consumption per effective worker
        c_star = (1 - s) * y_star

        return {
            "capital": k_star,
            "output": y_star,
            "consumption": c_star,
            "investment": i_star,
            "growth_rate": g,  # Growth rate of output per worker in steady state
        }

    def calculate_golden_rule(self) -> Dict[str, float]:
        """Calculate Golden Rule steady state (maximizes consumption).

        Golden Rule: MPK = n + g + δ
        This implies: α·k_gold^(α-1) = n + g + δ
        Solving: k_gold = [α / (n + g + δ)]^(1/(1-α))

        Returns:
            Dictionary with Golden Rule values:
            - capital: Golden Rule capital
            - output: Golden Rule output
            - consumption: Maximum steady-state consumption
            - savings_rate: Required savings rate for Golden Rule
        """
        n = self.params.population_growth
        g = self.params.tech_growth
        delta = self.params.depreciation_rate
        alpha = self.params.alpha

        # Golden Rule capital
        k_gold = (alpha / (n + g + delta)) ** (1 / (1 - alpha))

        # Golden Rule output
        y_gold = k_gold ** alpha

        # Required savings rate for Golden Rule
        s_gold = alpha

        # Golden Rule consumption (maximized)
        c_gold = (1 - s_gold) * y_gold

        return {
            "capital": k_gold,
            "output": y_gold,
            "consumption": c_gold,
            "savings_rate": s_gold,
        }

    def is_dynamically_efficient(self) -> bool:
        """Check if current savings rate is dynamically efficient.

        An economy is dynamically efficient if s < α (savings rate below Golden Rule).
        If s > α, the economy is over-saving.

        Returns:
            True if dynamically efficient, False if over-saving
        """
        return self.params.savings_rate <= self.params.alpha
