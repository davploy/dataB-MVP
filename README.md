# dataB MVP

Small monorepo: **Vue 3 + Vite** frontend (`datab-mvp-frontend`) and **Flask** backend (`datab-mvp-backend`) for CSV upload and LLM-backed analysis.

## Prerequisites

- **Node.js** (for the frontend)
- **Python** with **Pipenv** (for the backend)

## Environment variables

Configuration lives in a **single `.env` file at the repository root** (next to this README). It is used by both the backend and the frontend.

1. Copy the example file:

   ```bash
   cp .env.example .env
   ```

   On Windows (PowerShell):

   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and set at least:

   - **`ANTHROPIC_API_KEY`** — required for `/analyze` (Claude). Get a key from [Anthropic](https://console.anthropic.com/).

3. Optional keys:

   - **`OUTPUT_SCHEMA`** — path to the JSON schema file, **relative to `datab-mvp-backend/`**. If omitted, the backend defaults to `assets/schema.json`.
   - **`VITE_API_BASE`** — full URL of the API (e.g. `http://localhost:5000`). If you leave this unset during local dev, the Vite dev server proxies `/analyze` and `/input` to Flask on port 5000, so the frontend can call those paths on the same origin as the app.

The root `.env` file is listed in `.gitignore`; do not commit secrets.

## Backend setup

```bash
cd datab-mvp-backend
pipenv install
pipenv run python inputs.py
```

This starts Flask on **http://127.0.0.1:5000** (debug mode).

## Frontend setup

```bash
cd datab-mvp-frontend
npm install
npm run dev
```

Open the URL printed in the terminal (often **http://localhost:5173** or another port if that one is busy).

## Run both at once (Windows)

From the repo root:

```bat
run.bat
```

That opens two terminals: backend (Pipenv) and frontend (`npm run dev`). Ensure the root `.env` is configured first.

## Typical local workflow

1. Create and fill in root `.env`.
2. Start the backend (Flask on port 5000).
3. Start the frontend (`npm run dev`).
4. Use the UI to upload CSV and run analysis; with `VITE_API_BASE` unset, API calls are proxied to the backend automatically.
