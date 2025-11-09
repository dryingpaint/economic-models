# economic-models-analysis

Statistical analysis and policy tools.

## Ownership
**Team:** Economic Analysis
**Language:** Python 3.11+
**Slack:** #team-economic-analysis

## Purpose

Analysis capabilities:
- Comparative statics
- Policy scenario analysis
- Welfare analysis
- Statistical tests
- Model validation

## Key Exports

```python
from economic_models.analysis import (
    ComparativeStaticsAnalyzer,
    PolicyAnalyzer
)

analyzer = PolicyAnalyzer(model)
result = analyzer.compare_scenarios(baseline, policy)
```

## Dependencies

- `numpy`, `scipy` - Numerical work
- `pandas` - Data handling
- Models and simulation packages

## Structure

```
src/
├── comparative_statics/
├── policy/
├── welfare/
├── validation/
└── statistics/
tests/
└── test_*.py
```

## Development

```bash
uv pip install -e .
pytest
mypy src/
```

## Code Standards

- Max 300-400 lines per file
- Statistical rigor
- Confidence intervals
- Clear assumptions
- Test against known results
