<script setup>
import { ref, onMounted, watch } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  analysisResult: Object  // LLM analysis JSON with outliers data
})

const svgContainer = ref(null)
const errorMsg = ref('')

function extractNumericalData(result) {
  if (!result) {
    console.warn('No result provided')
    return null
  }

  if (!result?.rows || result.rows.length === 0) {
    console.warn('No rows found')
    return null
  }

  // Get column analysis to identify numerical columns
  const numericalCols = (result.column_analysis || [])
    .filter(col => col.data_type === 'float' || col.data_type === 'integer')
    .map(col => col.column_name)

  console.log('Found numerical columns:', numericalCols)

  if (numericalCols.length === 0) {
    console.warn('No numerical columns detected. Column types:', 
      result.column_analysis?.map(c => c.data_type))
    return null
  }

  // Convert rows to numerical values
  const data = result.rows.map((row, idx) => {
    const dataPoint = { __rowIndex: idx }
    numericalCols.forEach(col => {
      dataPoint[col] = parseFloat(row[col]) || 0
    })
    return dataPoint
  })

  return {
    columns: numericalCols,
    data,
    outlierIndices: result.outliers?.detected?.map(o => o.row_index) || []
  }
}

function renderParallelCoordinates() {
  const parsed = extractNumericalData(props.analysisResult)

  if (!parsed) {
    errorMsg.value = 'No numerical columns found for visualization'
    return
  }

  const { columns, data, outlierIndices } = parsed

  // Clear previous SVG
  d3.select(svgContainer.value).selectAll('*').remove()
  errorMsg.value = ''

  // Dimensions
  const margin = { top: 20, right: 20, bottom: 30, left: 60 }
  const width = 800 - margin.left - margin.right
  const height = 500 - margin.top - margin.bottom

  // Create SVG
  const svg = d3
    .select(svgContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Create scale for each dimension
  const scales = {}
  columns.forEach(col => {
    const values = data.map(d => d[col])
    scales[col] = d3
      .scaleLinear()
      .domain([Math.min(...values), Math.max(...values)])
      .range([height, 0])
  })

  // X scale for axes positions
  const xScale = d3.scalePoint().domain(columns).range([0, width])

  // Draw axes
  columns.forEach((col, i) => {
    const xPos = xScale(col)
    
    // Axis line
    svg
      .append('line')
      .attr('x1', xPos)
      .attr('y1', 0)
      .attr('x2', xPos)
      .attr('y2', height)
      .attr('stroke', '#ddd')
      .attr('stroke-width', 1)

    // Axis label
    svg
      .append('text')
      .attr('x', xPos)
      .attr('y', height + 20)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#333')
      .text(col)
  })

  // Draw polylines for each data row
  data.forEach(row => {
    const isOutlier = outlierIndices.includes(row.__rowIndex)
    const points = columns.map((col, i) => [
      xScale(col),
      scales[col](row[col])
    ])

    const lineGenerator = d3.line()

    svg
      .append('path')
      .attr('d', lineGenerator(points))
      .attr('stroke', isOutlier ? '#e74c3c' : '#3498db')
      .attr('stroke-width', isOutlier ? 2.5 : 1.5)
      .attr('fill', 'none')
      .attr('opacity', isOutlier ? 0.9 : 0.4)
  })

  // Legend
  svg
    .append('circle')
    .attr('cx', width - 100)
    .attr('cy', -15)
    .attr('r', 4)
    .attr('fill', '#3498db')

  svg
    .append('text')
    .attr('x', width - 85)
    .attr('y', -10)
    .attr('font-size', '12px')
    .attr('fill', '#666')
    .text('Normal')

  svg
    .append('circle')
    .attr('cx', width - 100)
    .attr('cy', 0)
    .attr('r', 4)
    .attr('fill', '#e74c3c')

  svg
    .append('text')
    .attr('x', width - 85)
    .attr('y', 5)
    .attr('font-size', '12px')
    .attr('fill', '#666')
    .text('Outlier')
}

onMounted(() => {
  if (props.analysisResult) {
    renderParallelCoordinates()
  }
})

watch(() => props.analysisResult, () => {
  if (svgContainer.value) {
    renderParallelCoordinates()
  }
})
</script>

<template>
  <div class="parallel-coords">
    <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
    <p v-else-if="!props.analysisResult" class="no-data-message">(No analysis yet)</p>
    <div v-else ref="svgContainer" class="svg-container"></div>
  </div>
</template>

<style scoped>
.parallel-coords {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.svg-container {
  width: 100%;
  max-width: 900px;
  overflow-x: auto;
}

.error-message {
  color: var(--error);
 

.no-data-message {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
} font-size: 14px;
}
</style>
