import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";
import { defineConfig } from "eslint/config";
import react from "eslint-plugin-react";
import { FlatCompat } from "@eslint/eslintrc";
import reactHooks from "eslint-plugin-react-hooks";

const compat = new FlatCompat({
  // import.meta.dirname is available after Node.js v20.11.0
  baseDirectory: import.meta.dirname,
  recommendedConfig: js.configs.recommended,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript", "prettier"),
  ...compat.config({
    extends: ["eslint:recommended", "next"],
    rules: {
      "react/no-unescaped-entities": "off",
      "@next/next/no-page-custom-font": "off",
    },
  }),
];

export default defineConfig([
  eslintConfig,
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    plugins: { js },
    extends: ["js/recommended"],
    languageOptions: { globals: globals.browser },
  },
  //{ files: ["**/*.{ts,tsx}"], plugins: { tseslint }, languageOptions: { parserOptions: tseslint.parserOptions } },
  // { files: ["**/*.{js,jsx}"], plugins: { react: pluginReact }, languageOptions: { parserOptions: pluginReact.parserOptions } },
  //{ files: ["**/*.{js,jsx,ts,tsx}"], plugins: { reactHooks }, languageOptions: { parserOptions: reactHooks.parserOptions } },
  tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,
  pluginReact.configs.flat["jsx-runtime"],
  //reactHooks.configs['recommended-latest'],
  {
    files: ["**/*.{js,jsx,mjs,cjs,ts,tsx}"],
    plugins: {
      react,
    },
    languageOptions: {
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      // ... any rules you want
      "react/jsx-uses-react": "error",
      "react/jsx-uses-vars": "error",
    },
    // ... others are omitted for brevity
  },
  {
    files: ["**/*.js,jsx"],
    plugins: { "react-hooks": reactHooks },
    // ...
    rules: {
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      "react-hooks/react-compiler": "error",
    },
  },
]);
