<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['upload-result'])

const fileInput = ref(null)
const uploading = ref(false)
const message = ref('')
const messageKind = ref('')

/** `${VITE_API_BASE}` + path (no trailing slash on base). */
function apiUrl(path) {
  const base = String(import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}

function isCsvFile(file) {
  const lower = file.name.toLowerCase()
  if (!lower.endsWith('.csv')) return false
  if (!file.type) return true
  return (
    file.type === 'text/csv' ||
    file.type === 'application/csv' ||
    file.type === 'application/vnd.ms-excel' ||
    file.type.includes('csv')
  )
}

async function onFileChange(event) {
  const input = event.target
  const file = input.files?.[0]
  input.value = ''
  if (!file) return

  if (!isCsvFile(file)) {
    const detail = 'Please choose a .csv file.'
    message.value = detail
    messageKind.value = 'error'
    emit('upload-result', {
      filename: file.name,
      ok: false,
      status: null,
      detail,
      analysis: response.data
    })
    return
  }

  uploading.value = true
  message.value = ''
  messageKind.value = ''

  let csvText = ''
  try {
    csvText = await file.text()
  } catch {
    uploading.value = false
    const detail = 'Could not read the file.'
    message.value = detail
    messageKind.value = 'error'
    emit('upload-result', {
      filename: file.name,
      ok: false,
      status: null,
      detail,
    })
    return
  }

  try {
    const url = apiUrl('/input')
    const response = await axios.post(url, csvText, {
      headers: {
        'Content-Type': 'text/csv',
      },
    })
    message.value = 'Upload successful.'
    messageKind.value = 'success'
    const detail =
      typeof response.data === 'string'
        ? response.data
        : JSON.stringify(response.data, null, 2)
    emit('upload-result', {
      filename: file.name,
      ok: true,
      status: response.status,
      detail,
      data: response.data,
      csvText,
    })
  } catch (err) {
    let detail = 'Upload failed.'
    let status = null
    if (axios.isAxiosError(err)) {
      status = err.response?.status ?? null
      const data = err.response?.data
      if (typeof data === 'string') detail = data
      else if (data != null) detail = JSON.stringify(data, null, 2)
      else if (err.message) detail = err.message
    }
    message.value = detail
    messageKind.value = 'error'
    emit('upload-result', {
      filename: file.name,
      ok: false,
      status,
      detail,
      csvText,
    })
  } finally {
    uploading.value = false
  }
}

function triggerPick() {
  fileInput.value?.click()
}
</script>

<template>
  <div class="upload">
    <input
      ref="fileInput"
      type="file"
      accept=".csv,text/csv"
      class="visually-hidden"
      :disabled="uploading"
      @change="onFileChange"
    />
    <button
      type="button"
      class="upload-btn"
      :disabled="uploading"
      @click="triggerPick"
    >
      {{ uploading ? 'Uploading…' : 'Choose CSV' }}
    </button>
    <p v-if="message" class="hint" :data-kind="messageKind || undefined">
      {{ message }}
    </p>
  </div>
</template>

<style scoped>
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.upload {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upload-btn {
  font: inherit;
  cursor: pointer;
  padding: 10px 14px;
  border-radius: 6px;
  border: 2px solid transparent;
  color: var(--accent);
  background: var(--accent-bg);
  transition: border-color 0.2s;
}

.upload-btn:hover:not(:disabled) {
  border-color: var(--accent-border);
}

.upload-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.upload-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.hint {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
  word-break: break-word;
}

.hint[data-kind='error'] {
  color: var(--text-h);
}

.hint[data-kind='success'] {
  color: var(--accent);
}
</style>
