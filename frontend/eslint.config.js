import js from "@eslint/js"
import globals from "globals"
import react from "eslint-plugin-react"
import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"

export default [
	require("eslint-config-prettier"),
  require("eslint-plugin-prettier"),
	{ ignores: ["dist"] },
	{
		files: ["**/*.{js,jsx}"],
		languageOptions: {
			ecmaVersion: 2020,
			globals: globals.browser,
			parserOptions: {
				ecmaVersion: "latest",
				ecmaFeatures: { jsx: true },
				sourceType: "module",
			},
		},
		settings: { react: { version: "19" } },
		plugins: {
			react,
			"react-hooks": reactHooks,
			"react-refresh": reactRefresh,
		},
		rules: {
			...js.configs.recommended.rules,
			...react.configs.recommended.rules,
			...react.configs["jsx-runtime"].rules,
			...reactHooks.configs.recommended.rules,
			"react/jsx-no-target-blank": "off",
			"react/prop-types": "off",
			"no-unused-vars": "warn",
			"quotes": ["error", "double"],
			"indent": ["error", "tab"],
			"no-mixed-spaces-and-tabs": "error",
			"react/jsx-max-props-per-line": ["error", { "maximum": 3 }],
			"prettier/prettier": "error",
			"react-refresh/only-export-components": [
				"warn",
				{ allowConstantExport: true },
			],
		},
	},
]