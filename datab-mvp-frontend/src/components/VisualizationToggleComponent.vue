<script setup>
import { ref } from 'vue'
import ParallelCoordinatesComponent from './ParallelCoordinatesComponent.vue'
import ResultJSONPreviewComponent from './ResultJSONPreviewComponent.vue'

const props = defineProps({
  analysisResult: Object
})

const activeTab = ref('visualization')
</script>

<template>
  <div class="visualization-toggle">
    <div class="tab-buttons">
      <button
        :class="['tab-btn', { active: activeTab === 'json' }]"
        @click="activeTab = 'json'"
      >
        JSON
      </button>
      <button
        :class="['tab-btn', { active: activeTab === 'visualization' }]"
        @click="activeTab = 'visualization'"
      >
        Visualization
      </button>

    </div>

    <div class="tab-content">
      <div v-show="activeTab === 'visualization'" class="tab-pane">
        <ParallelCoordinatesComponent :analysis-result="analysisResult" />
      </div>
      <div v-show="activeTab === 'json'" class="tab-pane">
        <ResultJSONPreviewComponent :analysis-result="analysisResult" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.visualization-toggle {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.tab-buttons {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border);
}

.tab-btn {
  padding: 8px 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-secondary);
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tab-btn.active {
  color: var(--text-primary);
  border-bottom-color: var(--accent);
  font-weight: 500;
}

.tab-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.tab-pane {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
</style>
