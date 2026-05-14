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
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
  overflow-y: auto;
  font-size: 13px;
  line-height: 1.5;
  flex: 1;
  min-height: 0;
}
</style>
