<template>
  <div class="bg-white rounded-xl shadow-lg p-8">
    <div class="text-center">
      <div class="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
        </svg>
      </div>
      
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">
        输入团队特质代码
      </h2>
      <p class="text-gray-600 mb-6">
        请输入四个4位唯一代码，系统将分析团队特质匹配度并生成专属评语
      </p>

      <!-- 代码输入表单 -->
      <div class="max-w-2xl mx-auto">
        <div class="grid grid-cols-2 gap-4">
          <div v-for="i in 4" :key="i">
            <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
              成员{{ i }}代码
            </label>
            <input 
              :value="modelValue[i-1]"
              @input="updateCode(i-1, ($event.target as HTMLInputElement).value)"
              type="text" 
              :placeholder="`请输入成员${i}的4位代码`"
              maxlength="4"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-center text-xl font-mono"
            >
          </div>
        </div>
        
        <button 
          :disabled="!canSubmit"
          :class="[
            'w-full mt-6 font-medium py-3 px-6 rounded-lg transition-colors duration-200',
            canSubmit 
              ? 'bg-orange-600 hover:bg-orange-700 text-white' 
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          ]"
          @click="$emit('submit')"
        >
          开始团队匹配
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: string[]
}

interface Emits {
  (e: 'update:modelValue', value: string[]): void
  (e: 'submit'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const canSubmit = computed(() => {
  return props.modelValue.every(code => code.length === 4)
})

const updateCode = (index: number, value: string) => {
  const newCodes = [...props.modelValue]
  newCodes[index] = value
  emit('update:modelValue', newCodes)
}
</script>
