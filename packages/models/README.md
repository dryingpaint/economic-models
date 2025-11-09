# economic-models-models

Economic model implementations in Python.

## Purpose

Implements economic models using scientific Python stack:
- Macroeconomic models (Solow, IS-LM, DSGE, RBC)
- Microeconomic models (Supply/Demand, Market equilibrium)
- Game theory models
- Agent-based models

## Key Exports

```python
from economic_models.models import SolowGrowthModel, ISLMModel

# Create and run model
model = SolowGrowthModel(
    savings_rate=0.2,
    depreciation_rate=0.05,
    population_growth=0.01,
    alpha=0.33
)

steady_state = model.calculate_steady_state()
```

## Dependencies

- `numpy` - Numerical computations
- `scipy` - Scientific computing
- `pydantic` - Data validation

## Structure

```
src/
├── macroeconomic/      # Macro models
├── microeconomic/      # Micro models
├── game_theory/        # Game theory
├── agent_based/        # ABM
└── base.py             # Base model interface
tests/
└── test_*.py           # Tests
```

## Development

```bash
# Install with uv
uv pip install -e .

# Run tests
pytest

# Type check
mypy src/

# Format
black src/ tests/
ruff check src/ tests/
```

## Code Standards

- **Max 300-400 lines per file**
- Type hints required
- Docstrings with numpy format
- Unit tests with analytical solutions
- Clean, simple implementations

## Adding a Model

1. Create class inheriting from `EconomicModel`
2. Implement required methods
3. Add type hints and docstrings
4. Write tests against known solutions
5. Keep files < 400 lines

Example:
```python
from pydantic import BaseModel, Field
import numpy as np

class SolowParameters(BaseModel):
    savings_rate: float = Field(gt=0, lt=1)
    depreciation_rate: float = Field(gt=0, lt=1)
    alpha: float = Field(gt=0, lt=1)

class SolowGrowthModel:
    """Solow-Swan growth model."""

    def __init__(self, params: SolowParameters):
        self.params = params

    def calculate_steady_state(self) -> dict[str, float]:
        """Calculate steady state capital and output."""
        s, delta, alpha = (
            self.params.savings_rate,
            self.params.depreciation_rate,
            self.params.alpha
        )
        k_star = (s / delta) ** (1 / (1 - alpha))
        y_star = k_star ** alpha
        return {"capital": k_star, "output": y_star}
```

## Testing

```python
def test_solow_steady_state():
    params = SolowParameters(
        savings_rate=0.2,
        depreciation_rate=0.05,
        alpha=0.33
    )
    model = SolowGrowthModel(params)
    ss = model.calculate_steady_state()

    # Test against analytical solution
    expected_k = (0.2 / 0.05) ** (1 / 0.67)
    assert abs(ss["capital"] - expected_k) < 1e-6
```

## API Stability

⚠️ **Alpha** - API may change. Pin versions in production.
