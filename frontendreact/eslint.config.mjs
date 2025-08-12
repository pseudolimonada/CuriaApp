import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";
//import { eslintConfigPrettier } from "@eslint-config-prettier/flat";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends(
    "next/core-web-vitals",
    "next/typescript",
    "next",
    "prettier",
  ),
];
//...(Array.isArray(eslintConfigPrettier) ? eslintConfigPrettier : [eslintConfigPrettier]),

export default eslintConfig;
