"""Tests for IS-LM model.

Tests compare numerical results against analytical solutions from macroeconomic theory.
"""

import pytest
import numpy as np
from packages.models.src.macroeconomic.islm import ISLMModel, ISLMParameters


class TestISLMParameters:
    """Test parameter validation."""

    def test_valid_parameters(self):
        """Valid parameters should be accepted."""
        params = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=1000,
            price_level=1.0,
        )
        assert params.mpc == 0.8
        assert params.government_spending == 250

    def test_mpc_bounds(self):
        """Marginal propensity to consume must be in (0, 1)."""
        with pytest.raises(ValueError):
            ISLMParameters(
                autonomous_consumption=100,
                mpc=0.0,  # Must be > 0
                autonomous_investment=200,
                investment_sensitivity=50,
                autonomous_money_demand=50,
                income_money_demand=0.2,
                interest_money_demand=100,
                government_spending=250,
                taxes=200,
                money_supply=1000,
            )

        with pytest.raises(ValueError):
            ISLMParameters(
                autonomous_consumption=100,
                mpc=1.0,  # Must be < 1
                autonomous_investment=200,
                investment_sensitivity=50,
                autonomous_money_demand=50,
                income_money_demand=0.2,
                interest_money_demand=100,
                government_spending=250,
                taxes=200,
                money_supply=1000,
            )

    def test_positive_parameters(self):
        """Most parameters must be positive."""
        with pytest.raises(ValueError):
            ISLMParameters(
                autonomous_consumption=-100,  # Must be > 0
                mpc=0.8,
                autonomous_investment=200,
                investment_sensitivity=50,
                autonomous_money_demand=50,
                income_money_demand=0.2,
                interest_money_demand=100,
                government_spending=250,
                taxes=200,
                money_supply=1000,
            )

    def test_immutability(self):
        """Parameters should be immutable."""
        params = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=1000,
        )
        with pytest.raises(ValueError):
            params.mpc = 0.9  # Should raise error


