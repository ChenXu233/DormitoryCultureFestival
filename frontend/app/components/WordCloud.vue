<template>
  <div class="relative w-full">
    <!-- 词云容器 -->
    <div 
      ref="wordcloudContainer" 
      class="w-full aspect-square bg-gray-50 rounded-lg overflow-hidden flex items-center justify-center"
      :style="{ backgroundColor: theme.bgColor }"
    >
        <!-- 词云画布（ECharts 渲染） -->
        <div ref="wordcloudContainerInner" class="w-full h-full" />
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

// Props
interface Props {
  words?: Array<{ text: string; value: number }>
  theme?: {
    bgColor?: string
    colors?: string[]
  }
  // 可选遮罩图片 URL，用于把词云裁剪成指定形状（例如云朵）
  maskImage?: string
  // 遮罩缩放因子，默认 >1 可放大遮罩以填充更多区域
  maskScale?: number
  // 是否允许重复渲染词语以填充画面
  repeat?: boolean
  // 重复因子（每个词渲染的次数，>=1）
  repeatFactor?: number
  // 最大渲染词数（在应用重复之前截断原始词表）
  maxWords?: number
  // 是否让词云触碰容器边缘（允许绘制出界并使用更密集的布局）
  touchEdges?: boolean
  // 全局缩放因子，用于放大/缩小词云整体尺寸
  overallScale?: number
}

const props = withDefaults(defineProps<Props>(), {
  words: () => [],
  theme: () => ({
    bgColor: '#f9fafb',
    colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
  }),
  maskImage: undefined,
  maskScale: 1,
  touchEdges: true,
  overallScale: 10,
  repeat: true,
  repeatFactor: 2,
  maxWords: 400
})

// Emits
const emit = defineEmits<{
  (e: 'rendered'): void
}>()

// Refs
const wordcloudContainer = ref<HTMLElement | null>(null)
const wordcloudContainerInner = ref<HTMLElement | null>(null)
const loading = ref(false)
const isClient = ref(false)

let echarts: any = null
let chart: any = null
let maskImgElement: HTMLImageElement | null = null
let lastMaskUrl: string | null = null

const loadMaskImage = (url: string) => {
  return new Promise<HTMLImageElement>((resolve, reject) => {
    try {
      const img = new Image()
      img.crossOrigin = 'anonymous'
      img.onload = () => resolve(img)
      img.onerror = () => reject(new Error('加载遮罩图片失败: ' + url))
      img.src = url
    } catch (e) {
      reject(e)
    }
  })
}

// 用来保存原始 getContext，以便卸载时恢复
let originalGetContext: any = null

