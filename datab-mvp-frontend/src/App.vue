<script setup>
import { ref } from 'vue'
import UploadComponent from './components/UploadComponent.vue'
import AnalyzeComponent from './components/AnalyzeComponent.vue'
import CsvPreviewComponent from './components/CsvPreviewComponent.vue'
import VisualizationToggleComponent from './components/VisualizationToggleComponent.vue'

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
      <template v-if="lastResult">
        <p class="meta">
          <strong>{{ lastResult.filename }}</strong>
          <span class="sep">·</span>
          <span :class="lastResult.ok ? 'state-ok' : 'state-err'">
            {{ lastResult.ok ? 'OK' : 'Error' }}
          </span>
        </p>
      </template>
      <div class="columns">
        <div class="column">
          <CsvPreviewComponent :csv-text="lastResult?.csvText" :preview-data="lastResult?.data?.preview" />
        </div>
        <div class="column">
          <VisualizationToggleComponent :analysis-result="analysisResult" />
        </div>
      </div>
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
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.viewer-title {
  margin: 0 0 16px;
  font-size: 20px;
  flex-shrink: 0;
}

.muted {
  color: var(--text-secondary);
}

.meta {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--text-secondary);
  flex-shrink: 0;
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

.columns {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0;
}

.column {
  flex: 1;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
</style>