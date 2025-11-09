# @economic-models/web

Main web application for the economic models platform.

## Purpose

This is the primary user-facing web application built with Next.js. It provides:
- Interactive model exploration
- Real-time simulations
- Educational content
- Data visualization
- Model comparison tools
- User workspace and saved scenarios

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **UI Library:** React 18
- **Styling:** TBD (Tailwind/CSS Modules/styled-components)
- **State Management:** TBD (React Context/Zustand/Redux)
- **Authentication:** TBD (NextAuth/Auth0/Clerk)

## Dependencies

All `@economic-models/*` packages

## Getting Started

```bash
cd apps/web
npm install
npm run dev  # Starts on http://localhost:3000
```

## Directory Structure

```
app/                    # Next.js app directory
├── (marketing)/        # Marketing pages
│   └── page.tsx        # Landing page
├── models/             # Model exploration
│   ├── page.tsx        # Model catalog
│   └── [id]/           # Individual model pages
├── simulate/           # Interactive simulation
├── analyze/            # Analysis tools
├── learn/              # Educational content
└── api/                # API routes

components/             # App-specific components
lib/                    # Utilities and helpers
public/                 # Static assets
styles/                 # Global styles
```

## Key Features

### 1. Model Catalog
Browse and search economic models with filters by type, complexity, and use case.

### 2. Interactive Simulation
- Real-time parameter adjustment
- Multiple visualization options
- Shock simulation
- Scenario comparison

### 3. Educational Platform
- Model explanations with math
- Step-by-step guides
- Interactive tutorials
- Video content

### 4. Analysis Workspace
- Policy analysis tools
- Custom scenarios
- Save and share results
- Export capabilities

## Development Guidelines

### Page Structure
- Use Next.js App Router
- Implement proper loading and error states
- Add metadata for SEO
- Optimize for performance (lazy loading, code splitting)

### Performance Targets
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.0s
- Lighthouse Score: > 90

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- Color contrast compliance

## Environment Variables

Create `.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001

# Analytics (optional)
NEXT_PUBLIC_ANALYTICS_ID=

# Feature Flags
NEXT_PUBLIC_ENABLE_AUTH=false
```

## Testing

- Unit tests: Component logic
- Integration tests: User flows
- E2E tests: Critical paths (Playwright)
- Visual regression: Storybook + Chromatic

## Deployment

- **Platform:** Vercel (recommended) / AWS / GCP
- **CI/CD:** GitHub Actions
- **Preview:** Automatic for PRs
- **Production:** Merge to main

## API Stability

⚠️ **Alpha** - Rapid iteration on UX and features.
