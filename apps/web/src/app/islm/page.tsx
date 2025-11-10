'use client'

import { ISLMSimulation } from '@economic-models/ui-components'

export default function ISLMPage() {
  return (
    <main className="container">
      <header>
        <h1>IS-LM Model</h1>
        <p>Short-run macroeconomic equilibrium and policy analysis</p>
      </header>

      <section>
        <ISLMSimulation />
      </section>

      <footer>
        <p>
          Interactive IS-LM model for analyzing fiscal and monetary policy effects
        </p>
      </footer>
    </main>
  )
}
