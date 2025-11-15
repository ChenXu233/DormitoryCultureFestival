<template>
  <div class="word-cloud-theme-selector">
    <h3 class="text-lg font-medium mb-4">自定义词云外观</h3>
    
    <!-- 颜色主题选择 -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">颜色主题</label>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <button
          v-for="theme in colorThemes"
          :key="theme.name"
          :class="[
            'p-2 rounded-md border-2 transition-all duration-200',
            selectedTheme.colorTheme === theme.name 
              ? 'border-blue-500' 
              : 'border-transparent hover:border-gray-300'
          ]"
          @click="selectColorTheme(theme.name)"
        >
          <div class="flex gap-1 mb-2">
            <div 
              v-for="color in theme.colors" 
              :key="color" 
              class="w-3 h-3 rounded-full" 
              :style="{ backgroundColor: color }"
            ></div>
          </div>
          <span class="text-xs text-center block">{{ theme.name }}</span>
        </button>
      </div>
    </div>
    
    <!-- 形状选择 -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">词云形状</label>
      <div class="grid grid-cols-3 sm:grid-cols-4 gap-3">
        <button
          v-for="shape in shapes"
          :key="shape.value"
          :class="[
            'p-2 rounded-md border-2 transition-all duration-200 flex items-center justify-center aspect-square',
            selectedTheme.shape === shape.value 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-transparent hover:border-gray-300 hover:bg-gray-50'
          ]"
          @click="selectShape(shape.value)"
        >
          <span class="text-sm">{{ shape.label }}</span>
        </button>
      </div>
    </div>
    
    <!-- 背景颜色选择 -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">背景颜色</label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="bgColor in bgColors"
          :key="bgColor.value"
          :class="[
            'w-8 h-8 rounded-full border-2 transition-all duration-200',
            selectedTheme.bgColor === bgColor.value 
              ? 'border-blue-500 scale-110' 
              : 'border-transparent hover:border-gray-300'
          ]"
          :style="{ backgroundColor: bgColor.value }"
          @click="selectBgColor(bgColor.value)"
        >
          <span v-if="bgColor.value === 'transparent'" class="text-xs text-gray-500">透明</span>
        </button>
      </div>
    </div>
    
    <!-- 文字大小调整 -->
    <div class="mb-4">
      <div class="flex justify-between items-center mb-2">
        <label class="block text-sm font-medium text-gray-700">文字大小变化</label>
        <span class="text-xs text-gray-500">{{ textScale }}%</span>
      </div>
      <input
        type="range"
        min="50"
        max="150"
        value="100"
        v-model.number="textScale"
        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        @input="updateTextScale"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'

// Props
interface Props {
  modelValue?: {
    colorTheme?: string
    shape?: string
    bgColor?: string
    textScale?: number
  }
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => ({
    colorTheme: 'default',
    shape: 'circle',
    bgColor: '#f9fafb',
    textScale: 100
  })
})

// Emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: any): void
  (e: 'change', value: any): void
}>()

// 颜色主题定义
const colorThemes = [
  { name: 'default', colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'] },
  { name: 'blue', colors: ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe'] },
  { name: 'green', colors: ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5'] },
  { name: 'warm', colors: ['#f59e0b', '#fbbf24', '#fcd34d', '#fde68a', '#fef3c7'] },
  { name: 'purple', colors: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'] },
  { name: 'pastel', colors: ['#fca5a5', '#f9a8d4', '#c4b5fd', '#93c5fd', '#6ee7b7'] }
]

// 形状定义
const shapes = [
  { label: '圆形', value: 'circle' },
  { label: '椭圆', value: 'cardioid' },
  { label: '菱形', value: 'diamond' },
  { label: '三角形', value: 'triangle-forward' },
  { label: '五角星', value: 'pentagon' },
  { label: '六边形', value: 'hexagon' },
  { label: '正方形', value: 'square' },
  { label: '随机', value: 'random' }
]

// 背景颜色定义
const bgColors = [
  { label: '白色', value: '#ffffff' },
  { label: '浅灰', value: '#f9fafb' },
  { label: '中灰', value: '#f3f4f6' },
  { label: '深蓝', value: '#1e40af' },
  { label: '浅蓝', value: '#dbeafe' },
  { label: '浅绿', value: '#d1fae5' },
  { label: '透明', value: 'transparent' }
]

// 响应式数据
const selectedTheme = reactive({
  colorTheme: props.modelValue.colorTheme,
  shape: props.modelValue.shape,
  bgColor: props.modelValue.bgColor,
  textScale: props.modelValue.textScale
})

const textScale = ref(selectedTheme.textScale)

// 计算属性 - 当前主题颜色
const currentThemeColors = computed(() => {
  const theme = colorThemes.find(t => t.name === selectedTheme.colorTheme)
  return theme?.colors || colorThemes[0].colors
})

// 方法
const selectColorTheme = (themeName: string) => {
  selectedTheme.colorTheme = themeName
  emitChanges()
}

const selectShape = (shapeValue: string) => {
  selectedTheme.shape = shapeValue
  emitChanges()
}

const selectBgColor = (bgColorValue: string) => {
  selectedTheme.bgColor = bgColorValue
  emitChanges()
}

const updateTextScale = () => {
  selectedTheme.textScale = textScale.value
  emitChanges()
}

const emitChanges = () => {
  emit('update:modelValue', { ...selectedTheme })
  emit('change', { ...selectedTheme, colors: currentThemeColors.value })
}

// 监听props变化
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    Object.assign(selectedTheme, newVal)
    textScale.value = selectedTheme.textScale
  }
}, { deep: true })

// 导出计算属性和方法供父组件使用
defineExpose({
  currentThemeColors,
  selectedTheme,
  selectColorTheme,
  selectShape,
  selectBgColor
})
</script>

<style scoped>
.word-cloud-theme-selector {
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
}
</style>