class TestISLMModel:
    """Test IS-LM model calculations."""

    @pytest.fixture
    def standard_params(self):
        """Standard calibration for testing."""
        return ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=1000,
            price_level=1.0,
        )

    @pytest.fixture
    def model(self, standard_params):
        """Create model instance."""
        return ISLMModel(standard_params)

    def test_consumption_function(self, model):
        """Test consumption: C = c0 + c1(Y - T)."""
        income = 1000
        expected = 100 + 0.8 * (1000 - 200)  # = 100 + 640 = 740
        assert np.isclose(model.consumption(income), expected)

    def test_investment_function(self, model):
        """Test investment: I = i0 - i1·r."""
        interest_rate = 0.05
        expected = 200 - 50 * 0.05  # = 200 - 2.5 = 197.5
        assert np.isclose(model.investment(interest_rate), expected)

    def test_money_demand(self, model):
        """Test money demand: M^d/P = L0 + L1·Y - L2·r."""
        income = 1000
        interest_rate = 0.05
        expected = 50 + 0.2 * 1000 - 100 * 0.05  # = 50 + 200 - 5 = 245
        assert np.isclose(model.money_demand(income, interest_rate), expected)

    def test_real_money_supply(self, model):
        """Test real money supply: M/P."""
        expected = 1000 / 1.0  # = 1000
        assert np.isclose(model.real_money_supply(), expected)

    def test_is_curve(self, model):
        """Test IS curve: Y = [c0 - c1·T + i0 - i1·r + G] / (1 - c1)."""
        r = 0.05
        # Numerator: 100 - 0.8*200 + 200 - 50*0.05 + 250
        # = 100 - 160 + 200 - 2.5 + 250 = 387.5
        # Denominator: 1 - 0.8 = 0.2
        # Y = 387.5 / 0.2 = 1937.5
        expected = 1937.5
        assert np.isclose(model.is_curve(r), expected, rtol=1e-6)

    def test_lm_curve(self, model):
        """Test LM curve: r = [L0 + L1·Y - M/P] / L2."""
        Y = 1000
        # Numerator: 50 + 0.2*1000 - 1000 = 50 + 200 - 1000 = -750
        # r = -750 / 100 = -7.5
        expected = -7.5
        assert np.isclose(model.lm_curve(Y), expected)

    def test_equilibrium_calculation(self, model):
        """Test equilibrium calculation matches IS-LM intersection."""
        eq = model.calculate_equilibrium()

        # Verify equilibrium satisfies IS curve
        Y_from_is = model.is_curve(eq["interest_rate"])
        assert np.isclose(eq["income"], Y_from_is, rtol=1e-4)

        # Verify equilibrium satisfies LM curve
        r_from_lm = model.lm_curve(eq["income"])
        assert np.isclose(eq["interest_rate"], r_from_lm, rtol=1e-4)

    def test_equilibrium_identities(self, model):
        """Test national income accounting identities hold at equilibrium."""
        eq = model.calculate_equilibrium()

        # Y = C + I + G
        Y_computed = eq["consumption"] + eq["investment"] + model.params.government_spending
        assert np.isclose(eq["income"], Y_computed, rtol=1e-6)

        # Aggregate demand should equal income
        assert np.isclose(eq["aggregate_demand"], eq["income"], rtol=1e-6)

    def test_fiscal_multiplier(self, model):
        """Test fiscal multiplier is 1/(1-c1)."""
        eq = model.calculate_equilibrium()
        expected_multiplier = 1 / (1 - 0.8)  # = 5
        assert np.isclose(eq["multiplier"], expected_multiplier)

    def test_fiscal_expansion_increases_output(self, model):
        """Government spending increase should increase output."""
        effect = model.fiscal_expansion_effect(delta_g=100)

        # Output should increase
        assert effect["delta_income"] > 0

        # Interest rate should increase (shift IS right)
        assert effect["delta_interest_rate"] > 0

        # Investment should decrease (crowding out)
        assert effect["delta_investment"] < 0

    def test_fiscal_expansion_crowding_out(self, model):
        """Fiscal expansion should crowd out some private investment."""
        effect = model.fiscal_expansion_effect(delta_g=100)

        # The increase in income should be less than multiplier * delta_g
        # due to crowding out
        simple_multiplier = model.calculate_equilibrium()["multiplier"]
        simple_effect = simple_multiplier * 100

        # With crowding out, actual effect is smaller
        assert effect["delta_income"] < simple_effect
        assert effect["delta_investment"] < 0  # Crowding out

    def test_tax_increase_reduces_output(self, model):
        """Tax increase should reduce output."""
        effect = model.fiscal_expansion_effect(delta_g=0, delta_t=100)

        # Output should decrease
        assert effect["delta_income"] < 0

        # Interest rate should decrease (shift IS left)
        assert effect["delta_interest_rate"] < 0

        # Investment should increase (less crowding out)
        assert effect["delta_investment"] > 0

    def test_balanced_budget_multiplier(self, model):
        """Equal increase in G and T should increase output (balanced budget multiplier = 1)."""
        # Increase both G and T by same amount
        effect = model.fiscal_expansion_effect(delta_g=100, delta_t=100)

        # Output should increase, but by less than just increasing G
        assert effect["delta_income"] > 0

        # The balanced budget multiplier is approximately 1
        # (exact value depends on interest rate effects)
        assert effect["delta_income"] < 100 * 5  # Less than full multiplier effect

    def test_monetary_expansion_increases_output(self, model):
        """Money supply increase should increase output and lower interest rate."""
        effect = model.monetary_expansion_effect(delta_m=100)

        # Output should increase
        assert effect["delta_income"] > 0

        # Interest rate should decrease (shift LM right)
        assert effect["delta_interest_rate"] < 0

        # Investment should increase (lower interest rate)
        assert effect["delta_investment"] > 0

        # Consumption should increase (higher income)
        assert effect["delta_consumption"] > 0

    def test_monetary_expansion_stimulates_investment(self, model):
        """Monetary expansion works through investment channel."""
        original = model.calculate_equilibrium()
        effect = model.monetary_expansion_effect(delta_m=200)

        # Investment should increase significantly
        assert effect["delta_investment"] > 0

        # The increase in investment should contribute to income increase
        # Investment increases because interest rate falls
        assert effect["delta_interest_rate"] < 0

    def test_liquidity_trap_detection(self):
        """Test liquidity trap detection when interest rate near zero."""
        # Create scenario with very low interest rate
        params_trap = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=500,  # High autonomous investment
            investment_sensitivity=10,  # Low sensitivity
            autonomous_money_demand=10,
            income_money_demand=0.1,
            interest_money_demand=1000,  # High interest sensitivity
            government_spending=100,
            taxes=100,
            money_supply=2000,  # High money supply
            price_level=1.0,
        )
        model_trap = ISLMModel(params_trap)

        # Check if interest rate is very low
        eq = model_trap.calculate_equilibrium()
        if eq["interest_rate"] < 0.001:
            assert model_trap.is_liquidity_trap()

    def test_comparative_statics_government_spending(self):
        """Higher government spending should increase equilibrium output."""
        params_low = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=200,  # Lower G
            taxes=200,
            money_supply=1000,
        )
        params_high = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=300,  # Higher G
            taxes=200,
            money_supply=1000,
        )

        model_low = ISLMModel(params_low)
        model_high = ISLMModel(params_high)

        eq_low = model_low.calculate_equilibrium()
        eq_high = model_high.calculate_equilibrium()

        assert eq_high["income"] > eq_low["income"]
        assert eq_high["interest_rate"] > eq_low["interest_rate"]

    def test_comparative_statics_money_supply(self):
        """Higher money supply should increase output and lower interest rate."""
        params_low = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=800,  # Lower M
        )
        params_high = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=1200,  # Higher M
        )

        model_low = ISLMModel(params_low)
        model_high = ISLMModel(params_high)

        eq_low = model_low.calculate_equilibrium()
        eq_high = model_high.calculate_equilibrium()

        assert eq_high["income"] > eq_low["income"]
        assert eq_high["interest_rate"] < eq_low["interest_rate"]

    def test_price_level_effects(self):
        """Higher price level should reduce real money supply and output."""
        params_low_p = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=1000,
            price_level=1.0,  # Lower P
        )
        params_high_p = ISLMParameters(
            autonomous_consumption=100,
            mpc=0.8,
            autonomous_investment=200,
            investment_sensitivity=50,
            autonomous_money_demand=50,
            income_money_demand=0.2,
            interest_money_demand=100,
            government_spending=250,
            taxes=200,
            money_supply=1000,
            price_level=2.0,  # Higher P
        )

        model_low_p = ISLMModel(params_low_p)
        model_high_p = ISLMModel(params_high_p)

        eq_low_p = model_low_p.calculate_equilibrium()
        eq_high_p = model_high_p.calculate_equilibrium()

        # Higher price level reduces real money supply
        assert model_high_p.real_money_supply() < model_low_p.real_money_supply()

        # Should reduce output and increase interest rate
        assert eq_high_p["income"] < eq_low_p["income"]
        assert eq_high_p["interest_rate"] > eq_low_p["interest_rate"]
