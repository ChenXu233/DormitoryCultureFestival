  <template>
  <div class="background-panel">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">桌面背景</h2>
    
    <div class="grid grid-cols-2 gap-3">
      <div 
        v-for="background in backgrounds" 
        :key="background.id"
        @click="selectBackground(background)"
        :class="[
          'h-20 rounded-lg cursor-pointer border-2 transition-all group relative overflow-hidden',
          selectedBackground.id === background.id 
            ? 'border-blue-500 ring-2 ring-blue-200' 
            : 'border-gray-200 hover:border-gray-300'
        ]"
        :style="getBackgroundStyle(background)"
      >
        <!-- 背景预览 -->
        <div 
          class="absolute inset-0 flex items-center justify-center text-white font-medium transition-transform group-hover:scale-105"
          :style="{
            textShadow: '0 1px 2px rgba(0,0,0,0.3)',
            color: getContrastColor(background.color)
          }"
        >
          {{ background.name }}
        </div>
        
        <!-- 选中标记 -->
        <div 
          v-if="selectedBackground.id === background.id"
          class="absolute top-2 right-2 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center"
        >
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
        </div>
      </div>
    </div>
    
    <!-- 自定义背景颜色 -->
    <div class="mt-6">
      <h3 class="font-medium text-gray-700 mb-3">自定义背景</h3>
      <div class="flex items-center space-x-3">
        <input 
          type="color" 
          v-model="customColor"
          @change="onCustomColorChange"
          class="w-12 h-12 rounded border-2 border-gray-300 cursor-pointer"
        >
        <div class="flex-1">
          <input 
            type="text" 
            v-model="customColor"
            @input="onCustomColorInput"
            placeholder="#FFFFFF"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
          >
        </div>
        <button 
          @click="applyCustomBackground"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors"
        >
          应用
        </button>
      </div>
    </div>
    
    <!-- 背景效果选项 -->
    <div class="mt-6">
      <h3 class="font-medium text-gray-700 mb-3">背景效果</h3>
      <div class="space-y-4">
        <!-- 渐变背景 -->
        <div>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input 
              type="checkbox" 
              v-model="enableGradient"
              @change="onEffectChange"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            >
            <span class="text-sm text-gray-700">渐变背景</span>
          </label>
          
          <div v-if="enableGradient" class="ml-6 mt-3 space-y-3">
            <div class="flex items-center space-x-3">
              <span class="text-sm text-gray-600 w-16">起始色</span>
              <input 
                type="color" 
                v-model="gradientStart"
                @change="onGradientChange"
                class="w-8 h-8 rounded border border-gray-300 cursor-pointer"
              >
              <input 
                type="text" 
                v-model="gradientStart"
                @input="onGradientChange"
                class="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
              >
            </div>
            <div class="flex items-center space-x-3">
              <span class="text-sm text-gray-600 w-16">结束色</span>
              <input 
                type="color" 
                v-model="gradientEnd"
                @change="onGradientChange"
                class="w-8 h-8 rounded border border-gray-300 cursor-pointer"
              >
              <input 
                type="text" 
                v-model="gradientEnd"
                @input="onGradientChange"
                class="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
              >
            </div>
          </div>
        </div>
        
        <!-- 纹理图案 -->
        <div>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input 
              type="checkbox" 
              v-model="enablePattern"
              @change="onEffectChange"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            >
            <span class="text-sm text-gray-700">纹理图案</span>
          </label>
          
          <div v-if="enablePattern" class="ml-6 mt-3">
            <div class="grid grid-cols-3 gap-2">
              <div 
                v-for="pattern in patterns" 
                :key="pattern.id"
                @click="selectPattern(pattern)"
                :class="[
                  'h-16 rounded-lg cursor-pointer border-2 transition-all relative overflow-hidden',
                  selectedPatternId === pattern.id
                    ? 'border-blue-500 ring-2 ring-blue-200'
                    : 'border-gray-200 hover:border-gray-300'
                ]"
                :style="{ background: pattern.value }"
              >
                <!-- 选中标记 -->
                <div 
                  v-if="selectedPatternId === pattern.id"
                  class="absolute top-1 right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center"
                >
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 定义背景接口
interface Background {
  id: number | string
  name: string
  color: string
  type?: 'solid' | 'gradient' | 'pattern'
}

