<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 py-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">
          室友默契度答题
        </h1>
        <p class="text-lg text-gray-600">
          测试你和室友的默契程度，看看你们有多了解彼此
        </p>
      </div>

      <!-- 答题流程 -->
      <div v-if="!quizStarted && !quizCompleted" class="bg-white rounded-xl shadow-lg p-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            个人特质测试
          </h2>
          <p class="text-gray-600 mb-8">
            通过答题来推断你的个人特质，完成后将获得4位唯一代码用于特质匹配
          </p>

          <!-- 参与者名称输入（可选） -->
          <div class="mb-4">
            <input
              v-model="participantName"
              type="text"
              placeholder="请输入你的姓名（可选)"
              class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-200">
          </div>

          <!-- 开始测试按钮 -->
          <button 
            class="px-12 py-4 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors duration-200 text-lg"
            @click="startQuiz"
          >
            开始测试
          </button>
        </div>
      </div>

      <!-- 答题界面 -->
      <div v-if="quizStarted && !quizCompleted" class="bg-white rounded-xl shadow-lg p-8">
        <div class="flex justify-between items-center mb-6">
          <div class="text-sm text-gray-600">
            题目 {{ currentQuestionIndex + 1 }} / {{ questions.length }}
          </div>
          <div class="text-sm text-gray-600">
            用时：{{ formatTime(elapsedTime) }}
          </div>
        </div>

        <!-- 问题卡片 -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold text-gray-800 mb-6">
            {{ currentQuestion.question }}
          </h3>
          
          <!-- 选项列表 -->
          <div class="space-y-3">
            <button
v-for="(option, index) in currentQuestion.options" :key="index"
              :class="[
                'w-full text-left px-4 py-3 border rounded-lg transition-colors duration-200',
                selectedAnswer === index ? 'border-green-500 bg-green-50 text-green-700' : 'border-gray-300 hover:border-green-300 hover:bg-green-50'
              ]"
              @click="selectAnswer(index)">
              <div class="flex items-center">
                <span
class="w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3"
                      :class="selectedAnswer === index ? 'border-green-500 bg-green-500 text-white' : 'border-gray-400'">{{ String.fromCharCode(65 + index) }}</span>
                <span>{{ option }}</span>
              </div>
            </button>
          </div>
        </div>

        <!-- 导航按钮 -->
        <div class="flex justify-between">
          <button
            :disabled="currentQuestionIndex === 0"
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            @click="previousQuestion"
          >
            上一题
          </button>
          
          <button
            :class="[
              'px-6 py-2 rounded-lg font-medium',
              selectedAnswer !== null 
                ? 'bg-green-600 hover:bg-green-700 text-white' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
            :disabled="selectedAnswer === null"
            @click="nextQuestion"
          >
            {{ currentQuestionIndex === questions.length - 1 ? '提交答案' : '下一题' }}
          </button>
        </div>
      </div>

      <!-- 答题结果 -->
      <div v-if="quizCompleted" class="bg-white rounded-xl shadow-lg p-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            特质测试完成！
          </h2>
          
          <!-- 唯一代码展示 -->
          <div class="max-w-md mx-auto mb-6">
            <div class="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-8 text-white">
              <div class="text-5xl font-bold mb-2">{{ result.unique_code }}</div>
              <div class="text-lg">你的4位唯一代码</div>
            </div>
            
            <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="text-blue-800 font-medium text-center">
                {{ result.message }}
              </div>
            </div>
            
            <!-- 雷达图与特质展示 -->
              <div class="mt-6">
                <client-only>
                  <RadarChart v-if="result.radar_data" :radar-data="result.radar_data"/>
                </client-only>

                <!-- 特质展示 -->
                <div v-if="result.traits" class="mt-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-4">你的主要特质：</h3>
              <div class="grid grid-cols-2 gap-3">
                <div 
                  v-for="(trait, dimension) in result.traits" 
                  :key="dimension"
                  class="bg-gray-50 border border-gray-200 rounded-lg p-3 text-center"
                >
                  <div class="text-sm text-gray-600">{{ dimension }}</div>
                  <div class="font-medium text-green-600">{{ trait }}</div>
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4 mt-6 text-center">
              <div>
                <div class="text-2xl font-bold text-green-600">{{ questions.length }}</div>
                <div class="text-sm text-gray-600">答题数量</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-purple-600">{{ formatTime(result.time_spent) }}</div>
                <div class="text-sm text-gray-600">用时</div>
              </div>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200"
              @click="restartQuiz"
            >
              重新答题
            </button>
            <NuxtLink 
              to="/match"
              class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors duration-200 text-center"
            >
              双人匹配
            </NuxtLink>
            <NuxtLink 
              to="/team-match"
              class="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors duration-200 text-center"
            >
              团队匹配
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import CONFIG from '../config/config'
import RadarChart from '../components/RadarChart.vue'
const API_BASE_URL = CONFIG.apiBaseUrl
// 设置页面元信息
useSeoMeta({
  title: '室友默契度答题 - 宿舍文化节',
  description: '测试你和室友的默契程度，看看你们有多了解彼此'
})

