<script setup>
import { ref } from 'vue'
import UploadComponent from './components/UploadComponent.vue'
import AnalyzeComponent from './components/AnalyzeComponent.vue'

const lastResult = ref(null)
const analysisResult = ref(null)

function onUploadResult(payload) {
  lastResult.value = payload
  analysisResult.value = null
}

function onAnalyzeResult(payload) {
  if (payload.ok) {
    analysisResult.value = payload.analysis
  }
}
</script>

<template>
  <div class="shell">
    <aside class="sidebar" aria-label="Upload">
      <h2 class="sidebar-title">Upload</h2>
      <UploadComponent @upload-result="onUploadResult" />
      <AnalyzeComponent 
        :csv-text="lastResult?.csvText" 
        @analyze-result="onAnalyzeResult"
      />
    </aside>
    <main class="viewer">
      <h2 class="viewer-title">Viewer</h2>
      <p v-if="!lastResult" class="muted">
        Upload a CSV to see the response here.
      </p>
      <template v-else>
        <p class="meta">
          <strong>{{ lastResult.filename }}</strong>
          <span class="sep">·</span>
          <span :class="lastResult.ok ? 'state-ok' : 'state-err'">
            {{ lastResult.ok ? 'OK' : 'Error' }}
            <template v-if="lastResult.status != null">
              ({{ lastResult.status }})
            </template>
          </span>
        </p>
        <template v-if="lastResult.csvText">
          <h3 class="section-title">CSV (from your file)</h3>
          <pre class="preview">{{ lastResult.csvText }}</pre>
        </template>
        <template v-if="lastResult.detail">
          <h3 class="section-title">Server / upload message</h3>
          <pre class="preview detail-preview">{{ lastResult.detail }}</pre>
        </template>
        <template v-if="analysisResult">
          <h3 class="section-title">Analysis Result (from LLM)</h3>
          <pre class="preview">{{ JSON.stringify(analysisResult, null, 2) }}</pre>
        </template>
      </template>
    </main>
  </div>
</template>

<style scoped>
.shell {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.sidebar {
  width: 280px;
  flex-shrink: 0;
  border-right: 1px solid var(--border);
  padding: 24px;
  box-sizing: border-box;
}

.sidebar-title {
  margin: 0 0 16px;
  font-size: 20px;
}

.viewer {
  flex: 1;
  padding: 24px;
  min-width: 0;
}

.viewer-title {
  margin: 0 0 16px;
  font-size: 20px;
}

.muted {
  color: var(--text-secondary);
}

.meta {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--text-secondary);
}

.sep {
  margin: 0 8px;
}

.state-ok {
  color: var(--success);
}

.state-err {
  color: var(--error);
}

.section-title {
  margin: 24px 0 12px;
  font-size: 16px;
}

.preview {
  margin: 0;
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.detail-preview {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>