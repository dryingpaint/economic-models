'use client'

import { SolowSimulation } from '@economic-models/ui-components'

export default function Home() {
  return (
    <main className="container">
      <header>
        <h1>Economic Models Platform</h1>
        <p>Interactive Solow Growth Model</p>
      </header>

      <section>
        <SolowSimulation />
      </section>

      <footer>
        <p>
          Built with Python (FastAPI), TypeScript (Next.js), and economic theory
        </p>
      </footer>
    </main>
  )
}
