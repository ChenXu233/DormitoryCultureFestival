<template>
  <div class="word-cloud-selector">
    <h3 class="text-lg font-medium mb-4">选择描述室友特质的词汇（最多10个）</h3>
    
    <!-- 词汇标签组 -->
    <div class="flex flex-wrap gap-2 mb-4">
      <button
        v-for="word in words"
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
import { ref, computed } from 'vue'

// Props
interface Props {
  words?: Array<{ text: string; value?: number }>
}

const props = withDefaults(defineProps<Props>(), {
  words: () => [
    // 预设50+个描述室友特质的词汇
    { text: '友善' },
    { text: '幽默' },
    { text: '责任心' },
    { text: '细心' },
    { text: '热情' },
    { text: '开朗' },
    { text: '善解人意' },
    { text: '聪明' },
    { text: '勤奋' },
    { text: '乐观' },
    { text: '诚实' },
    { text: '正直' },
    { text: '可靠' },
    { text: '慷慨' },
    { text: '耐心' },
    { text: '积极' },
    { text: '理性' },
    { text: '感性' },
    { text: '稳重' },
    { text: '活泼' },
    { text: '冷静' },
    { text: '外向' },
    { text: '内向' },
    { text: '独立' },
    { text: '合作' },
    { text: '创新' },
    { text: '踏实' },
    { text: '细心' },
    { text: '有条理' },
    { text: '整洁' },
    { text: '爱干净' },
    { text: '有趣' },
    { text: '健谈' },
    { text: '安静' },
    { text: '乐于助人' },
    { text: '善解人意' },
    { text: '有同理心' },
    { text: '有爱心' },
    { text: '有正义感' },
    { text: '有创造力' },
    { text: '有领导力' },
    { text: '有团队精神' },
    { text: '有毅力' },
    { text: '有耐心' },
    { text: '有幽默感' },
    { text: '有品味' },
    { text: '有活力' },
    { text: '温柔' },
    { text: '坚强' },
    { text: '勇敢' }
  ]
})

// Emits
const emit = defineEmits<{
  (e: 'confirm', words: string[]): void
  (e: 'selectionChange', words: string[]): void
}>()

// 响应式数据
const selectedWords = ref<string[]>([])

// 计算属性
const isSelected = (word: string) => {
  return selectedWords.value.includes(word)
}

// 方法
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

// 导出方法供父组件调用
defineExpose({
  selectedWords,
  clearAll,
  toggleSelection
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