const updateChart = async () => {
  if (!isClient.value || !chart) return

  loading.value = true
  try {
    await nextTick()

    // 按 value 降序排序，确保大词先被布局，降低冲突概率
    const sorted = [...(props.words || [])].sort((a, b) => b.value - a.value)

    // 可选截断原始词表以控制渲染量
    const maxWords = typeof props.maxWords === 'number' ? props.maxWords : sorted.length
    const sliced = sorted.slice(0, maxWords)

    // 构建数据：先对词频进行归一化并做幂次压缩，限制最大词语权重，避免个别词过大导致画面稀疏
    const repeatFactor = Math.max(1, Math.round(props.repeatFactor || 1))
    const data: Array<{ name: string; value: number }> = []

    // 归一化原始值到 0-1，然后用幂次小于1进行压缩（例如 0.6），减小极差
    const rawValues = sliced.map(s => s.value)
    const rawMax = Math.max(...rawValues, 1)
    const rawMin = Math.min(...rawValues, 0)
    const rawRange = rawMax - rawMin || 1
    const compressExponent = 0.6

    const overallScale = typeof props.overallScale === 'number' ? props.overallScale : 1

    // Strategy:
    // - Keep the top N (5) words single (no repeats) so they don't dominate.
    // - For other words, repeat smaller words much more aggressively (repeatCount proportional to (1 - normalized)^power)
    // - Do NOT cap total items here; let the layout try to place many small words to fill gaps.
    const topN = 5
    // 极致优化：降低总数上限，移除复杂数学运算
    const maxTotalItems = 50 // 降低上限是提升 ECharts 布局速度的最直接手段

    // 缓存变量避免重复访问
    const hasRepeat = repeatFactor > 1
    const limitRepeat =10 // 限制最大重复次数

    for (let idx = 0; idx < sliced.length; idx++) {
      if (data.length >= maxTotalItems) break

      const item = sliced[idx]
      const normalized = (item.value - rawMin) / rawRange

      // Top 5: 保持高质量渲染
      if (idx < 5) {
        const compressed = Math.sqrt(normalized)
        const baseValue = Math.max(1, Math.round((40 + compressed * 160) * overallScale * 0.85))
        data.push({ name: item.text, value: baseValue })
        continue
      }

      // 普通词汇：使用线性计算代替开方，极大提升 JS 执行效率
      // 基础大小范围 12-92
      const baseValueSmall = Math.max(1, Math.round((12 + normalized * 80) * overallScale))
      data.push({ name: item.text, value: baseValueSmall })

      // 简化重复逻辑：仅对中高频词进行少量重复，且直接计算
      if (hasRepeat && normalized > 0.15 && data.length < maxTotalItems) {
        // 仅当前 40% 的词允许重复，且最多重复 limitRepeat 次
        const count = normalized > 0.4 ? limitRepeat : 1
        
        for (let r = 1; r <= count; r++) {
           // 快速衰减
           const val = (baseValueSmall * (1 - r * 0.25)) | 0 // 使用位运算取整
           if (val < 1) break // 过滤过小的词，减少布局负担
           
           data.push({ name: item.text, value: val })
           if (data.length >= maxTotalItems) break
        }
      }
    }

    const colors = props.theme?.colors || ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

    const containerWidth = wordcloudContainer.value?.clientWidth || 380
    const containerHeight = wordcloudContainer.value?.clientHeight || 380

    // 根据是否使用遮罩（maskImage）和是否希望贴边（touchEdges）来调整布局参数：
    // 使用遮罩时放大词语并更密集一些以填满形状；若希望贴边则进一步密集
    const usingMask = Boolean(props.maskImage && maskImgElement)
    const touchEdges = typeof props.touchEdges === 'boolean' ? props.touchEdges : true
    // 更小的 baseGrid 和更激进的缩放系数以增加密度
    const baseGrid = usingMask ? Math.round((containerWidth / 1024) * 6) : Math.round((containerWidth / 1024) * 10)
    const gridSizeVar = Math.max(1, Math.floor(baseGrid * (touchEdges ? 0.5 : 0.8)))

    // 使用容器短边来更可靠地计算词语上限，使词在形状内显得更大
    const shortSide = Math.min(containerWidth, containerHeight)
    const sizeUpperBase = usingMask
      ? Math.max(32, Math.round(shortSide / 8))
      : Math.max(28, Math.round(containerWidth / 12))

    // 为了画面更饱满，略微提高最小字号
    const sizeLowerBase = usingMask ? 16 : 14

    // 应用 overallScale 到字号范围
    const sizeUpper = Math.max(8, Math.round(sizeUpperBase * overallScale))
    const sizeLower = Math.max(6, Math.round(sizeLowerBase * overallScale))

    // 为了让画面更“满”且词稍大：使用上述计算值
    const option = {
      tooltip: { show: true },
      series: [
        {
          type: 'wordCloud',
          shape: 'circle',
          // 根据容器和是否使用遮罩/贴边动态计算 gridSize 和 sizeRange
          gridSize: gridSizeVar,
          sizeRange: [sizeLower, sizeUpper],
          // 禁用旋转，水平排布更利于中文显示
          rotationRange: [-90, 90],
          rotationStep: 90,
          // 当词太挤时允许根据需要缩小文本以适配形状
          shrinkToFit: true,
          // 少量随机旋转可以帮助小词塞入缝隙（全局控制，低比例）
          rotateRatio: 0.08,
          // 保持圆形分布
          ellipticity: 1,
          // 中文字体
          textStyle: {
            fontFamily: '"Microsoft YaHei", "Segoe UI", sans-serif',
            color: (params: any) => colors[Math.floor(Math.random() * colors.length)]
          },
          emphasis: {
            focus: 'self',
            textStyle: {
              textShadowBlur: 10,
              textShadowColor: '#333'
            }
          },
          data
        }
      ]
    }
    if (props.maskImage) {
      try {
        if (props.maskImage !== lastMaskUrl) {
          maskImgElement = await loadMaskImage(props.maskImage)
          lastMaskUrl = props.maskImage
        }
        if (maskImgElement) {
          // 将遮罩图片按容器尺寸绘制到临时 canvas 上，确保遮罩填满图表区域
          try {
            const maskCanvas = document.createElement('canvas')
            maskCanvas.width = containerWidth
            maskCanvas.height = containerHeight
            const ctx = maskCanvas.getContext('2d')
            if (ctx) {
              const imgW = (maskImgElement.naturalWidth || (maskImgElement as any).width || 0)
              const imgH = (maskImgElement.naturalHeight || (maskImgElement as any).height || 0)
              // 如果图片尺寸有效，则按 cover 模式拉伸填满画布并居中
              if (imgW > 0 && imgH > 0) {
                const baseScale = Math.max(containerWidth / imgW, containerHeight / imgH)
                const maskScale = typeof props.maskScale === 'number' ? props.maskScale : 1
                const scale = baseScale * maskScale
                const drawW = imgW * scale
                const drawH = imgH * scale
                const dx = Math.round((containerWidth - drawW) / 2)
                const dy = Math.round((containerHeight - drawH) / 2)
                ctx.clearRect(0, 0, maskCanvas.width, maskCanvas.height)
                ctx.drawImage(maskImgElement, dx, dy, drawW, drawH)
              } else {
                // 兜底：直接绘制图片（浏览器会按默认尺寸处理）
                ctx.drawImage(maskImgElement, 0, 0)
              }
              option.series[0].maskImage = maskCanvas
            }
          } catch (drawErr) {
            // 如果绘制失败，回退为直接使用 image 元素
            console.warn('绘制遮罩到 canvas 失败，回退使用原始图片：', drawErr)
            option.series[0].maskImage = maskImgElement
            option.series[0].drawOutOfBound = touchEdges
          }
        }
      } catch (imgErr) {
        console.warn('遮罩图片加载失败，回退到默认形状：', imgErr)
        maskImgElement = null
        lastMaskUrl = null
      }
    }

    chart.setOption(option, { notMerge: true })
    emit('rendered')
  } catch (e) {
    console.error('ECharts 词云渲染失败:', e)
  } finally {
    loading.value = false
  }
}

