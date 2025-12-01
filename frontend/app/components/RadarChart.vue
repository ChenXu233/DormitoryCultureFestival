<template>
  <div class="radar-chart" :style="maxWidth ? { maxWidth: maxWidth } : {}">
    <canvas ref="canvas"/>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{ 
  radarData?: { dimensions: string[]; scores: number[]; max_score: number },
  multiRadarData?: { dimensions: string[]; datasets: { label: string; scores: number[]; color?: string }[]; max_score: number },
  dimensionEmojis?: Record<string, string>,
  maxWidth?: string
}>()
const canvas = ref<HTMLCanvasElement | null>(null)
let chart: any = null

onMounted(async () => {
  if (!import.meta.client) return
  // dynamically import Chart.js only on client
  const ChartModule = await import('chart.js/auto')
  const Chart = (ChartModule as any).default || (ChartModule as any).Chart || ChartModule

  if (!canvas.value) return

  const dimensions = props.multiRadarData?.dimensions || props.radarData?.dimensions || []
  const maxScore = props.multiRadarData?.max_score || props.radarData?.max_score || 100

  const labels = dimensions.map(dim => {
    const emoji = props.dimensionEmojis?.[dim]
    return emoji ? `${emoji} ${dim}` : dim
  })

  let datasets: any[] = []

  if (props.multiRadarData) {
    datasets = props.multiRadarData.datasets.map(ds => ({
      label: ds.label,
      data: ds.scores,
      backgroundColor: ds.color ? `${ds.color}33` : 'rgba(34,197,94,0.2)', // 0.2 opacity (hex 33)
      borderColor: ds.color || 'rgba(34,197,94,1)',
      pointBackgroundColor: ds.color || 'rgba(34,197,94,1)',
    }))
  } else if (props.radarData) {
    datasets = [{
      label: '特质得分',
      data: props.radarData.scores,
      backgroundColor: 'rgba(34,197,94,0.2)',
      borderColor: 'rgba(34,197,94,1)',
      pointBackgroundColor: 'rgba(34,197,94,1)',
    }]
  }

  chart = new Chart(canvas.value, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        r: {
          suggestedMin: 0,
          suggestedMax: maxScore,
          ticks: {
            stepSize: 20,
          },
          pointLabels: {
            font: {
              size: 16, // Increased font size
            },
          },
        },
      },
      plugins: {
        legend: {
          display: !!props.multiRadarData,
          labels: {
            font: {
              size: 14 // Increased legend font size
            }
          }
        },
      },
    },
  })
})

// Update chart when data changes
watch(
  () => [props.radarData, props.multiRadarData, props.dimensionEmojis],
  ([nvRadarData, nvMultiRadarData, nvEmojis]) => {
    if (!chart) return
    
    const radarData = nvRadarData as typeof props.radarData
    const multiRadarData = nvMultiRadarData as typeof props.multiRadarData
    const emojis = nvEmojis as Record<string, string> | undefined
    
    const dimensions = multiRadarData?.dimensions || radarData?.dimensions || []
    const maxScore = multiRadarData?.max_score || radarData?.max_score || 100

    const labels = dimensions.map(dim => {
      const emoji = emojis?.[dim]
      return emoji ? `${emoji} ${dim}` : dim
    })
    
    chart.data.labels = labels

    if (multiRadarData) {
      chart.data.datasets = multiRadarData.datasets.map(ds => ({
        label: ds.label,
        data: ds.scores,
        backgroundColor: ds.color ? `${ds.color}33` : 'rgba(34,197,94,0.2)',
        borderColor: ds.color || 'rgba(34,197,94,1)',
        pointBackgroundColor: ds.color || 'rgba(34,197,94,1)',
      }))
      chart.options.plugins.legend.display = true
    } else if (radarData) {
      chart.data.datasets = [{
        label: '特质得分',
        data: radarData.scores,
        backgroundColor: 'rgba(34,197,94,0.2)',
        borderColor: 'rgba(34,197,94,1)',
        pointBackgroundColor: 'rgba(34,197,94,1)',
      }]
      chart.options.plugins.legend.display = false
    }

    if (chart.options && chart.options.scales && chart.options.scales.r) {
      chart.options.scales.r.suggestedMax = maxScore
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
  width: 60%;
  max-width: 800px;
  margin: 0 auto;
}
</style>