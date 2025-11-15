import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ['@privy-io/react-auth'],

  webpack: (config, { isServer }) => {
    // Fix for Privy wallet connector issues
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
        encoding: false,
      };
    }

    // Ignore test files from wallet packages
    config.module.rules.push({
      test: /\.test\.(ts|js)$/,
      loader: 'ignore-loader',
    });

    // Ignore helper files in test directories
    config.module.rules.push({
      test: /\/test\/helper\.(ts|js)$/,
      loader: 'ignore-loader',
    });

    return config;
  },
};

export default nextConfig;
