<template>
  <div class="relative w-full max-w-4xl mx-auto">
    <!-- 词云容器 -->
    <div 
      ref="wordcloudContainer" 
      class="w-full aspect-square bg-gray-50 rounded-lg overflow-hidden flex items-center justify-center"
      :style="{ backgroundColor: theme.bgColor }"
    >
      <!-- 词云画布 -->
      <canvas ref="canvasRef" class="max-w-full max-h-full"></canvas>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/80">
      <div class="text-center">
        <div class="mb-2 w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p>生成词云中...</p>
      </div>
    </div>
    
    <!-- 空状态提示 -->
    <div v-if="!loading && words.length === 0" class="absolute inset-0 flex items-center justify-center">
      <div class="text-center text-gray-500">
        <div class="mb-2 text-4xl">☁️</div>
        <p>暂无词云数据</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

// 只在客户端导入wordcloud库
let WordCloud: any = null
if (process.client) {
  import('wordcloud').then(module => {
    WordCloud = module.default || module
  })
}

// Props
interface Props {
  words: Array<{ text: string; value: number }>
  theme?: {
    bgColor?: string
    colors?: string[]
  }
  width?: number
  height?: number
}

const props = withDefaults(defineProps<Props>(), {
  words: () => [],
  theme: () => ({
    bgColor: '#f9fafb',
    colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
  }),
  width: 600,
  height: 600
})

// Emits
const emit = defineEmits<{
  (e: 'rendered'): void
}>()

// Refs
const wordcloudContainer = ref<HTMLElement>()
const canvasRef = ref<HTMLCanvasElement>()
const loading = ref(false)
const isClient = ref(false)

// 生成词云的方法
const generateWordCloud = async () => {
  if (!isClient.value || !wordcloudContainer.value || props.words.length === 0 || !WordCloud) return
  
  loading.value = true
  
  try {
    await nextTick()
    
    // 获取容器尺寸
    const containerWidth = wordcloudContainer.value.clientWidth
    const containerHeight = wordcloudContainer.value.clientHeight
    
    // 设置canvas尺寸
    if (canvasRef.value) {
      canvasRef.value.width = containerWidth
      canvasRef.value.height = containerHeight
    }
    
    // 确保数据格式正确
    const wordList = props.words.map(item => [item.text, item.value])
    
    const options = {
      list: wordList,
      gridSize: Math.round(16 * containerWidth / 1024),
      weightFactor: (size: number) => {
        // 根据词频调整词的大小
        return Math.pow(size, 0.8) * containerWidth / 1024 * 15
      },
      fontFamily: '"Segoe UI", "Microsoft YaHei", sans-serif',
      color: () => props.theme.colors[Math.floor(Math.random() * props.theme.colors.length)],
      rotateRatio: 0.5,
      rotationSteps: 2,
      backgroundColor: props.theme.bgColor,
      drawOutOfBound: false,
      shrinkToFit: true,
      shape: 'circle',
      ellipticity: 0.65,
      clearCanvas: true,
      minSize: 10,
      minRotation: -45,
      maxRotation: 45
    }
    
    // 使用canvas元素生成词云
    if (canvasRef.value) {
      WordCloud(canvasRef.value, options)
    } else {
      // 备用方案：使用容器元素
      WordCloud(wordcloudContainer.value, options)
    }
    
    emit('rendered')
  } catch (error) {
    console.error('词云生成失败:', error)
    // 如果词云生成失败，显示错误信息
    console.log('词云数据:', props.words)
    console.log('词云选项:', options)
  } finally {
    loading.value = false
  }
}

// 监听词云数据变化
watch(() => props.words, () => {
  generateWordCloud()
}, { deep: true })

// 监听主题变化
watch(() => props.theme, () => {
  generateWordCloud()
}, { deep: true })

// 组件挂载时生成词云
onMounted(() => {
  isClient.value = true
  // 如果WordCloud库已经加载，立即生成词云
  if (WordCloud) {
    generateWordCloud()
  } else {
    // 等待WordCloud库加载完成
    import('wordcloud').then(module => {
      WordCloud = module.default || module
      generateWordCloud()
    })
  }
})

// 窗口大小变化时重新生成词云
const handleResize = () => {
  generateWordCloud()
}

onMounted(() => {
  if (process.client) {
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener('resize', handleResize)
  }
})

// 导出方法供父组件调用
defineExpose({
  generateWordCloud
})
</script>

<style scoped>
/* 词云容器样式 */
:deep(canvas) {
  max-width: 100% !important;
  height: auto !important;
}
</style>