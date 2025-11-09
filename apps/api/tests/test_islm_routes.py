"""Tests for IS-LM model API routes."""

import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app

client = TestClient(app)


class TestISLMRoutes:
    """Test IS-LM API endpoints."""

    @pytest.fixture
    def standard_params(self):
        """Standard IS-LM parameters for testing."""
        return {
            "autonomous_consumption": 100,
            "mpc": 0.8,
            "autonomous_investment": 200,
            "investment_sensitivity": 50,
            "autonomous_money_demand": 50,
            "income_money_demand": 0.2,
            "interest_money_demand": 100,
            "government_spending": 250,
            "taxes": 200,
            "money_supply": 1000,
            "price_level": 1.0,
        }

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_islm_health_check(self):
        """Test IS-LM-specific health endpoint."""
        response = client.get("/api/islm/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model"] == "islm"

    def test_calculate_equilibrium(self, standard_params):
        """Test equilibrium calculation endpoint."""
        response = client.post("/api/islm/equilibrium", json=standard_params)

        assert response.status_code == 200
        data = response.json()

        # Check all required fields present
        assert "income" in data
        assert "interest_rate" in data
        assert "consumption" in data
        assert "investment" in data
        assert "aggregate_demand" in data
        assert "real_money_supply" in data
        assert "multiplier" in data

        # Check income, consumption, investment are positive
        assert data["income"] > 0
        assert data["consumption"] > 0
        assert data["investment"] > 0
        # Interest rate can be negative in some parameter configurations

        # Check multiplier is correct (1/(1-mpc))
        expected_multiplier = 1 / (1 - 0.8)
        assert abs(data["multiplier"] - expected_multiplier) < 0.01

    def test_fiscal_expansion_effect(self, standard_params):
        """Test fiscal expansion effect endpoint."""
        request_data = {
            "parameters": standard_params,
            "delta_g": 100,
            "delta_t": 0,
            "delta_m": 0,
        }

        response = client.post("/api/islm/fiscal-effect", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check all fields present
        assert "delta_income" in data
        assert "delta_interest_rate" in data
        assert "delta_consumption" in data
        assert "delta_investment" in data

        # Fiscal expansion should increase income
        assert data["delta_income"] > 0

        # Interest rate should increase
        assert data["delta_interest_rate"] > 0

        # Investment should decrease (crowding out)
        assert data["delta_investment"] < 0

    def test_tax_increase_effect(self, standard_params):
        """Test tax increase effect endpoint."""
        request_data = {
            "parameters": standard_params,
            "delta_g": 0,
            "delta_t": 100,
            "delta_m": 0,
        }

        response = client.post("/api/islm/fiscal-effect", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Tax increase should decrease income
        assert data["delta_income"] < 0

        # Interest rate should decrease
        assert data["delta_interest_rate"] < 0

    def test_monetary_expansion_effect(self, standard_params):
        """Test monetary expansion effect endpoint."""
        request_data = {"parameters": standard_params, "delta_m": 200, "delta_g": 0, "delta_t": 0}

        response = client.post("/api/islm/monetary-effect", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Monetary expansion should increase income
        assert data["delta_income"] > 0

        # Interest rate should decrease
        assert data["delta_interest_rate"] < 0

        # Investment should increase
        assert data["delta_investment"] > 0

    def test_simulate_no_shocks(self, standard_params):
        """Test simulation endpoint without shocks."""
        request_data = {
            "parameters": standard_params,
            "horizon": 20,
            "shock_times": [],
            "shock_types": [],
            "shock_sizes": [],
        }

        response = client.post("/api/islm/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "time" in data
        assert "income" in data
        assert "interest_rate" in data
        assert "consumption" in data
        assert "investment" in data
        assert "metadata" in data

        # Check arrays are correct length
        assert len(data["time"]) == 21  # 0 to 20 inclusive
        assert len(data["income"]) == 21
        assert len(data["interest_rate"]) == 21

        # Without shocks, values should be constant
        income_values = data["income"]
        assert all(abs(y - income_values[0]) < 0.001 for y in income_values)

    def test_simulate_with_fiscal_shock(self, standard_params):
        """Test simulation with fiscal policy shock."""
        request_data = {
            "parameters": standard_params,
            "horizon": 30,
            "shock_times": [10],
            "shock_types": ["G"],
            "shock_sizes": [100],
        }

        response = client.post("/api/islm/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check income increases after shock
        income = data["income"]
        assert income[15] > income[5]  # After shock > before shock

        # Check interest rate increases
        interest = data["interest_rate"]
        assert interest[15] > interest[5]

    def test_simulate_with_monetary_shock(self, standard_params):
        """Test simulation with monetary policy shock."""
        request_data = {
            "parameters": standard_params,
            "horizon": 30,
            "shock_times": [10],
            "shock_types": ["M"],
            "shock_sizes": [200],
        }

        response = client.post("/api/islm/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check income increases after shock
        income = data["income"]
        assert income[15] > income[5]

        # Check interest rate decreases
        interest = data["interest_rate"]
        assert interest[15] < interest[5]

    def test_simulate_multiple_shocks(self, standard_params):
        """Test simulation with multiple shocks."""
        request_data = {
            "parameters": standard_params,
            "horizon": 40,
            "shock_times": [10, 20, 30],
            "shock_types": ["G", "M", "T"],
            "shock_sizes": [100, 200, 50],
        }

        response = client.post("/api/islm/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check metadata contains shock information
        assert data["metadata"]["shock_times"] == [10, 20, 30]
        assert data["metadata"]["shock_types"] == ["G", "M", "T"]
        assert data["metadata"]["shock_sizes"] == [100, 200, 50]

    def test_impulse_response_fiscal(self, standard_params):
        """Test fiscal impulse response endpoint."""
        request_data = {
            "parameters": standard_params,
            "shock_type": "G",
            "shock_size": 100,
            "horizon": 20,
        }

        response = client.post("/api/islm/impulse-response", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "time" in data
        assert "income" in data
        assert "interest_rate" in data
        assert "metadata" in data

        # Check shock information in metadata
        assert data["metadata"]["shock_types"] == ["G"]
        assert data["metadata"]["shock_sizes"] == [100]

        # Income should jump after shock
        income = data["income"]
        assert income[2] > income[0]

    def test_impulse_response_monetary(self, standard_params):
        """Test monetary impulse response endpoint."""
        request_data = {
            "parameters": standard_params,
            "shock_type": "M",
            "shock_size": 200,
            "horizon": 20,
        }

        response = client.post("/api/islm/impulse-response", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Interest rate should fall after monetary expansion
        interest = data["interest_rate"]
        assert interest[2] < interest[0]

        # Income should rise
        income = data["income"]
        assert income[2] > income[0]

    def test_invalid_parameters(self):
        """Test endpoint with invalid parameters."""
        invalid_params = {
            "autonomous_consumption": -100,  # Negative (invalid)
            "mpc": 0.8,
            "autonomous_investment": 200,
            "investment_sensitivity": 50,
            "autonomous_money_demand": 50,
            "income_money_demand": 0.2,
            "interest_money_demand": 100,
            "government_spending": 250,
            "taxes": 200,
            "money_supply": 1000,
        }

        response = client.post("/api/islm/equilibrium", json=invalid_params)

        # Should return validation error
        assert response.status_code == 422

    def test_mpc_out_of_bounds(self):
        """Test endpoint with MPC out of valid range."""
        invalid_params = {
            "autonomous_consumption": 100,
            "mpc": 1.5,  # > 1 (invalid)
            "autonomous_investment": 200,
            "investment_sensitivity": 50,
            "autonomous_money_demand": 50,
            "income_money_demand": 0.2,
            "interest_money_demand": 100,
            "government_spending": 250,
            "taxes": 200,
            "money_supply": 1000,
        }

        response = client.post("/api/islm/equilibrium", json=invalid_params)

        # Should return validation error
        assert response.status_code == 422
