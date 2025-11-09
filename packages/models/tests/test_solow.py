"""Tests for Solow growth model.

Tests compare numerical results against analytical solutions from economic theory.
"""

import pytest
import numpy as np
from packages.models.src.macroeconomic.solow import SolowGrowthModel, SolowParameters


class TestSolowParameters:
    """Test parameter validation."""

    def test_valid_parameters(self):
        """Valid parameters should be accepted."""
        params = SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        assert params.savings_rate == 0.2
        assert params.alpha == 0.33

    def test_savings_rate_bounds(self):
        """Savings rate must be in (0, 1)."""
        with pytest.raises(ValueError):
            SolowParameters(
                savings_rate=0.0,  # Must be > 0
                depreciation_rate=0.05,
                population_growth=0.01,
                tech_growth=0.02,
                alpha=0.33,
                initial_capital=1.0,
            )

        with pytest.raises(ValueError):
            SolowParameters(
                savings_rate=1.0,  # Must be < 1
                depreciation_rate=0.05,
                population_growth=0.01,
                tech_growth=0.02,
                alpha=0.33,
                initial_capital=1.0,
            )

    def test_immutability(self):
        """Parameters should be immutable."""
        params = SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        with pytest.raises(ValueError):
            params.savings_rate = 0.3  # Should raise error


class TestSolowModel:
    """Test Solow model calculations."""

    @pytest.fixture
    def standard_params(self):
        """Standard calibration for testing."""
        return SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )

    @pytest.fixture
    def model(self, standard_params):
        """Create model instance."""
        return SolowGrowthModel(standard_params)

    def test_production_function(self, model):
        """Test Cobb-Douglas production: y = k^α."""
        k = 4.0
        expected = 4.0 ** 0.33
        assert np.isclose(model.production(k), expected)

    def test_investment(self, model):
        """Test investment: i = s·k^α."""
        k = 4.0
        expected = 0.2 * (4.0 ** 0.33)
        assert np.isclose(model.investment(k), expected)

    def test_effective_depreciation(self, model):
        """Test effective depreciation: n + g + δ."""
        expected = 0.01 + 0.02 + 0.05  # = 0.08
        assert np.isclose(model.effective_depreciation(), expected)

    def test_steady_state_analytical(self, model):
        """Test steady state against analytical solution.

        Analytical: k* = [s / (n + g + δ)]^(1/(1-α))
        """
        ss = model.calculate_steady_state()

        # Calculate expected steady state manually
        s, n, g, delta, alpha = 0.2, 0.01, 0.02, 0.05, 0.33
        k_star_expected = (s / (n + g + delta)) ** (1 / (1 - alpha))
        y_star_expected = k_star_expected ** alpha
        c_star_expected = (1 - s) * y_star_expected
        i_star_expected = s * y_star_expected

        assert np.isclose(ss["capital"], k_star_expected, rtol=1e-6)
        assert np.isclose(ss["output"], y_star_expected, rtol=1e-6)
        assert np.isclose(ss["consumption"], c_star_expected, rtol=1e-6)
        assert np.isclose(ss["investment"], i_star_expected, rtol=1e-6)
        assert np.isclose(ss["growth_rate"], 0.02)  # = g

    def test_steady_state_zero_change(self, model):
        """At steady state, capital change should be zero."""
        ss = model.calculate_steady_state()
        k_star = ss["capital"]

        # At steady state: dk/dt = 0
        dk = model.capital_change(k_star)
        assert np.isclose(dk, 0.0, atol=1e-10)

    def test_golden_rule(self):
        """Test Golden Rule calculation.

        Golden Rule: s = α maximizes steady-state consumption.
        """
        params = SolowParameters(
            savings_rate=0.33,  # = α
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        model = SolowGrowthModel(params)

        ss = model.calculate_steady_state()
        golden = model.calculate_golden_rule()

        # When s = α, steady state should equal Golden Rule
        assert np.isclose(ss["capital"], golden["capital"], rtol=1e-6)
        assert np.isclose(ss["consumption"], golden["consumption"], rtol=1e-6)

    def test_golden_rule_maximizes_consumption(self):
        """Golden Rule should give higher consumption than arbitrary s."""
        # Model with s < α
        params_low = SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        model_low = SolowGrowthModel(params_low)

        # Golden Rule consumption
        golden = model_low.calculate_golden_rule()
        ss_low = model_low.calculate_steady_state()

        # Golden Rule should have higher consumption
        assert golden["consumption"] > ss_low["consumption"]

    def test_dynamic_efficiency(self):
        """Test dynamic efficiency check."""
        # Efficient: s < α
        params_efficient = SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        model_efficient = SolowGrowthModel(params_efficient)
        assert model_efficient.is_dynamically_efficient()

        # Inefficient: s > α
        params_inefficient = SolowParameters(
            savings_rate=0.5,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        model_inefficient = SolowGrowthModel(params_inefficient)
        assert not model_inefficient.is_dynamically_efficient()

    def test_capital_accumulation_below_steady_state(self, model):
        """Below steady state, capital should increase (dk/dt > 0)."""
        ss = model.calculate_steady_state()
        k_below = ss["capital"] * 0.5

        dk = model.capital_change(k_below)
        assert dk > 0, "Capital should accumulate below steady state"

    def test_capital_accumulation_above_steady_state(self, model):
        """Above steady state, capital should decrease (dk/dt < 0)."""
        ss = model.calculate_steady_state()
        k_above = ss["capital"] * 1.5

        dk = model.capital_change(k_above)
        assert dk < 0, "Capital should depreciate above steady state"

    def test_comparative_statics_savings_rate(self):
        """Higher savings rate should increase steady-state capital."""
        params_low = SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        params_high = SolowParameters(
            savings_rate=0.3,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )

        model_low = SolowGrowthModel(params_low)
        model_high = SolowGrowthModel(params_high)

        ss_low = model_low.calculate_steady_state()
        ss_high = model_high.calculate_steady_state()

        assert ss_high["capital"] > ss_low["capital"]
        assert ss_high["output"] > ss_low["output"]
