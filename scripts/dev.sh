#!/bin/bash
set -e

echo "🚀 Starting Economic Models Platform..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "${BLUE}Creating Python virtual environment...${NC}"
    uv venv
fi

# Install Python dependencies
echo "${BLUE}Installing Python dependencies...${NC}"
uv pip install -e .
echo "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Install TypeScript dependencies
echo "${BLUE}Installing TypeScript dependencies...${NC}"
pnpm install
echo "${GREEN}✓ TypeScript dependencies installed${NC}"
echo ""

# Build TypeScript packages
echo "${BLUE}Building TypeScript packages...${NC}"
pnpm run build
echo "${GREEN}✓ TypeScript packages built${NC}"
echo ""

# Start development servers
echo "${GREEN}Starting development servers...${NC}"
echo ""
echo "  📍 FastAPI backend: http://localhost:8000"
echo "  📍 FastAPI docs:    http://localhost:8000/docs"
echo "  📍 Next.js frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "${BLUE}Shutting down servers...${NC}"
    kill 0
}
trap cleanup EXIT

# Activate virtual environment and start FastAPI in background
source .venv/bin/activate
uvicorn apps.api.src.main:app --reload --host 0.0.0.0 --port 8000 &

# Start Next.js dev server in background
cd apps/web
pnpm run dev &

# Wait for all background processes
wait