// 页面配置
definePageMeta({
  layout: false
})

// 答题状态
const quizStarted = ref(false)
const quizCompleted = ref(false)

// 参与者名称（可选）
const participantName = ref<string | null>(null)

// 题目相关
const questions = ref<any[]>([])
const currentQuestionIndex = ref(0)
const selectedAnswer = ref<number | null>(null)
const answers = ref<Record<string, string>>({})

// 计时器
const elapsedTime = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

// 答题结果
const result = ref({
  unique_code: '',
  traits: {} as Record<string, string>,
  trait_scores: {} as Record<string, Record<string, number>>,
  radar_data: { dimensions: [] as string[], scores: [] as number[], max_score: 100 },
  message: '',
  time_spent: 0,
})

// 计算当前问题
const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value] || {}
})

// 格式化时间
const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 开始答题
const startQuiz = async () => {
  try {
    // 获取所有题目
    const response = await $fetch(`${API_BASE_URL}/api/quiz/questions`) as any
    questions.value = response
    quizStarted.value = true
    
    // 开始计时
    elapsedTime.value = 0
    timer = setInterval(() => {
      elapsedTime.value++
    }, 1000)
  } catch (error) {
    console.error('获取题目失败:', error)
    alert('获取题目失败，请稍后重试')
  }
}

// 选择答案
const selectAnswer = (index: number) => {
  selectedAnswer.value = index
  answers.value[currentQuestion.value.id] = index.toString()
}

// 上一题
const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedAnswer.value = parseInt(answers.value[currentQuestion.value.id] ?? '0')
  }
}

// 下一题
const nextQuestion = async () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    selectedAnswer.value = parseInt(answers.value[currentQuestion.value.id] ?? '0')
  } else {
    // 提交答案
    await submitQuiz()
  }
}

// 提交答题
const submitQuiz = async () => {
  try {
    const submission = {
      participant_name: participantName.value,
      answers: answers.value,
      submitted_at: new Date().toISOString(),
    }

    const response = await $fetch(`${API_BASE_URL}/api/quiz/submit`, {
      method: 'POST',
      body: submission
    }) as any

    result.value = response
    quizCompleted.value = true
    
    // 停止计时
    if (timer) {
      clearInterval(timer)
      timer = null
    }
    
    result.value.time_spent = elapsedTime.value
  } catch (error) {
    console.error('提交答案失败:', error)
    alert('提交答案失败，请稍后重试')
  }
}

// 重新开始
const restartQuiz = () => {
  quizStarted.value = false
  quizCompleted.value = false
  currentQuestionIndex.value = 0
  selectedAnswer.value = null
  answers.value = {}
  elapsedTime.value = 0
}

// 组件卸载时清理计时器
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
/* 自定义样式 */
</style>