<template>
  <div class="radar-chart" :style="wrapperStyle">
    <canvas ref="canvas" :style="canvasStyle" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'

const props = defineProps<{ 
  radarData?: { dimensions: string[]; scores: number[]; max_score: number },
  multiRadarData?: { dimensions: string[]; datasets: { label: string; scores: number[]; color?: string }[]; max_score: number },
  dimensionEmojis?: Record<string, string>,
  // optional layout props
  width?: string | number,
  height?: string | number,
  lenendbignum1?: number ,
  lenendbignum2?: number ,
  maintainAspectRatio?: boolean,
  // allow caller to force the wrapper to use full width (keeps default behavior unchanged)
  fullWidth?: boolean,
}>()
const canvas = ref<HTMLCanvasElement | null>(null)
let chart: any = null

// compute CSS size for canvas; Chart.js will use these when maintainAspectRatio is false
const canvasStyle = computed(() => {
  const width = props.width ?? '100%'
  const height = props.height ?? '400px'
  const fmt = (v: string | number) => (typeof v === 'number' ? `${v}px` : v)
  return {
    width: fmt(width),
    height: fmt(height),
    display: 'block',
  }
})

// compute wrapper style so callers can override the default 50% width
const wrapperStyle = computed(() => {
  const fmt = (v: string | number) => (typeof v === 'number' ? `${v}px` : v)
  // priority: explicit width prop -> fullWidth flag -> default 50%
  const w = props.width ?? (props.fullWidth ? '100%' : '50%')
  return {
    width: fmt(w),
    maxWidth: '100000px',
    margin: '0 auto',
  }
})

const wrapLabel = (label: string, maxLen = 8) => {
  if (!label) return label
  // preserve emoji + space if present
  // split into chunks for better display around the radar
  const parts: string[] = []
  // keep existing newlines
  if (label.includes('\n')) return label
  for (let i = 0; i < label.length; i += maxLen) {
    parts.push(label.slice(i, i + maxLen))
  }
  return parts.join('\n')
}

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
    const raw = emoji ? `${emoji} ${dim}` : dim
    return wrapLabel(raw, 8)
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
      // allow non-square charts by default; can be overridden with prop
      maintainAspectRatio: props.maintainAspectRatio ?? false,
        layout: {
          padding: {
            top: 10,
            bottom: 10,
            left: 10,
            right: 10,
          }
        },
      scales: {
        r: {
          suggestedMin: 0,
          suggestedMax: maxScore,
          ticks: {
            stepSize: 20,
          },
            pointLabels: {
              font: {
                size: props.lenendbignum1 ?? 12, // Increased font size
              },
              padding: 8,
            },
        },
      },
      plugins: {
        legend: {
          display: props.multiRadarData ? true : false,
          labels: {
            font: {
              size: props.lenendbignum2 ?? 12, // Increased legend font size
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
      const raw = emoji ? `${emoji} ${dim}` : dim
      return wrapLabel(raw, 8)
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
      // ensure point label font size and padding are kept in sync on updates
      if (!chart.options.scales.r.pointLabels) chart.options.scales.r.pointLabels = {}
      chart.options.scales.r.pointLabels.font = chart.options.scales.r.pointLabels.font || {}
      chart.options.scales.r.pointLabels.font.size = props.lenendbignum1 ?? chart.options.scales.r.pointLabels.font.size
      chart.options.scales.r.pointLabels.padding = chart.options.scales.r.pointLabels.padding ?? 8
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
  max-width:100000px;
  margin: 0 auto;
}
</style>