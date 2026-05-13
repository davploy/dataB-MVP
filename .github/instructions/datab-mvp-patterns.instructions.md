---
description: "Use when building Vue 3 components, Flask API routes, or any frontend/backend code for the DataB MVP. Covers Composition API patterns, component structure, async error handling, and API design conventions."
---

# DataB MVP — Code Patterns & Conventions

This project spans a Flask backend (Python 3.14) and a Vue 3 + Vite frontend. Follow these patterns to maintain consistency and clarity across the codebase.

## Frontend: Vue 3 Components

### Structure & Setup

All Single-File Components must use **Vue 3 Composition API** with **`<script setup>`**:

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const isLoading = ref(false)
const items = ref([])

const itemCount = computed(() => items.value.length)

onMounted(async () => {
  // Initialize here
})
</script>

<template>
  <div class="component-root">
    <p v-if="isLoading">Loading...</p>
    <p v-else>Count: {{ itemCount }}</p>
  </div>
</template>

<style scoped>
.component-root {
  /* Styles here */
}
</style>
```

**Never use the Options API** (`export default { data, methods, ... }`).

### Props & Emits

Use `defineProps` and `defineEmits` for type clarity:

```vue
<script setup>
defineProps({
  label: String,
  disabled: Boolean,
})

const emit = defineEmits(['click', 'update'])

function handleClick() {
  emit('click', { timestamp: Date.now() })
}
</script>
```

### State Management

- Use `ref()` for reactive primitives and objects.
- Use `computed()` for derived state (don't mutate, only read).
- Keep component state **flat and localized**; avoid deeply nested reactivity.

```vue
<script setup>
const message = ref('')
const isError = ref(false)

// ✅ Good: computed derives from refs
const displayMessage = computed(() => 
  isError.value ? `Error: ${message.value}` : message.value
)

// ❌ Avoid: mutating computed (read-only derived state)
// const message = computed(() => { message.value = 'x' }) // ❌
</script>
```

### Async & Error Handling

Use **try/catch** for async operations. Leverage **axios error detection** for HTTP errors:

```vue
<script setup>
import axios from 'axios'

const data = ref(null)
const error = ref(null)
const loading = ref(false)

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/api/data')
    data.value = response.data
  } catch (err) {
    if (axios.isAxiosError(err)) {
      error.value = `HTTP ${err.response?.status}: ${err.message}`
    } else {
      error.value = err instanceof Error ? err.message : 'Unknown error'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <button @click="fetchData" :disabled="loading">Load</button>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-else-if="data">{{ data }}</p>
  </div>
</template>
```

### Naming Conventions

- **Component files**: PascalCase (e.g., `UploadComponent.vue`, `InputField.vue`)
- **Refs and computed**: camelCase (e.g., `isLoading`, `selectedFile`)
- **Events**: kebab-case in templates, camelCase in `defineEmits` (e.g., `@upload-result` emits `uploadResult`)
- **CSS classes**: kebab-case (e.g., `.upload-button`, `.error-message`)

### Styling

- Use **scoped styles** (`<style scoped>`) unless global styles are explicitly needed.
- Reference **global CSS variables** from `src/style.css` for consistency:
  - `--text`, `--text-h` (text colors)
  - `--bg`, `--border` (backgrounds & borders)
  - `--accent`, `--accent-bg` (brand colors)
  - `--code-bg`, `--mono` (code styling)
  - `--shadow` (shadows)

```vue
<style scoped>
.upload-button {
  border: 1px solid var(--border);
  color: var(--text);
  background: var(--bg);
  box-shadow: var(--shadow);
}

.upload-button:hover {
  border-color: var(--accent);
}
</style>
```

## Frontend: API Integration

### Base URL Resolution

Resolve API URLs using environment variables, with fallback to relative paths:

```javascript
export function apiUrl(path) {
  const base = String(import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}

// Usage
const response = await axios.post(apiUrl('/input'), file)
```

### File Uploads

When uploading files (e.g., CSV), send them as raw request bodies with proper MIME type:

```javascript
const file = event.target.files[0]
await axios.post(apiUrl('/input'), file, {
  headers: {
    'Content-Type': file.type || 'text/csv',
  },
})
```

Don't use FormData unless the API explicitly requires it.

## Backend: Flask Routes

### Structure

Organize routes logically, group by resource, and always specify request methods:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5000", "http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/input', methods=['POST'])
def input_handler():
    """Handle CSV file upload."""
    csv_data = request.data.decode('utf-8')
    # Process...
    return {'status': 'received'}, 200

@app.route('/status', methods=['GET'])
def get_status():
    """Return server status."""
    return {'healthy': True}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Response Format

Always return JSON with consistent structure:

```python
# ✅ Good: structured response
return {
    'status': 'success',
    'data': {...},
    'message': 'Operation completed'
}, 200

# ✅ Also good: error response with status code
return {
    'status': 'error',
    'message': 'File format not supported'
}, 400
```

### Error Handling

Handle exceptions gracefully and return appropriate HTTP status codes:

```python
@app.route('/input', methods=['POST'])
def input_handler():
    try:
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            return {'status': 'error', 'message': 'Empty file'}, 400
        # Process...
        return {'status': 'success', 'data': result}, 200
    except UnicodeDecodeError:
        return {'status': 'error', 'message': 'File must be valid UTF-8'}, 400
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500
```

## Cross-Cutting Patterns

### Logging

Frontend: Use `console.log` during development; consider structured logging in production.

Backend: Use Python's `logging` module:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Processing file")
logger.error("File upload failed", exc_info=True)
```

### Environment Configuration

Frontend: Use `.env.local` and `import.meta.env.*`:

```javascript
const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:5000'
```

Backend: Use environment variables or a `config.py`:

```python
import os
DEBUG = os.getenv('DEBUG', 'False') == 'True'
API_PORT = int(os.getenv('API_PORT', '5000'))
```

### Code Comments

- Use comments sparingly; prefer clear naming and structure.
- For complex logic, explain *why*, not *what*:

```javascript
// ✅ Good: explains intent
// Trim trailing slashes to avoid double-slash in concatenation
const base = String(import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')

// ❌ Avoid: states the obvious
// Split the string at '/'
const parts = url.split('/')
```

---

**Questions?** Refer to the existing code in `datab-mvp-frontend/` and `datab-mvp-backend/` for examples, or update this file to reflect new patterns as the project evolves.
