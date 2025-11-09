"""
IS-LM Model

Classic macroeconomic model of short-run equilibrium in the goods and money markets.
Analyzes the interaction between real and monetary sectors of the economy.

The IS curve represents goods market equilibrium (Investment-Savings).
The LM curve represents money market equilibrium (Liquidity-Money).

References:
- Hicks, J. R. (1937). "Mr. Keynes and the 'Classics': A Suggested Interpretation"
- Blanchard, O. (2017). "Macroeconomics" (7th edition), Chapter 5
"""

import numpy as np
from pydantic import BaseModel, Field
from typing import Dict, Optional
from scipy.optimize import fsolve


class ISLMParameters(BaseModel):
    """Parameters for the IS-LM model.

    Consumption function: C = c0 + c1(Y - T)
    Investment function: I = i0 - i1·r
    Money demand: M^d/P = L0 + L1·Y - L2·r
    Money supply: M^s (exogenous)

    Attributes:
        autonomous_consumption: Autonomous consumption (c0), c0 > 0
        mpc: Marginal propensity to consume (c1), 0 < c1 < 1
        autonomous_investment: Autonomous investment (i0), i0 > 0
        investment_sensitivity: Investment sensitivity to interest rate (i1), i1 > 0
        autonomous_money_demand: Autonomous money demand (L0), L0 > 0
        income_money_demand: Income sensitivity of money demand (L1), L1 > 0
        interest_money_demand: Interest rate sensitivity of money demand (L2), L2 > 0
        government_spending: Government spending (G), G >= 0
        taxes: Lump-sum taxes (T), T >= 0
        money_supply: Nominal money supply (M), M > 0
        price_level: Price level (P), P > 0
    """

    # Consumption parameters
    autonomous_consumption: float = Field(
        gt=0, description="Autonomous consumption (c0)"
    )
    mpc: float = Field(gt=0, lt=1, description="Marginal propensity to consume (c1)")

    # Investment parameters
    autonomous_investment: float = Field(
        gt=0, description="Autonomous investment (i0)"
    )
    investment_sensitivity: float = Field(
        gt=0, description="Investment interest rate sensitivity (i1)"
    )

    # Money demand parameters
    autonomous_money_demand: float = Field(
        gt=0, description="Autonomous money demand (L0)"
    )
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

    model_config = {"frozen": True}