// 定义纹理图案接口
interface Pattern {
  id: number | string
  name: string
  value: string
}

// 定义组件属性
interface Props {
  backgrounds?: Background[]
  initialBackground?: Background
}

// 定义组件事件
interface Emits {
  (e: 'background-change', background: Background): void
}

// 组件属性
const props = withDefaults(defineProps<Props>(), {
  backgrounds: () => [
    { id: 1, name: '木质桌面', color: '#f5deb3', type: 'solid' },
    { id: 2, name: '白色桌面', color: '#ffffff', type: 'solid' },
    { id: 3, name: '黑色桌面', color: '#2d3748', type: 'solid' },
    { id: 4, name: '蓝色桌面', color: '#bee3f8', type: 'solid' },
    { id: 5, name: '绿色桌面', color: '#c6f6d5', type: 'solid' },
    { id: 6, name: '粉色桌面', color: '#fed7d7', type: 'solid' },
    { id: 7, name: '木纹纹理', color: '#deb887', type: 'pattern' },
    { id: 8, name: '网格纹理', color: '#f0f0f0', type: 'pattern' }
  ],
  initialBackground: () => ({ id: 1, name: '木质桌面', color: '#f5deb3', type: 'solid' })
})

// 组件事件
const emit = defineEmits<Emits>()

// 纹理图案列表
const patterns = ref<Pattern[]>([
  {
    id: 1,
    name: '斜条纹',
    value: 'repeating-linear-gradient(45deg, #f0f0f0, #f0f0f0 10px, #e0e0e0 10px, #e0e0e0 20px)'
  },
  {
    id: 2,
    name: '横线',
    value: 'repeating-linear-gradient(0deg, #f0f0f0, #f0f0f0 10px, #e0e0e0 10px, #e0e0e0 11px)'
  },
  {
    id: 3,
    name: '圆点',
    value: 'radial-gradient(circle, #e0e0e0 2px, transparent 2px) 0 0 / 10px 10px'
  },
  {
    id: 4,
    name: '方格',
    value: 'linear-gradient(45deg, #e0e0e0 25%, transparent 25%) -5px 0, linear-gradient(-45deg, #e0e0e0 25%, transparent 25%) -5px 0, linear-gradient(45deg, transparent 75%, #e0e0e0 75%), linear-gradient(-45deg, transparent 75%, #e0e0e0 75%)'
  },
  {
    id: 5,
    name: '波浪',
    value: 'repeating-radial-gradient(circle at 50% 50%, #f0f0f0, #f0f0f0 5px, #e0e0e0 5px, #e0e0e0 10px)'
  },
  {
    id: 6,
    name: '点阵',
    value: 'linear-gradient(90deg, #e0e0e0 1px, transparent 1px) 0 0 / 10px 10px, linear-gradient(#e0e0e0 1px, transparent 1px) 0 0 / 10px 10px'
  },
  {
    id: 7,
    name: '木纹',
    value: 'repeating-linear-gradient(45deg, #deb887, #deb887 2px, #d2b48c 2px, #d2b48c 4px)'
  },
  {
    id: 8,
    name: '牛仔布',
    value: 'repeating-linear-gradient(90deg, #2b580c 1px, transparent 1px) 0 0 / 15px 15px, repeating-linear-gradient(0deg, #2b580c 1px, transparent 1px) 0 0 / 15px 15px, #558b2f'
  },
  {
    id: 9,
    name: '大理石',
    value: 'radial-gradient(circle at 50% 50%, #f5f5f5, #f5f5f5 1px, #e0e0e0 1px, #e0e0e0 2px) 0 0 / 20px 20px'
  }
])

