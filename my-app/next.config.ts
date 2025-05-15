import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  reactStrictMode: true,
  basePath: '/Project1/my-app', // Matches your GitHub Pages URL (https://datav1nci.github.io/Project1/)
};

export default nextConfig;