let debounceTimer: ReturnType<typeof setTimeout> | null = null

const debouncedUpdateChart = () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    updateChart()
  }, 100)
}

// 监听数据和主题变化
watch(() => props.words, debouncedUpdateChart, { deep: true })
watch(() => props.theme, debouncedUpdateChart, { deep: true })
watch(() => props.maskImage, debouncedUpdateChart)

// 窗口大小变化时调整图表
const handleResize = () => {
  if (chart && isClient.value) chart.resize()
}

onMounted(async () => {
  isClient.value = true

  if (!import.meta.client) return
  // 在加载 ECharts 前，临时覆盖 canvas.getContext，
  // 为所有后续请求 2d 上下文的调用设置 willReadFrequently: true，
  // 以避免多次 getImageData 导致的性能警告（并提升大量读回操作的性能）。
  try {
    if (!originalGetContext) {
      originalGetContext = (HTMLCanvasElement.prototype as any).getContext
      ;(HTMLCanvasElement.prototype as any).getContext = function(type: string, attrs?: any) {
        if (type === '2d') {
          // 如果调用方没有显式传入 willReadFrequently，则合并并设置为 true
          if (!attrs || typeof attrs !== 'object' || attrs.willReadFrequently === undefined) {
            const merged = Object.assign({}, attrs || {}, { willReadFrequently: true })
            return originalGetContext.call(this, type, merged)
          }
        }
        return originalGetContext.call(this, type, attrs)
      }
    }
  } catch (patchErr) {
    // 如果 patch 失败，不影响后续逻辑，仅在控制台记录
    console.warn('无法应用 canvas.getContext 补丁:', patchErr)
  }

  // 动态加载 echarts 及 wordcloud 插件（仅在客户端）
  try {
    const echartsModule = await import('echarts')
    // echarts-wordcloud 插件会自动向 echarts 注册 series
    await import('echarts-wordcloud')

    echarts = echartsModule.default || echartsModule

    // 初始化图表
    await nextTick()
    const container = wordcloudContainerInner.value || wordcloudContainer.value
    if (container) {
      chart = echarts.init(container)
      debouncedUpdateChart()
    }

    window.addEventListener('resize', handleResize)
  } catch (e) {
    console.error('加载 ECharts 或插件失败:', e)
  }
})

onUnmounted(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
  if (import.meta.client) {
    window.removeEventListener('resize', handleResize)
  }
  if (chart && echarts) {
    try {
      chart.dispose()
    } catch (e) {
      // ignore
    }
    chart = null
  }

  // 恢复被覆盖的 getContext 实现
  // 注意：如果有多个组件实例，这里可能会过早恢复，但通常不影响功能，只是性能警告会回来
  try {
    if (originalGetContext) {
      (HTMLCanvasElement.prototype as any).getContext = originalGetContext
      originalGetContext = null
    }
  } catch (restoreErr) {
    // 忽略恢复错误
  }
})

// 保持兼容的导出方法名
defineExpose({
  generateWordCloud: updateChart
})
</script>

<style scoped>
/* 词云容器样式 */
.relative > div[ref] {
  width: 150%;
}

.w-full.h-full {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
</style>