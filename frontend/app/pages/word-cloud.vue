<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <!-- 页面标题 -->
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">最佳室友词云</h1>
        <p class="text-gray-600">选择描述你室友特质的词汇，生成专属词云</p>
      </div>

      <!-- 主要内容区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左侧：词汇选择器 -->
        <div class="lg:col-span-1">
          <div class="sticky top-6">
            <WordCloudSelector 
              ref="selectorRef"
              @confirm="handleWordSelectionConfirm"
              @selectionChange="handleWordSelectionChange"
            />
          </div>
        </div>

        <!-- 中间：词云展示 -->
        <div class="lg:col-span-2">
          <!-- 词云展示区域 -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
            <!-- 标签切换 -->
            <div class="flex border-b border-gray-200 mb-4">
              <button
                :class="[
                  'px-4 py-2 font-medium text-sm transition-colors flex-1 text-center',
                  activeTab === 'personal' 
                    ? 'text-blue-600 border-b-2 border-blue-500' 
                    : 'text-gray-500 hover:text-gray-700'
                ]"
                @click="switchTab('personal')"
              >
                我的室友词云
              </button>
              <button
                :class="[
                  'px-4 py-2 font-medium text-sm transition-colors flex-1 text-center',
                  activeTab === 'global' 
                    ? 'text-blue-600 border-b-2 border-blue-500' 
                    : 'text-gray-500 hover:text-gray-700'
                ]"
                @click="switchTab('global')"
              >
                全局词云
                <span v-if="globalWordCloudData.length > 0" class="ml-1 text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded-full">
                  实时
                </span>
              </button>
            </div>
            
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold text-gray-800">
                {{ activeTab === 'personal' ? '我的词云' : '大家眼中的最佳室友' }}
              </h2>
              
              <!-- 操作按钮 -->
              <div class="flex gap-2">
                <button
                  class="px-3 py-1.5 bg-blue-50 text-blue-600 rounded-md text-sm hover:bg-blue-100 transition-colors flex items-center gap-1"
                  :disabled="!wordCloudGenerated || (activeTab === 'personal' && selectedWords.length === 0)"
                  @click="downloadWordCloud"
                >
                  <span>下载</span>
                </button>
                <button
                  class="px-3 py-1.5 bg-green-50 text-green-600 rounded-md text-sm hover:bg-green-100 transition-colors flex items-center gap-1"
                  :disabled="!wordCloudGenerated || (activeTab === 'personal' && selectedWords.length === 0)"
                  @click="shareWordCloud"
                >
                  <span>分享</span>
                </button>
              </div>
            </div>
            
            <!-- 词云组件 -->
            <WordCloud 
              ref="wordCloudRef"
              :words="wordCloudData"
              :theme="wordCloudTheme"
              @rendered="handleWordCloudRendered"
            />
            
            <!-- 空状态提示 -->
            <div v-if="activeTab === 'personal' && selectedWords.length === 0 && !loading" class="text-center py-16 text-gray-500">
              <div class="mb-4 text-4xl">☁️</div>
              <p>请从左侧选择描述室友特质的词汇</p>
            </div>
            
            <!-- 全局词云加载状态 -->
            <div v-if="activeTab === 'global' && loading" class="text-center py-16 text-gray-500">
              <div class="mb-4 w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p>加载全局词云数据中...</p>
            </div>
          </div>
          
          <!-- 词云主题设置 -->
          <WordCloudThemeSelector 
            v-model="themeSettings"
            @change="handleThemeChange"
          />
        </div>
      </div>
    </div>
    
    <!-- 分享模态框 -->
    <div v-if="showShareModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">分享词云</h3>
          <button class="text-gray-500 hover:text-gray-700" @click="showShareModal = false">
            ✕
          </button>
        </div>
        <div class="mb-4">
          <img 
            :src="shareImageUrl" 
            alt="词云分享" 
            class="w-full rounded border border-gray-200"
          />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">分享链接</label>
          <input 
            type="text" 
            :value="shareUrl" 
            readonly 
            class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
          />
        </div>
        <div class="flex gap-2">
          <button 
            class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
            @click="copyShareUrl"
          >
            复制链接
          </button>
          <button 
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
            @click="showShareModal = false"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
    
    <!-- 提示消息 -->
    <div v-if="showToast" class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-md shadow-lg z-50 animate-fade-in">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, nextTick, onMounted } from 'vue'
import WordCloud from '../components/WordCloud.vue'
import WordCloudSelector from '../components/WordCloudSelector.vue'
import WordCloudThemeSelector from '../components/WordCloudThemeSelector.vue'

// API基础URL
const API_BASE_URL = 'http://localhost:8000'

// Refs
const wordCloudRef = ref<InstanceType<typeof WordCloud>>()
const selectorRef = ref<InstanceType<typeof WordCloudSelector>>()

// 响应式数据
const selectedWords = ref<string[]>([])
const globalWordCloudData = ref<Array<{text: string; value: number}>>([])
const wordCloudGenerated = ref(false)
const loading = ref(false)
const showShareModal = ref(false)
const shareImageUrl = ref('')
const shareUrl = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const activeTab = ref<'personal' | 'global'>('personal')
const presetWords = ref<string[]>([])

// 主题设置
const themeSettings = reactive({
  colorTheme: 'default',
  shape: 'circle',
  bgColor: '#f9fafb',
  textScale: 100
})

