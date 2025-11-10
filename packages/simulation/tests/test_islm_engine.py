"""Tests for IS-LM simulation engine."""

import pytest
import numpy as np

from packages.models.src.macroeconomic.islm import ISLMModel, ISLMParameters
from packages.simulation.src.engine import SimulationEngine, SimulationResult


class TestISLMSimulation:
    """Test IS-LM model simulation."""

    @pytest.fixture
    def model(self):
        """Create standard IS-LM model."""
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
        return ISLMModel(params)

    @pytest.fixture
    def engine(self, model):
        """Create simulation engine."""
        return SimulationEngine(model)

    def test_simulate_no_shocks(self, engine):
        """Simulation without shocks should stay at equilibrium."""
        result = engine.simulate_islm(horizon=10)

        # Check result structure
        assert len(result.time) == 11  # 0 to 10 inclusive
        assert "income" in result.states
        assert "interest_rate" in result.states
        assert "consumption" in result.states
        assert "investment" in result.states

        # Without shocks, all values should remain constant
        income_path = result.states["income"]
        initial_income = income_path[0]

        # Should stay approximately constant (numerical tolerance)
        for y in income_path:
            assert np.isclose(y, initial_income, rtol=1e-6)

    def test_fiscal_expansion_shock(self, engine):
        """Government spending increase should raise output."""
        # Shock at time 5
        result = engine.simulate_islm(
            horizon=20, shock_times=[5], shock_types=["G"], shock_sizes=[100]
        )

        income_before = result.states["income"][4]
        income_after = result.states["income"][6]
        interest_before = result.states["interest_rate"][4]
        interest_after = result.states["interest_rate"][6]

        # Income should increase
        assert income_after > income_before

        # Interest rate should increase
        assert interest_after > interest_before

        # Investment should decrease (crowding out)
        investment_before = result.states["investment"][4]
        investment_after = result.states["investment"][6]
        assert investment_after < investment_before

    def test_tax_increase_shock(self, engine):
        """Tax increase should reduce output."""
        result = engine.simulate_islm(
            horizon=20, shock_times=[5], shock_types=["T"], shock_sizes=[100]
        )

        income_before = result.states["income"][4]
        income_after = result.states["income"][6]
        interest_before = result.states["interest_rate"][4]
        interest_after = result.states["interest_rate"][6]

        # Income should decrease
        assert income_after < income_before

        # Interest rate should decrease
        assert interest_after < interest_before

    def test_monetary_expansion_shock(self, engine):
        """Money supply increase should raise output and lower interest rate."""
        result = engine.simulate_islm(
            horizon=20, shock_times=[5], shock_types=["M"], shock_sizes=[200]
        )

        income_before = result.states["income"][4]
        income_after = result.states["income"][6]
        interest_before = result.states["interest_rate"][4]
        interest_after = result.states["interest_rate"][6]

        # Income should increase
        assert income_after > income_before

        # Interest rate should decrease
        assert interest_after < interest_before

        # Investment should increase
        investment_before = result.states["investment"][4]
        investment_after = result.states["investment"][6]
        assert investment_after > investment_before

    def test_multiple_shocks(self, engine):
        """Test multiple shocks at different times."""
        result = engine.simulate_islm(
            horizon=30,
            shock_times=[5, 15, 25],
            shock_types=["G", "M", "T"],
            shock_sizes=[100, 200, 50],
        )

        # Check all time periods were simulated
        assert len(result.time) == 31

        # Income should respond to each shock
        income_path = result.states["income"]

        # After first shock (G increase): income increases
        assert income_path[6] > income_path[4]

        # After second shock (M increase): income should be higher
        assert income_path[16] > income_path[14]

        # After third shock (T increase): income should decrease
        assert income_path[26] < income_path[24]

    def test_impulse_response_government_spending(self, engine):
        """Test impulse response to government spending shock."""
        result = engine.islm_impulse_response(shock_type="G", shock_size=100, horizon=20)

        # Check metadata
        assert result.metadata["shock_times"] == [1]
        assert result.metadata["shock_types"] == ["G"]
        assert result.metadata["shock_sizes"] == [100]

        # Output should jump at shock time
        income_before = result.states["income"][0]
        income_after = result.states["income"][2]
        assert income_after > income_before

    def test_impulse_response_monetary_policy(self, engine):
        """Test impulse response to monetary expansion."""
        result = engine.islm_impulse_response(shock_type="M", shock_size=200, horizon=20)

        # Interest rate should fall
        r_before = result.states["interest_rate"][0]
        r_after = result.states["interest_rate"][2]
        assert r_after < r_before

        # Income should rise
        y_before = result.states["income"][0]
        y_after = result.states["income"][2]
        assert y_after > y_before

    def test_simulation_result_metadata(self, engine):
        """Check simulation result has correct metadata."""
        result = engine.simulate_islm(
            horizon=10, shock_times=[5], shock_types=["G"], shock_sizes=[100]
        )

        # Check metadata fields
        assert result.metadata["horizon"] == 10
        assert "initial_equilibrium" in result.metadata
        assert "income" in result.metadata["initial_equilibrium"]
        assert "interest_rate" in result.metadata["initial_equilibrium"]
        assert result.metadata["shock_times"] == [5]
        assert result.metadata["shock_types"] == ["G"]
        assert result.metadata["shock_sizes"] == [100]

    def test_national_income_identity(self, engine):
        """Y = C + I + G should hold at all times."""
        result = engine.simulate_islm(
            horizon=20, shock_times=[5, 15], shock_types=["G", "M"], shock_sizes=[100, 200]
        )

        # Get government spending from metadata
        G = engine.model.params.government_spending

        for t in range(len(result.time)):
            Y = result.states["income"][t]
            C = result.states["consumption"][t]
            I = result.states["investment"][t]

            # Adjust G if shock occurred
            current_G = G
            if t >= 5:
                current_G += 100  # First shock

            # Check identity
            assert np.isclose(Y, C + I + current_G, rtol=1e-5)

    def test_permanent_vs_temporary_effects(self, engine):
        """In IS-LM, policy changes have permanent effects (static model)."""
        result = engine.simulate_islm(
            horizon=30, shock_times=[10], shock_types=["G"], shock_sizes=[100]
        )

        income_path = result.states["income"]

        # Before shock: constant
        assert np.isclose(income_path[5], income_path[9], rtol=1e-6)

        # After shock: new higher level
        new_level = income_path[15]
        assert new_level > income_path[9]

        # Stays at new level
        assert np.isclose(income_path[15], income_path[25], rtol=1e-6)

    def test_crowding_out_effect(self, engine):
        """Fiscal expansion should crowd out investment."""
        # Run simulation with fiscal expansion
        result = engine.simulate_islm(
            horizon=20, shock_times=[10], shock_types=["G"], shock_sizes=[100]
        )

        # Investment should fall
        investment_before = result.states["investment"][9]
        investment_after = result.states["investment"][11]

        assert investment_after < investment_before, "Investment should be crowded out"

        # But total income still rises (partial crowding out)
        income_before = result.states["income"][9]
        income_after = result.states["income"][11]
        assert income_after > income_before

    def test_to_dict_conversion(self, engine):
        """Test result can be converted to dictionary."""
        result = engine.simulate_islm(horizon=5)

        data = result.to_dict()

        # Check structure
        assert "time" in data
        assert "states" in data
        assert "metadata" in data

        # Check state variables
        assert "income" in data["states"]
        assert "interest_rate" in data["states"]
        assert "consumption" in data["states"]
        assert "investment" in data["states"]

        # All should be lists (serialized from numpy)
        assert isinstance(data["time"], list)
        assert isinstance(data["states"]["income"], list)
