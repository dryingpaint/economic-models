'use client'

import { SolowSimulation } from '@economic-models/ui-components'

export default function SolowPage() {
  return (
    <main className="container">
      <header>
        <h1>Solow Growth Model</h1>
        <p>Long-run economic growth through capital accumulation</p>
      </header>

      <section>
        <SolowSimulation />
      </section>

      <footer>
        <p>
          Interactive Solow-Swan growth model with steady-state analysis
        </p>
      </footer>
    </main>
  )
}
