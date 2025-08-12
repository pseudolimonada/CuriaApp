import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    reactCompiler: {
      compilationMode: "annotation",
    },
  },
};
module.exports = {
  eslint: {
    rules: {
      "react-hooks/react-compiler": "error",
    },
  },
};

export default nextConfig;
