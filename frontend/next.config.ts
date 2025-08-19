import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    reactCompiler: true,
  },
  sassOptions: {
    additionalData: `$var: red;`,
    implementation: 'sass-embedded',
  },
};

export default nextConfig;
