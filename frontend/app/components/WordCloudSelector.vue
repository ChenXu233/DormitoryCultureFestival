<template>
  <div class="word-cloud-selector">
    <h3 class="text-lg font-medium mb-4">选择描述室友特质的词汇（最多10个）</h3>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="mb-4 text-center">
      <div class="inline-block w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"/>
      <p class="text-sm text-gray-500 mt-2">正在加载词汇列表...</p>
    </div>
    
    <!-- 错误提示 -->
    <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
      <p class="text-sm text-red-600">{{ error }}</p>
    </div>
    
    <!-- 词汇标签组 -->
    <div v-if="!loading" class="flex flex-wrap gap-2 mb-4">
      <button
        v-for="word in displayWords"
        :key="word.text"
        :class="[
          'px-3 py-1.5 rounded-full text-sm transition-all duration-200',
          isSelected(word.text) 
            ? 'bg-blue-500 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
        :disabled="!isSelected(word.text) && selectedWords.length >= 10"
        @click="toggleSelection(word.text)"
      >
        {{ word.text }}
      </button>
    </div>
    
    <!-- 已选词汇显示 -->
    <div v-if="selectedWords.length > 0" class="mb-4">
      <p class="text-sm text-gray-500 mb-2">已选择 {{ selectedWords.length }}/10 个词汇：</p>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="word in selectedWords"
          :key="word"
          class="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-sm flex items-center gap-1"
        >
          {{ word }}
          <button 
            class="text-blue-500 hover:text-blue-700 transition-colors"
            @click="removeSelection(word)"
          >
            ✕
          </button>
        </span>
      </div>
    </div>
    
    <!-- 提示信息 -->
    <div v-if="selectedWords.length >= 10" class="text-sm text-yellow-600 mb-4">
      已达到选择上限（10个）
    </div>
    
    <!-- 操作按钮 -->
    <div class="flex gap-2 mt-4">
      <button
        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
        @click="clearAll"
      >
        清空选择
      </button>
      <button
        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        :disabled="selectedWords.length === 0"
        @click="confirmSelection"
      >
        确认选择
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import  CONFIG  from '../config/config'
// Props
interface Props {
  words?: Array<{ text: string; value?: number }>
}

const props = withDefaults(defineProps<Props>(), {
  words: () => []
})

// API基础URL
const API_BASE_URL = CONFIG.apiBaseUrl

// Emits
const emit = defineEmits<{
  (e: 'confirm' | 'selectionChange', words: string[]): void
}>()

// 响应式数据
const selectedWords = ref<string[]>([])
const presetWords = ref<string[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// 计算属性
const isSelected = (word: string) => {
  return selectedWords.value.includes(word)
}

// 获取显示的词汇列表（优先使用props传入的词汇，否则使用从后端获取的预设词汇）
const displayWords = computed(() => {
  if (props.words && props.words.length > 0) {
    return props.words
  }
  return presetWords.value.map(word => ({ text: word }))
})

// 方法
const fetchPresetWords = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await fetch(`${API_BASE_URL}/api/wordcloud/words`)
    if (response.ok) {
      const data = await response.json()
      presetWords.value = data
    } else {
      error.value = '获取预设词汇失败'
    }
  } catch (err) {
    console.error('获取预设词汇失败:', err)
    error.value = '网络连接失败，请检查后端服务是否运行'
    // 使用默认词汇作为后备
    presetWords.value = [
      '友善', '幽默', '责任心', '细心', '热情', '开朗', '善解人意', '聪明', '勤奋', '乐观',
      '诚实', '正直', '可靠', '慷慨', '耐心', '积极', '理性', '感性', '稳重', '活泼',
      '冷静', '外向', '内向', '独立', '合作', '创新', '踏实', '有条理', '整洁', '爱干净',
      '有趣', '健谈', '安静', '乐于助人', '有同理心', '有爱心', '有正义感', '有创造力',
      '有领导力', '有团队精神', '有毅力', '有幽默感', '有品味', '有活力', '温柔', '坚强', '勇敢'
    ]
  } finally {
    loading.value = false
  }
}

const toggleSelection = (word: string) => {
  const index = selectedWords.value.indexOf(word)
  if (index > -1) {
    // 如果已选择，则取消选择
    selectedWords.value.splice(index, 1)
  } else {
    // 如果未选择且未达到上限，则添加选择
    if (selectedWords.value.length < 10) {
      selectedWords.value.push(word)
    }
  }
  emitSelectionChange()
}

const removeSelection = (word: string) => {
  const index = selectedWords.value.indexOf(word)
  if (index > -1) {
    selectedWords.value.splice(index, 1)
    emitSelectionChange()
  }
}

const clearAll = () => {
  selectedWords.value = []
  emitSelectionChange()
}

const confirmSelection = () => {
  emit('confirm', [...selectedWords.value])
}

const emitSelectionChange = () => {
  emit('selectionChange', [...selectedWords.value])
}

// 组件挂载时自动获取预设词汇
onMounted(() => {
  // 只有当没有通过props传入词汇时才从后端获取
  if (!props.words || props.words.length === 0) {
    fetchPresetWords()
  }
})

// 导出方法供父组件调用
defineExpose({
  selectedWords,
  clearAll,
  toggleSelection,
  fetchPresetWords
})
</script>

<style scoped>
.word-cloud-selector {
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>