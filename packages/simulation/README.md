# economic-models-simulation

Simulation engine using numerical methods.

## Ownership
**Team:** Computational Economics
**Language:** Python 3.11+
**Slack:** #team-computational-econ

## Purpose

Numerical simulation capabilities:
- ODE/PDE solvers
- Monte Carlo simulation
- Impulse response functions
- Sensitivity analysis
- Calibration algorithms

## Key Exports

```python
from economic_models.simulation import SimulationEngine, ODESolver

engine = SimulationEngine(model)
result = engine.simulate(horizon=100, shocks=[...])
```

## Dependencies

- `numpy` - Array operations
- `scipy` - Numerical solvers
- Models from `economic-models-models`

## Structure

```
src/
├── solvers/            # ODE, PDE solvers
├── monte_carlo/        # MC simulation
├── impulse_response/   # IRF computation
├── calibration/        # Parameter fitting
└── engine.py           # Main engine
tests/
└── test_*.py
```

## Development

```bash
uv pip install -e .
pytest
mypy src/
black src/ tests/
```

## Code Standards

- Max 300-400 lines per file
- Vectorized NumPy operations
- Type hints required
- Performance-critical code profiled
- Test numerical convergence

## Example

```python
import numpy as np
from scipy.integrate import odeint

class ODESolver:
    """Solve ordinary differential equations."""

    def solve(
        self,
        func: callable,
        y0: np.ndarray,
        t: np.ndarray
    ) -> np.ndarray:
        """Solve ODE using scipy."""
        return odeint(func, y0, t)
```

## Performance

- Use NumPy vectorization
- Profile before optimizing
- Consider Numba for hot loops
- Keep it simple first
