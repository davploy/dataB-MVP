<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  csvText: String
})

const emit = defineEmits(['analyze-result'])

const analyzing = ref(false)

function apiUrl(path) {
  const base = String(import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}

async function onAnalyze() {
  if (!props.csvText?.trim()) return

  analyzing.value = true
  try {
    const response = await axios.post(apiUrl('/analyze'), props.csvText, {
      headers: { 'Content-Type': 'text/csv' }
    })
    emit('analyze-result', {
      ok: response.data.status === 'success',
      analysis: response.data.result
    })
  } catch (err) {
    emit('analyze-result', { ok: false, analysis: null })
  } finally {
    analyzing.value = false
  }
}
</script>

<template>
  <button
    type="button"
    :disabled="analyzing || !csvText"
    @click="onAnalyze"
  >
    {{ analyzing ? 'Analyzing…' : 'Analyze with LLM' }}
  </button>
</template>

<style scoped>
button {
  font: inherit;
  cursor: pointer;
  padding: 10px 14px;
  border-radius: 6px;
  border: 2px solid transparent;
  color: var(--accent);
  background: var(--accent-bg);
  transition: border-color 0.2s;
}

button:hover:not(:disabled) {
  border-color: var(--accent-border);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>