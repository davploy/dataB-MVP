<script setup>
const props = defineProps({
  csvText: String
})
</script>

<template>
  <div class="csv-preview">
    <h3 class="section-title">CSV (from file)</h3>
    <pre class="preview">{{ csvText || '(No CSV uploaded yet)' }}</pre>
  </div>
</template>

<style scoped>
.csv-preview {
  display: flex;
  flex-direction: column;
  height: 900px;
  min-height: 0;
}

.section-title {
  margin: 0 0 12px;
  font-size: 16px;
  flex-shrink: 0;
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
