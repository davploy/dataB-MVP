<script setup>
import { ref } from 'vue'
import UploadComponent from './components/UploadComponent.vue'

const lastResult = ref(null)

function onUploadResult(payload) {
  lastResult.value = payload
}
</script>

<template>
  <div class="shell">
    <aside class="sidebar" aria-label="Upload">
      <h2 class="sidebar-title">Upload</h2>
      <UploadComponent @upload-result="onUploadResult" />
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
        <!-- NEW BOX: Analysis JSON Results -->
        <template v-if="lastResult.analysis">
          <h3 class="section-title">Analysis Result (from LLM)</h3>
          <pre class="preview">{{ JSON.stringify(lastResult.analysis, null, 2) }}</pre>
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
  margin: 0;
  color: var(--text);
}

.meta {
  margin: 0 0 16px;
  color: var(--text-h);
}

.sep {
  margin: 0 6px;
  color: var(--text);
}

.state-ok {
  color: var(--accent);
}

.state-err {
  color: var(--text-h);
}

.section-title {
  margin: 16px 0 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}

.section-title:first-of-type {
  margin-top: 0;
}

.preview {
  margin: 0;
  padding: 16px;
  border-radius: 6px;
  font-family: var(--mono);
  font-size: 14px;
  line-height: 1.45;
  overflow: auto;
  max-height: min(70vh, 640px);
  color: var(--text-h);
  background: var(--code-bg);
  border: 1px solid var(--border);
}

.detail-preview {
  max-height: min(30vh, 240px);
  font-size: 13px;
}
</style>
