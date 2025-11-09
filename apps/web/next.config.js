/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: [
    '@economic-models/core',
    '@economic-models/visualization',
    '@economic-models/ui-components',
  ],
}

module.exports = nextConfig