class ISLMModel:
    """
    IS-LM model implementation.

    IS curve (goods market equilibrium):
    Y = C + I + G
    Y = c0 + c1(Y - T) + i0 - i1·r + G

    LM curve (money market equilibrium):
    M/P = L0 + L1·Y - L2·r

    Equilibrium: Solve system of two equations for Y and r.
    """

    def __init__(self, params: ISLMParameters):
        """Initialize model with parameters.

        Args:
            params: Model parameters (immutable)
        """
        self.params = params

    def consumption(self, income: float) -> float:
        """Calculate consumption given income.

        C = c0 + c1(Y - T)

        Args:
            income: National income (Y)

        Returns:
            Consumption (C)
        """
        disposable_income = income - self.params.taxes
        return (
            self.params.autonomous_consumption
            + self.params.mpc * disposable_income
        )

    def investment(self, interest_rate: float) -> float:
        """Calculate investment given interest rate.

        I = i0 - i1·r

        Args:
            interest_rate: Real interest rate (r)

        Returns:
            Investment (I)
        """
        return (
            self.params.autonomous_investment
            - self.params.investment_sensitivity * interest_rate
        )

    def money_demand(self, income: float, interest_rate: float) -> float:
        """Calculate real money demand.

        M^d/P = L0 + L1·Y - L2·r

        Args:
            income: National income (Y)
            interest_rate: Interest rate (r)

        Returns:
            Real money demand (M^d/P)
        """
        return (
            self.params.autonomous_money_demand
            + self.params.income_money_demand * income
            - self.params.interest_money_demand * interest_rate
        )

    def real_money_supply(self) -> float:
        """Calculate real money supply.

        M^s/P

        Returns:
            Real money supply (M/P)
        """
        return self.params.money_supply / self.params.price_level

    def is_curve(self, interest_rate: float) -> float:
        """Calculate output on IS curve for given interest rate.

        From Y = c0 + c1(Y - T) + i0 - i1·r + G
        Solving for Y:
        Y = [c0 - c1·T + i0 - i1·r + G] / (1 - c1)

        Args:
            interest_rate: Interest rate (r)

        Returns:
            Output level (Y) satisfying IS curve
        """
        numerator = (
            self.params.autonomous_consumption
            - self.params.mpc * self.params.taxes
            + self.params.autonomous_investment
            - self.params.investment_sensitivity * interest_rate
            + self.params.government_spending
        )
        denominator = 1 - self.params.mpc
        return numerator / denominator

    def lm_curve(self, income: float) -> float:
        """Calculate interest rate on LM curve for given income.

        From M/P = L0 + L1·Y - L2·r
        Solving for r:
        r = [L0 + L1·Y - M/P] / L2

        Args:
            income: National income (Y)

        Returns:
            Interest rate (r) satisfying LM curve
        """
        numerator = (
            self.params.autonomous_money_demand
            + self.params.income_money_demand * income
            - self.real_money_supply()
        )
        return numerator / self.params.interest_money_demand

    def calculate_equilibrium(
        self, initial_guess: Optional[tuple[float, float]] = None
    ) -> Dict[str, float]:
        """Calculate IS-LM equilibrium numerically.

        Solves the system:
        - IS: Y = c0 + c1(Y - T) + i0 - i1·r + G
        - LM: M/P = L0 + L1·Y - L2·r

        Args:
            initial_guess: Optional (Y, r) starting point for solver

        Returns:
            Dictionary with equilibrium values:
            - income: Equilibrium output (Y*)
            - interest_rate: Equilibrium interest rate (r*)
            - consumption: Equilibrium consumption (C*)
            - investment: Equilibrium investment (I*)
            - aggregate_demand: Total aggregate demand (AD*)
            - real_money_supply: Real money supply (M/P)
            - multiplier: Fiscal multiplier (1/(1-c1))
        """
        if initial_guess is None:
            # Use simple heuristic for initial guess
            y0 = (
                self.params.autonomous_consumption
                + self.params.autonomous_investment
                + self.params.government_spending
            )
            r0 = 0.05  # 5% interest rate
            initial_guess = (y0, r0)

        def equations(vars):
            """System of equations to solve."""
            Y, r = vars

            # IS curve residual: Y - [c0 + c1(Y-T) + i0 - i1·r + G] = 0
            is_residual = Y - (
                self.params.autonomous_consumption
                + self.params.mpc * (Y - self.params.taxes)
                + self.params.autonomous_investment
                - self.params.investment_sensitivity * r
                + self.params.government_spending
            )

            # LM curve residual: M/P - [L0 + L1·Y - L2·r] = 0
            lm_residual = self.real_money_supply() - (
                self.params.autonomous_money_demand
                + self.params.income_money_demand * Y
                - self.params.interest_money_demand * r
            )

            return [is_residual, lm_residual]

        # Solve system
        solution = fsolve(equations, initial_guess)
        Y_star, r_star = solution

        # Calculate equilibrium quantities
        C_star = self.consumption(Y_star)
        I_star = self.investment(r_star)
        AD_star = C_star + I_star + self.params.government_spending

        # Fiscal multiplier
        multiplier = 1 / (1 - self.params.mpc)

        return {
            "income": float(Y_star),
            "interest_rate": float(r_star),
            "consumption": float(C_star),
            "investment": float(I_star),
            "aggregate_demand": float(AD_star),
            "real_money_supply": float(self.real_money_supply()),
            "multiplier": float(multiplier),
        }

    def fiscal_expansion_effect(
        self, delta_g: float, delta_t: float = 0.0
    ) -> Dict[str, float]:
        """Calculate effect of fiscal policy change.

        Args:
            delta_g: Change in government spending
            delta_t: Change in taxes

        Returns:
            Dictionary with changes in equilibrium:
            - delta_income: Change in equilibrium income
            - delta_interest_rate: Change in equilibrium interest rate
            - delta_consumption: Change in consumption
            - delta_investment: Change in investment (crowding out)
        """
        # Original equilibrium
        original = self.calculate_equilibrium()

        # New parameters with fiscal policy change
        new_params = self.params.model_copy(
            update={
                "government_spending": self.params.government_spending + delta_g,
                "taxes": self.params.taxes + delta_t,
            }
        )
        new_model = ISLMModel(new_params)
        new_equilibrium = new_model.calculate_equilibrium()

        return {
            "delta_income": new_equilibrium["income"] - original["income"],
            "delta_interest_rate": new_equilibrium["interest_rate"]
            - original["interest_rate"],
            "delta_consumption": new_equilibrium["consumption"]
            - original["consumption"],
            "delta_investment": new_equilibrium["investment"] - original["investment"],
        }

    def monetary_expansion_effect(self, delta_m: float) -> Dict[str, float]:
        """Calculate effect of monetary policy change.

        Args:
            delta_m: Change in money supply

        Returns:
            Dictionary with changes in equilibrium:
            - delta_income: Change in equilibrium income
            - delta_interest_rate: Change in equilibrium interest rate
            - delta_consumption: Change in consumption
            - delta_investment: Change in investment
        """
        # Original equilibrium
        original = self.calculate_equilibrium()

        # New parameters with monetary policy change
        new_params = self.params.model_copy(
            update={"money_supply": self.params.money_supply + delta_m}
        )
        new_model = ISLMModel(new_params)
        new_equilibrium = new_model.calculate_equilibrium()

        return {
            "delta_income": new_equilibrium["income"] - original["income"],
            "delta_interest_rate": new_equilibrium["interest_rate"]
            - original["interest_rate"],
            "delta_consumption": new_equilibrium["consumption"]
            - original["consumption"],
            "delta_investment": new_equilibrium["investment"] - original["investment"],
        }

    def is_liquidity_trap(self, threshold: float = 0.001) -> bool:
        """Check if economy is in liquidity trap.

        A liquidity trap occurs when interest rate is near zero and
        monetary policy becomes ineffective.

        Args:
            threshold: Interest rate threshold for liquidity trap

        Returns:
            True if in liquidity trap, False otherwise
        """
        equilibrium = self.calculate_equilibrium()
        return equilibrium["interest_rate"] < threshold
