<script setup>
const props = defineProps({
  analysisResult: Object
})
</script>

<template>
  <div class="result-preview">
    <pre class="preview">{{ analysisResult ? JSON.stringify(analysisResult, null, 2) : '(No analysis yet)' }}</pre>
  </div>
</template>

<style scoped>
.result-preview {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.preview {
  margin: 0;
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow-y: scroll;
  font-size: 13px;
  line-height: 1.5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  flex: 1;
  min-height: 0;
  max-height: 100%;
}
</style>
