"""Tests for simulation engine."""

import pytest
import numpy as np

from packages.models.src.macroeconomic.solow import SolowGrowthModel, SolowParameters
from packages.simulation.src.engine import SimulationEngine, SimulationResult


class TestSimulationResult:
    """Test simulation result data structure."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = SimulationResult(
            time=np.array([0, 1, 2]),
            states={"capital": np.array([1.0, 1.5, 2.0])},
            metadata={"horizon": 2},
        )

        data = result.to_dict()
        assert data["time"] == [0, 1, 2]
        assert data["states"]["capital"] == [1.0, 1.5, 2.0]
        assert data["metadata"]["horizon"] == 2


class TestSimulationEngine:
    """Test simulation engine."""

    @pytest.fixture
    def model(self):
        """Create standard Solow model."""
        params = SolowParameters(
            savings_rate=0.2,
            depreciation_rate=0.05,
            population_growth=0.01,
            tech_growth=0.02,
            alpha=0.33,
            initial_capital=1.0,
        )
        return SolowGrowthModel(params)

    @pytest.fixture
    def engine(self, model):
        """Create simulation engine."""
        return SimulationEngine(model)

    def test_simulate_converges_to_steady_state(self, engine):
        """Simulation should converge to analytical steady state."""
        # Start below steady state
        result = engine.simulate_solow(horizon=100, time_step=1.0, initial_capital=1.0)

        # Get steady state
        ss = engine.model.calculate_steady_state()

        # Final capital should be close to steady state
        final_capital = result.states["capital"][-1]
        assert np.isclose(final_capital, ss["capital"], rtol=0.01)

        # Final output should be close to steady state
        final_output = result.states["output"][-1]
        assert np.isclose(final_output, ss["output"], rtol=0.01)

    def test_simulate_from_above_steady_state(self, engine):
        """Simulation starting above SS should converge down."""
        ss = engine.model.calculate_steady_state()

        # Start above steady state
        result = engine.simulate_solow(
            horizon=100, time_step=1.0, initial_capital=ss["capital"] * 2
        )

        # Capital should decrease
        assert result.states["capital"][0] > result.states["capital"][-1]

        # Should converge to steady state
        final_capital = result.states["capital"][-1]
        assert np.isclose(final_capital, ss["capital"], rtol=0.01)

    def test_simulate_result_structure(self, engine):
        """Check simulation result has correct structure."""
        result = engine.simulate_solow(horizon=10, time_step=0.5)

        # Check time array
        assert len(result.time) > 0
        assert result.time[0] == 0
        assert result.time[-1] >= 10

        # Check state variables
        assert "capital" in result.states
        assert "output" in result.states
        assert "consumption" in result.states
        assert "investment" in result.states

        # All arrays same length
        n = len(result.time)
        assert len(result.states["capital"]) == n
        assert len(result.states["output"]) == n
        assert len(result.states["consumption"]) == n

        # Check metadata
        assert result.metadata["horizon"] == 10
        assert "steady_state" in result.metadata

    def test_consumption_investment_sum(self, engine):
        """Consumption + investment should equal output."""
        result = engine.simulate_solow(horizon=10)

        for i in range(len(result.time)):
            c = result.states["consumption"][i]
            inv = result.states["investment"][i]
            y = result.states["output"][i]
            assert np.isclose(c + inv, y, rtol=1e-6)

    def test_impulse_response_higher_savings(self, engine):
        """Positive savings shock should increase steady-state capital."""
        ss_initial = engine.model.calculate_steady_state()

        # Shock savings rate up by 0.1
        result = engine.impulse_response(
            shock_var="savings_rate", shock_size=0.1, horizon=100, time_step=1.0
        )

        # Should converge to higher capital
        final_capital = result.states["capital"][-1]
        assert final_capital > ss_initial["capital"]

        # Check metadata
        assert result.metadata["shock_var"] == "savings_rate"
        assert result.metadata["shock_size"] == 0.1

    def test_simulation_at_steady_state(self, engine):
        """Starting at steady state should stay there."""
        ss = engine.model.calculate_steady_state()

        result = engine.simulate_solow(
            horizon=50, time_step=1.0, initial_capital=ss["capital"]
        )

        # Capital should stay constant (within numerical tolerance)
        capital_path = result.states["capital"]
        assert np.allclose(capital_path, ss["capital"], rtol=0.001)
