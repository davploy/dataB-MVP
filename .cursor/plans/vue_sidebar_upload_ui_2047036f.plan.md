---
name: Vue sidebar upload UI
overview: Implement a minimal Vue 3 (Composition API, `<script setup>`) shell with a sidebar containing CSV upload to `POST /input`, plus a main viewer panel. Align layout with existing CSS variables and lightly adjust global `#app` styles so the dashboard is full-width.
todos:
  - id: adjust-global-app-css
    content: "Tweak style.css #app (full width, align left) for sidebar shell"
    status: completed
  - id: implement-upload-component
    content: "Build UploadComponent.vue: file input, CSV check, axios POST /input (raw file body), emit optional result"
    status: completed
  - id: implement-app-layout
    content: "Build App.vue: flex sidebar + viewer, wire UploadComponent and optional viewer feedback"
    status: completed
isProject: false
---

# Simple Vue 3 sidebar + CSV upload plan

## Current state

- Stack: Vue `^3.5`, Vite `^8`, [`@vitejs/plugin-vue`](datab-mvp-frontend/vite.config.js). Entry: [`main.js`](datab-mvp-frontend/src/main.js) mounts `App`.
- [`App.vue`](datab-mvp-frontend/src/App.vue) and [`UploadComponent.vue`](datab-mvp-frontend/src/components/UploadComponent.vue) are empty.
- Global [`style.css`](datab-mvp-frontend/src/style.css) styles `#app` as a **1126px-centered, column flex** shell with centered text—fine for the old Vite template, wrong for a sidebar app. One small update there avoids fighting the layout from every child.

## Layout ([`App.vue`](datab-mvp-frontend/src/App.vue))

- Single-file component with **`<script setup lang="ts">`** — if the project has no TypeScript dependency yet, use plain `<script setup>` (JavaScript only) to avoid adding `@vue/tsconfig` / `vue-tsc` unless you want TS; **default recommendation: stay on JS** to match current `main.js` and keep scope minimal.
- Structure:
  - Root: horizontal flex, full viewport height (`min-height: 100vh`), sidebar fixed width (e.g. `280px`), main area `flex: 1`.
  - **Sidebar**: heading + [`UploadComponent`](datab-mvp-frontend/src/components/UploadComponent.vue).
  - **Viewer**: a simple `<main>` with a title and placeholder text; optionally show **last upload status** (filename, HTTP status, short message) via an `@upload-result` (or similar) emit from the upload component so the viewer is not purely dead UI—still a few lines, no router/store.

Use existing CSS variables from `style.css` (`--border`, `--text`, `--text-h`, `--accent`) for borders and typography so it stays visually consistent.

## Upload ([`UploadComponent.vue`](datab-mvp-frontend/src/components/UploadComponent.vue))

- Add **`axios`** as a runtime dependency in [`package.json`](datab-mvp-frontend/package.json) (`npm install axios`).
- Hidden `<input type="file" accept=".csv,text/csv" />` + visible button/label to trigger it.
- On file chosen:
  - If the file is not CSV by extension/MIME, show a brief inline error and return.
  - **`POST`** to **`/input`** using **`axios.post`**, sending the selected **`File`** as the **request body** (no `FormData`): e.g. `axios.post(url, file, { headers: { 'Content-Type': file.type || 'text/csv' } })`. Keeps the implementation small and avoids manual multipart assembly.
  - Handle success with `response.data`; handle failures with `try/catch` and `axios.isAxiosError` for HTTP errors and network errors. Minimal UX: `uploading` state and a short success/error message.
- **Base URL**: Resolve the URL as **`${import.meta.env.VITE_API_BASE ?? ''}/input`** (trim slash duplication if needed), or a tiny helper so dev can use a relative `/input` when `VITE_API_BASE` is unset. When the API is on another origin during dev, use Vite [`server.proxy`](https://vite.dev/config/server-options.html#server-proxy) in [`vite.config.js`](datab-mvp-frontend/vite.config.js) pointing `/input` to your backend (optional until the backend URL is known).

**Note:** This assumes the backend accepts a **raw CSV body** on `POST /input`. If the backend instead expects **`multipart/form-data`**, you must either change the API to accept raw bodies or use `FormData` with axios (multipart)—confirm with the server contract below.

## Global CSS tweak ([`style.css`](datab-mvp-frontend/src/style.css))

- Adjust `#app` so the app shell is **full width**, **left-aligned text**, and suitable as a flex container for the new layout (e.g. `width: 100%`, `max-width: none`, `margin: 0`, drop or soften `text-align: center` and the narrow max-width). Optionally remove or narrow the vertical side borders on `#app` if they clash with the sidebar—your call during implementation for a clean look.

## Files to touch

| File | Change |
|------|--------|
| [`datab-mvp-frontend/package.json`](datab-mvp-frontend/package.json) | Add `axios` dependency |
| [`datab-mvp-frontend/src/App.vue`](datab-mvp-frontend/src/App.vue) | Sidebar + viewer layout, import `UploadComponent`, optional handler for upload emit |
| [`datab-mvp-frontend/src/components/UploadComponent.vue`](datab-mvp-frontend/src/components/UploadComponent.vue) | File input, `axios.post` `/input` (raw `File` body), loading/error UI, optional emit |
| [`datab-mvp-frontend/src/style.css`](datab-mvp-frontend/src/style.css) | Minimal `#app` (and if needed `body`) adjustments for full-width dashboard |

Optional later (not required for MVP): [`vite.config.js`](datab-mvp-frontend/vite.config.js) proxy block when the backend URL is fixed.

## Backend contract (for whoever implements `/input`)

- **Method**: `POST`
- **Path**: `/input` (or prefixed if you use `VITE_API_BASE`)
- **Body**: **Raw CSV bytes** with `Content-Type` typically `text/csv` (or the browser-provided file MIME type). Not multipart when following this plan.
- **Response**: Any JSON or text is fine; the UI can show status + `response.data` on success/error (axios).