// 词云主题数据
const wordCloudTheme = computed(() => {
  const themes = {
    default: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
    blue: ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe'],
    green: ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5'],
    warm: ['#f59e0b', '#fbbf24', '#fcd34d', '#fde68a', '#fef3c7'],
    purple: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'],
    pastel: ['#fca5a5', '#f9a8d4', '#c4b5fd', '#93c5fd', '#6ee7b7']
  }
  
  return {
    bgColor: themeSettings.bgColor,
    colors: themes[themeSettings.colorTheme as keyof typeof themes] || themes.default
  }
})

// 当前显示的词云数据
const wordCloudData = computed(() => {
  if (activeTab.value === 'global') {
    return globalWordCloudData.value
  }
  
  // 个人词云数据 - 使用递减的词频值，确保词云显示合理
  return selectedWords.value.map((word, index) => ({
    text: word,
    value: Math.max(10, 50 - index * 5) // 第一个词50，依次递减，最小10
  }))
})

// API方法
const fetchGlobalWordCloud = async () => {
  try {
    loading.value = true
    const response = await fetch(`${API_BASE_URL}/api/wordcloud/global`)
    if (response.ok) {
      const data = await response.json()
      globalWordCloudData.value = data
    }
  } catch (error) {
    console.error('获取全局词云数据失败:', error)
    // 使用模拟数据
    globalWordCloudData.value = [
      { text: '友善', value: 45 },
      { text: '幽默', value: 38 },
      { text: '责任心', value: 35 },
      { text: '细心', value: 32 },
      { text: '热情', value: 30 },
      { text: '开朗', value: 28 },
      { text: '善解人意', value: 25 },
      { text: '勤奋', value: 22 },
      { text: '乐观', value: 20 },
      { text: '诚实', value: 18 },
      { text: '可靠', value: 16 },
      { text: '慷慨', value: 14 },
      { text: '耐心', value: 12 },
      { text: '积极', value: 10 },
      { text: '理性', value: 9 }
    ]
  } finally {
    loading.value = false
  }
}

const fetchPresetWords = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/wordcloud/words`)
    if (response.ok) {
      const data = await response.json()
      presetWords.value = data
    }
  } catch (error) {
    console.error('获取预设词汇失败:', error)
  }
}

const saveWordCloudSelection = async (words: string[]) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/wordcloud/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words,
        theme: {
          ...themeSettings
        }
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      return data.id
    }
  } catch (error) {
    console.error('保存词云选择失败:', error)
  }
  return null
}

// 方法
const handleWordSelectionChange = (words: string[]) => {
  selectedWords.value = words
}

const handleWordSelectionConfirm = async (words: string[]) => {
  selectedWords.value = words
  
  // 保存到后端
  if (words.length > 0) {
    const entryId = await saveWordCloudSelection(words)
    if (entryId) {
      showToastMessage('词云选择已保存')
      // 重新获取全局词云数据
      fetchGlobalWordCloud()
    }
  }
  
  nextTick(() => {
    wordCloudRef.value?.generateWordCloud()
  })
}

const handleThemeChange = (theme: any) => {
  nextTick(() => {
    wordCloudRef.value?.generateWordCloud()
  })
}

const handleWordCloudRendered = () => {
  wordCloudGenerated.value = true
}

const downloadWordCloud = () => {
  if (!wordCloudRef.value || !process.client) return
  
  const canvas = document.querySelector('canvas')
  if (canvas) {
    // 创建下载链接
    const link = document.createElement('a')
    const filename = activeTab.value === 'global' 
      ? `全局最佳室友词云_${new Date().toLocaleDateString()}.png`
      : `我的室友词云_${new Date().toLocaleDateString()}.png`
    
    link.download = filename
    link.href = canvas.toDataURL('image/png')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    showToastMessage('词云已下载')
  }
}

const shareWordCloud = async () => {
  if (!wordCloudRef.value || !process.client) return
  
  const canvas = document.querySelector('canvas')
  if (canvas) {
    // 生成分享图片URL
    shareImageUrl.value = canvas.toDataURL('image/png')
    
    // 生成分享链接
    const params = new URLSearchParams()
    params.append('tab', activeTab.value)
    if (activeTab.value === 'personal') {
      params.append('words', selectedWords.value.join(','))
    }
    
    shareUrl.value = `${window.location.origin}${window.location.pathname}?${params.toString()}`
    showShareModal.value = true
  }
}

const copyShareUrl = () => {
  if (!process.client) return
  
  navigator.clipboard.writeText(shareUrl.value)
    .then(() => {
      showToastMessage('分享链接已复制')
    })
    .catch(err => {
      console.error('复制失败:', err)
    })
}

const showToastMessage = (message: string) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const switchTab = (tab: 'personal' | 'global') => {
  activeTab.value = tab
  nextTick(() => {
    wordCloudRef.value?.generateWordCloud()
  })
}

// 页面加载时检查URL参数，恢复词汇选择
const initFromUrl = () => {
  if (!process.client) return
  
  const params = new URLSearchParams(window.location.search)
  const tabParam = params.get('tab')
  const wordsParam = params.get('words')
  
  // 设置激活的标签
  if (tabParam === 'global') {
    activeTab.value = 'global'
  }
  
  // 设置选择的词汇
  if (wordsParam) {
    const words = wordsParam.split(',')
    if (words.length > 0) {
      selectedWords.value = words
      nextTick(() => {
        wordCloudRef.value?.generateWordCloud()
      })
    }
  }
}

// 组件挂载时初始化
onMounted(async () => {
  initFromUrl()
  await fetchPresetWords()
  await fetchGlobalWordCloud()
  
  // 数据加载完成后生成词云
  nextTick(() => {
    wordCloudRef.value?.generateWordCloud()
  })
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>