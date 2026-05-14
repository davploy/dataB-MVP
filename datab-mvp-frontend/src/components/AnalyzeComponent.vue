<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  csvText: String
})

const emit = defineEmits(['analyze-result'])

const analyzing = ref(false)
const message = ref('')
const messageKind = ref('')

function apiUrl(path) {
  const base = String(import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}

async function onAnalyze() {
  if (!props.csvText?.trim()) return

  analyzing.value = true
  message.value = ''
  messageKind.value = ''
  try {
    const response = await axios.post(apiUrl('/analyze'), props.csvText, {
      headers: { 'Content-Type': 'text/csv' }
    })
    const ok = response.data.status === 'success'
    if (ok) {
      message.value = 'Analysis successful'
      messageKind.value = 'success'
    } else {
      message.value = 'Analysis failed.'
      messageKind.value = 'error'
    }
    emit('analyze-result', {
      ok,
      analysis: response.data.result
    })
  } catch (err) {
    message.value = 'Analysis failed.'
    messageKind.value = 'error'
    emit('analyze-result', { ok: false, analysis: null })
  } finally {
    analyzing.value = false
  }
}
</script>

<template>
  <div class="analyze">
    <button
      type="button"
      :disabled="analyzing || !csvText"
      @click="onAnalyze"
    >
      {{ analyzing ? 'Analyzing…' : 'Analyze with LLM' }}
    </button>
    <p v-if="message" class="hint" :data-kind="messageKind || undefined">
      {{ message }}
    </p>
  </div>
</template>

<style scoped>
.analyze {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

button {
  width: 100%;
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

.hint {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
  word-break: break-word;
  text-align: center;
}

.hint[data-kind='error'] {
  color: var(--error);
}

.hint[data-kind='success'] {
  color: var(--success);
}
</style>