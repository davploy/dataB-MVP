<script setup>
const props = defineProps({
  csvText: String,
  previewData: Object  // {headers: [], rows: [], row_count, column_count}
})
</script>

<template>
  <div class="csv-preview">
    <h3 class="section-title">CSV (from file)</h3>
    
    <!-- Table view if structured data is available -->
    <div v-if="previewData?.headers && previewData?.rows" class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="header in previewData.headers" :key="header" class="table-header">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIdx) in previewData.rows" :key="rowIdx" class="table-row">
            <td v-for="header in previewData.headers" :key="`${rowIdx}-${header}`" class="table-cell">
              {{ row[header] || '—' }}
            </td>
          </tr>
        </tbody>
      </table>
      <p class="table-footer">
        {{ previewData.row_count }} rows × {{ previewData.column_count }} columns
      </p>
    </div>
    
    <!-- Fallback to raw CSV text if structured data unavailable -->
    <pre v-else class="preview">{{ csvText || '(No CSV uploaded yet)' }}</pre>
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

.table-container {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow-y: auto;
  background: var(--bg-secondary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.table-header {
  background: var(--bg-tertiary);
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 10;
}

.table-row:hover {
  background: var(--bg-hover);
}

.table-row:nth-child(even) {
  background: rgba(0, 0, 0, 0.02);
}

.table-cell {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  word-break: break-word;
  max-width: 300px;
}

.table-footer {
  margin: 0;
  padding: 8px 12px;
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  border-top: 1px solid var(--border);
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
