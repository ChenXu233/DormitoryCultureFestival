<template>
  <div class="relative w-full max-w-4xl mx-auto">
    <!-- 词云容器 -->
    <div 
      ref="wordcloudContainer" 
      class="w-full aspect-square bg-gray-50 rounded-lg overflow-hidden flex items-center justify-center"
      :style="{ backgroundColor: theme.bgColor }"
    >
      <!-- 词云画布 -->
      <canvas ref="canvasRef" class="max-w-full max-h-full"/>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/80">
      <div class="text-center">
        <div class="mb-2 w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"/>
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
if (import.meta.client) {
  import('wordcloud').then(module => {
    WordCloud = module.default || module
  })
}

// Props
interface Props {
  words?: Array<{ text: string; value: number }>
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
      
      // 首先按词频降序排序，确保大词先被放置，避免大词占据过多空间
      const sortedWords = [...props.words].sort((a, b) => b.value - a.value)
      
      // 数据归一化处理
      const values = sortedWords.map(item => item.value)
      const maxValue = Math.max(...values)
      const minValue = Math.min(...values)
      const valueRange = maxValue - minValue || 1 // 避免除零错误
      
      // 确保数据格式正确并进行归一化
      const wordList = sortedWords.map(item => {
        // 将值归一化到1-100的范围，保持相对关系
        const normalizedValue = 1 + ((item.value - minValue) / valueRange) * 99
        return [item.text, normalizedValue]
      })

      const colors = props.theme.colors || ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
      
      const options = {
        list: wordList,
        gridSize: Math.round(16 * containerWidth / 1024),
        weightFactor: (size: number) => {
          return Math.pow(size, 0.7) * containerWidth / 1024 * 30
        },
        fontFamily: '"Microsoft YaHei", "Segoe UI", sans-serif', // 优先使用中文字体
        color: () => colors[Math.floor(Math.random() * colors.length)],
        rotateRatio: 0.3, // 减少旋转比例，提高中文可读性
        backgroundColor: props.theme.bgColor,
        drawOutOfBound: false,
        shrinkToFit: true,
        ellipticity: 0.65,
        clearCanvas: true,
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
    // 错误处理，避免引用作用域外的变量
    console.log('词云数据:', props.words)
    console.log('容器尺寸:', wordcloudContainer.value?.clientWidth, wordcloudContainer.value?.clientHeight)
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

// 窗口大小变化时重新生成词云
const handleResize = () => {
  generateWordCloud()
}

// 组件挂载时的初始化（合并为单个onMounted）
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
  
  // 添加窗口大小变化监听
  if (import.meta.client) {
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  if (import.meta.client) {
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