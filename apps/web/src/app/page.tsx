'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="container">
      <header>
        <h1>Economic Models Platform</h1>
        <p>Interactive macroeconomic models for teaching and research</p>
      </header>

      <section style={{ marginTop: '40px' }}>
        <h2>Available Models</h2>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', marginTop: '30px' }}>
          <Link href="/solow" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div style={{
              border: '2px solid #0070f3',
              borderRadius: '8px',
              padding: '30px',
              cursor: 'pointer',
              transition: 'transform 0.2s',
            }}
            onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
            onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              <h3 style={{ marginTop: 0 }}>Solow Growth Model</h3>
              <p>Long-run economic growth through capital accumulation</p>
              <ul>
                <li>Production function: Y = K^α (AL)^(1-α)</li>
                <li>Steady-state analysis</li>
                <li>Golden rule of capital</li>
                <li>Convergence dynamics</li>
              </ul>
            </div>
          </Link>

          <Link href="/islm" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div style={{
              border: '2px solid #10b981',
              borderRadius: '8px',
              padding: '30px',
              cursor: 'pointer',
              transition: 'transform 0.2s',
            }}
            onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
            onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              <h3 style={{ marginTop: 0 }}>IS-LM Model</h3>
              <p>Short-run equilibrium and policy analysis</p>
              <ul>
                <li>IS curve: Goods market equilibrium</li>
                <li>LM curve: Money market equilibrium</li>
                <li>Fiscal policy effects (G, T)</li>
                <li>Monetary policy effects (M)</li>
              </ul>
            </div>
          </Link>
        </div>
      </section>

      <footer style={{ marginTop: '60px' }}>
        <p>
          Built with Python (FastAPI), TypeScript (Next.js), and economic theory
        </p>
      </footer>
    </main>
  )
}
