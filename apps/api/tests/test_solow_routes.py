"""Tests for Solow model API routes."""

import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app

client = TestClient(app)


class TestSolowRoutes:
    """Test Solow API endpoints."""

    @pytest.fixture
    def standard_params(self):
        """Standard Solow parameters for testing."""
        return {
            "savings_rate": 0.2,
            "depreciation_rate": 0.05,
            "population_growth": 0.01,
            "tech_growth": 0.02,
            "alpha": 0.33,
            "initial_capital": 1.0,
        }

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_solow_health_check(self):
        """Test Solow-specific health endpoint."""
        response = client.get("/api/solow/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model"] == "solow"

    def test_calculate_steady_state(self, standard_params):
        """Test steady state calculation endpoint."""
        response = client.post("/api/solow/steady-state", json=standard_params)

        assert response.status_code == 200
        data = response.json()

        # Check all required fields present
        assert "capital" in data
        assert "output" in data
        assert "consumption" in data
        assert "investment" in data
        assert "growth_rate" in data

        # Check values are positive
        assert data["capital"] > 0
        assert data["output"] > 0
        assert data["consumption"] > 0
        assert data["investment"] > 0
        assert data["growth_rate"] == 0.02  # Should equal tech growth

    def test_simulate_model(self, standard_params):
        """Test simulation endpoint."""
        request_data = {
            "parameters": standard_params,
            "horizon": 50,
            "time_step": 1.0,
        }

        response = client.post("/api/solow/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "time" in data
        assert "capital" in data
        assert "output" in data
        assert "consumption" in data
        assert "investment" in data
        assert "metadata" in data

        # Check arrays have same length
        n = len(data["time"])
        assert len(data["capital"]) == n
        assert len(data["output"]) == n
        assert len(data["consumption"]) == n
        assert len(data["investment"]) == n

        # Check time starts at 0
        assert data["time"][0] == 0

        # Check capital converges (last value close to steady state)
        ss_response = client.post("/api/solow/steady-state", json=standard_params)
        ss_capital = ss_response.json()["capital"]
        final_capital = data["capital"][-1]

        # Should be within 10% of steady state after 50 periods
        assert abs(final_capital - ss_capital) / ss_capital < 0.10

    def test_impulse_response(self, standard_params):
        """Test impulse response endpoint."""
        request_data = {
            "parameters": standard_params,
            "shock_var": "savings_rate",
            "shock_size": 0.1,
            "horizon": 50,
            "time_step": 1.0,
        }

        response = client.post("/api/solow/impulse-response", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "time" in data
        assert "capital" in data
        assert "metadata" in data

        # Check metadata includes shock info
        assert data["metadata"]["shock_var"] == "savings_rate"
        assert data["metadata"]["shock_size"] == 0.1

        # Capital should end higher than original steady state
        # (positive savings shock increases steady state capital)
        original_ss = data["metadata"]["initial_steady_state"]["capital"]
        final_capital = data["capital"][-1]
        assert final_capital > original_ss

    def test_invalid_parameters(self):
        """Test validation of invalid parameters."""
        invalid_params = {
            "savings_rate": 1.5,  # Invalid: must be < 1
            "depreciation_rate": 0.05,
            "population_growth": 0.01,
            "tech_growth": 0.02,
            "alpha": 0.33,
            "initial_capital": 1.0,
        }

        response = client.post("/api/solow/steady-state", json=invalid_params)
        assert response.status_code == 422  # Validation error

    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "docs" in data

    def test_openapi_docs(self):
        """Test that OpenAPI docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200

        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_spec = response.json()
        assert "paths" in openapi_spec
        assert "/api/solow/steady-state" in openapi_spec["paths"]
