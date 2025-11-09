# @economic-models/api

REST API server for the economic models platform.

## Ownership
**Team:** Backend Engineering
**Lead:** TBD
**Slack:** #team-backend

## Purpose

This API provides HTTP endpoints for:
- Running model simulations
- Fetching economic data
- Performing analysis
- Managing user workspaces (future)
- Model catalog queries

## Tech Stack

- **Framework:** Express.js
- **Runtime:** Node.js 18+
- **Validation:** Zod
- **Documentation:** OpenAPI/Swagger
- **Database:** TBD (PostgreSQL/MongoDB)

## Dependencies

- `@economic-models/core`
- `@economic-models/models`
- `@economic-models/simulation`
- `@economic-models/data`
- `@economic-models/analysis`

## Getting Started

```bash
cd apps/api
npm install
npm run dev  # Starts on http://localhost:3001
```

## Directory Structure

```
src/
├── routes/             # Route definitions
│   ├── models.ts       # /api/models
│   ├── simulate.ts     # /api/simulate
│   ├── data.ts         # /api/data
│   └── analyze.ts      # /api/analyze
├── controllers/        # Request handlers
├── middleware/         # Express middleware
├── services/           # Business logic
├── validators/         # Request validation
└── index.ts            # Server entry point
```

## API Endpoints

### Models
- `GET /api/models` - List all models
- `GET /api/models/:id` - Get model details
- `GET /api/models/:id/parameters` - Get model parameters

### Simulation
- `POST /api/simulate` - Run simulation
- `POST /api/simulate/impulse-response` - Compute IRF
- `POST /api/simulate/sensitivity` - Sensitivity analysis

### Data
- `GET /api/data/sources` - List data sources
- `GET /api/data/:source/:series` - Fetch time series
- `POST /api/data/transform` - Transform data

### Analysis
- `POST /api/analyze/comparative-statics` - Run comparative statics
- `POST /api/analyze/policy` - Policy analysis
- `POST /api/analyze/welfare` - Welfare analysis

## Development Guidelines

### Request Validation
Always validate requests with Zod schemas:

```typescript
import { z } from 'zod'

const simulateSchema = z.object({
  modelId: z.string(),
  parameters: z.record(z.number()),
  horizon: z.number().positive()
})

app.post('/api/simulate', async (req, res) => {
  const body = simulateSchema.parse(req.body)
  // ...
})
```

### Error Handling
Use consistent error responses:

```typescript
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameters",
    "details": { ... }
  }
}
```

### Rate Limiting
- Implement rate limiting for compute-intensive endpoints
- Document limits in API docs
- Return 429 with Retry-After header

### Caching
- Cache simulation results by hash of inputs
- Cache data fetches with appropriate TTL
- Use Redis for distributed caching (future)

## Environment Variables

Create `.env`:

```bash
# Server
PORT=3001
NODE_ENV=development

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Data Sources
FRED_API_KEY=your_key_here
WORLD_BANK_API_KEY=your_key_here

# Cache
REDIS_URL=redis://localhost:6379
```

## Testing

- Unit tests: Controllers and services
- Integration tests: Full API endpoints
- Load tests: Performance benchmarks

## Performance

- Response time targets: < 200ms (catalog), < 2s (simulation)
- Implement streaming for large datasets
- Use worker threads for CPU-intensive computations
- Monitor with APM tools (New Relic/DataDog)

## API Documentation

API docs auto-generated from OpenAPI spec and available at `/api/docs`

## Deployment

- **Platform:** AWS ECS / GCP Cloud Run / Railway
- **CI/CD:** GitHub Actions
- **Monitoring:** DataDog / New Relic
- **Logging:** Winston + CloudWatch

## API Stability

⚠️ **Alpha** - API versioning will be added before beta.