// 响应式数据
const selectedBackground = ref<Background>(props.initialBackground)
const customColor = ref('#f5deb3')
const enableGradient = ref(false)
const enablePattern = ref(false)
const gradientStart = ref('#bee3f8')
const gradientEnd = ref('#c6f6d5')
const selectedPatternId = ref<number | string>(1)

// 获取背景样式
const getBackgroundStyle = (background: Background) => {
  if (background.type === 'pattern') {
    // 为预设的纹理背景添加对应的样式
    if (background.id === 7) return { background: patterns.value[6].value } // 木纹纹理
    if (background.id === 8) return { background: patterns.value[5].value } // 网格纹理
  }
  return { background: background.color }
}

// 根据背景颜色获取对比色
const getContrastColor = (hexColor: string) => {
  // 简单的亮度计算
  const hex = hexColor.replace('#', '')
  const r = parseInt(hex.substr(0, 2), 16)
  const g = parseInt(hex.substr(2, 2), 16)
  const b = parseInt(hex.substr(4, 2), 16)
  
  // 计算亮度（YIQ公式）
  const brightness = (r * 299 + g * 587 + b * 114) / 1000
  
  return brightness > 128 ? '#000000' : '#ffffff'
}

// 选择背景
const selectBackground = (background: Background) => {
  selectedBackground.value = background
  customColor.value = background.color
  enableGradient.value = false
  enablePattern.value = false
  
  emit('background-change', background)
}

// 选择纹理图案
const selectPattern = (pattern: Pattern) => {
  selectedPatternId.value = pattern.id
  
  const patternBackground: Background = {
    id: `pattern-${pattern.id}`,
    name: pattern.name,
    color: pattern.value,
    type: 'pattern'
  }
  
  selectedBackground.value = patternBackground
  emit('background-change', patternBackground)
}

// 自定义颜色变化
const onCustomColorChange = () => {
  const customBackground: Background = {
    id: 'custom',
    name: '自定义颜色',
    color: customColor.value,
    type: 'solid'
  }
  
  selectedBackground.value = customBackground
  emit('background-change', customBackground)
}

const onCustomColorInput = () => {
  // 验证颜色格式
  if (/^#[0-9A-F]{6}$/i.test(customColor.value)) {
    onCustomColorChange()
  }
}

// 应用自定义背景
const applyCustomBackground = () => {
  onCustomColorChange()
}

// 渐变背景变化
const onGradientChange = () => {
  if (enableGradient.value) {
    const gradientBackground: Background = {
      id: 'gradient',
      name: '渐变背景',
      color: `linear-gradient(135deg, ${gradientStart.value}, ${gradientEnd.value})`,
      type: 'gradient'
    }
    
    selectedBackground.value = gradientBackground
    emit('background-change', gradientBackground)
  }
}

// 效果变化
const onEffectChange = () => {
  if (enableGradient.value) {
    enablePattern.value = false
    onGradientChange()
  } else if (enablePattern.value) {
    enableGradient.value = false
    // 默认选择第一个纹理图案
    const selectedPattern = patterns.value.find(p => p.id === selectedPatternId.value) || patterns.value[0]
    selectPattern(selectedPattern)
  } else {
    // 恢复默认背景
    selectBackground(props.backgrounds[0])
  }
}

// 监听初始背景变化
watch(() => props.initialBackground, (newBackground) => {
  if (newBackground) {
    selectedBackground.value = newBackground
    customColor.value = newBackground.color
    
    // 如果初始背景是纹理图案，启用纹理选项
    if (newBackground.type === 'pattern') {
      enablePattern.value = true
    }
  }
}, { immediate: true })

// 暴露方法给父组件
defineExpose({
  selectedBackground,
  selectBackground
})
</script>

<style scoped>
/* 自定义颜色输入框样式 */
input[type="color"] {
  -webkit-appearance: none;
  border: none;
}

input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
}

input[type="color"]::-webkit-color-swatch {
  border: none;
  border-radius: 4px;
}

/* 渐变预览效果 */
.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}
</style>