# @economic-models/data

Data integration, management, and preprocessing for economic analysis.

## Ownership
**Team:** Data Engineering
**Lead:** TBD
**Slack:** #team-data-engineering

## Purpose

This package handles:
- Real-world economic data sources (FRED, World Bank, IMF, OECD, BLS)
- Data fetching and caching
- Data preprocessing and cleaning
- Time series transformations
- Data validation
- Model calibration helpers

## Key Exports

```typescript
// Data sources
export class FREDDataSource { ... }
export class WorldBankDataSource { ... }
export class IMFDataSource { ... }

// Data management
export class DataManager { ... }

// Preprocessing
export function cleanTimeSeries(data): TimeSeries
export function interpolateMissingValues(data): TimeSeries
export function transformData(data, transformation): TimeSeries
```

## Dependencies

- `@economic-models/core` - Base types
- `axios` - HTTP client

## Dependents

- `@economic-models/analysis` - Uses real data
- `@economic-models/simulation` - Calibration
- `apps/api` - Data endpoints

## Getting Started

```bash
cd packages/data
npm install
npm run dev
npm run test
```

## Directory Structure

```
src/
├── sources/            # Data source connectors
│   ├── fred.ts         # FRED API
│   ├── world-bank.ts   # World Bank API
│   ├── imf.ts          # IMF data
│   └── oecd.ts         # OECD data
├── cache/              # Caching layer
├── preprocessing/      # Data cleaning and transformation
├── validation/         # Data quality checks
└── calibration/        # Calibration utilities
```

## Development Guidelines

### Adding a New Data Source

1. Implement `DataSource` interface
2. Add API authentication handling
3. Implement rate limiting
4. Add caching layer
5. Document API limitations
6. Add integration tests (with mocking)

### API Keys and Credentials

- Never commit API keys
- Use environment variables
- Document required credentials in README
- Provide example `.env.example` file

## Testing

- Mock external API calls in tests
- Test data validation logic
- Test transformation functions
- Integration tests with real APIs (CI only)

## API Rate Limits

| Source      | Rate Limit           | Notes                    |
|-------------|----------------------|--------------------------|
| FRED        | No stated limit      | Be respectful            |
| World Bank  | No stated limit      | 120 requests/minute recommended |
| IMF         | Varies by endpoint   | Check documentation      |
| OECD        | No stated limit      | Cache aggressively       |

## Examples

```typescript
import { FREDDataSource, DataManager } from '@economic-models/data'

const fred = new FREDDataSource({ apiKey: process.env.FRED_API_KEY })
const manager = new DataManager()

const gdp = await fred.getSeries('GDP')
const cleaned = manager.cleanAndValidate(gdp)
```

## API Stability

⚠️ **Alpha** - Data source APIs may change as we learn usage patterns.
