<template>
  <div class="radar-chart">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{ radarData: { dimensions: string[]; scores: number[]; max_score: number } }>()
const canvas = ref<HTMLCanvasElement | null>(null)
let chart: any = null

// Helper function to create the chart
const createChart = async () => {
  if (!process.client || !canvas.value) return
  
  try {
    // Import chart.js/auto which registers all components automatically
    const { Chart } = await import('chart.js/auto')
    
    // Create the chart with proper configuration
    chart = new Chart(canvas.value, {
      type: 'radar',
      data: {
        labels: props.radarData?.dimensions || [],
        datasets: [
          {
            label: '特质得分',
            data: props.radarData?.scores || [],
            backgroundColor: 'rgba(34,197,94,0.2)',
            borderColor: 'rgba(34,197,94,1)',
            pointBackgroundColor: 'rgba(34,197,94,1)',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          r: {
            suggestedMin: 0,
            suggestedMax: props.radarData?.max_score ?? 100,
            ticks: {
              stepSize: 20,
            },
            pointLabels: {
              font: {
                size: 12,
              },
            },
          },
        },
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    })
  } catch (error) {
    console.error('Error initializing chart:', error)
  }
}

// Initialize the chart on mount
onMounted(() => {
  createChart()
})

// Update chart when data changes
watch(
  () => props.radarData,
  (nv) => {
    if (!chart || !nv) return
    chart.data.labels = nv.dimensions
    chart.data.datasets[0].data = nv.scores
    if (chart.options && chart.options.scales && chart.options.scales.r) {
      chart.options.scales.r.suggestedMax = nv.max_score
    }
    chart.update()
  },
  { immediate: true, deep: true }
)

// Clean up chart instance before unmount
onBeforeUnmount(() => {
  if (chart) {
    chart.destroy()
    chart = null
  }
})
</script>

<style scoped>
.radar-chart {
  max-width: 520px;
  margin: 0 auto;
}
</style>