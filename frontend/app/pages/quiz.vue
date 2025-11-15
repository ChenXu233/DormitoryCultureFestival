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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            开始答题
          </h2>
          <p class="text-gray-600 mb-6">
            请填写基本信息，然后开始答题。题目将测试你对室友的了解程度。
          </p>

          <!-- 基本信息表单 -->
          <div class="max-w-md mx-auto">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
                  寝室编号
                </label>
                <input 
                  v-model="dormitoryId"
                  type="text" 
                  placeholder="例如：A101"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
                  你的姓名
                </label>
                <input 
                  v-model="participantName"
                  type="text" 
                  placeholder="请输入你的姓名"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
                  目标室友姓名
                </label>
                <input 
                  v-model="targetRoommate"
                  type="text" 
                  placeholder="请输入你要测试默契度的室友姓名"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <button 
              @click="startQuiz"
              :disabled="!dormitoryId || !participantName || !targetRoommate"
              class="w-full mt-6 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
            >
              开始答题
            </button>
          </div>
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
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              @click="selectAnswer(index)"
              :class="[
                'w-full text-left px-4 py-3 border rounded-lg transition-colors duration-200',
                selectedAnswer === index 
                  ? 'border-green-500 bg-green-50 text-green-700' 
                  : 'border-gray-300 hover:border-green-300 hover:bg-green-50'
              ]"
            >
              <div class="flex items-center">
                <span class="w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3"
                      :class="selectedAnswer === index ? 'border-green-500 bg-green-500 text-white' : 'border-gray-400'">
                  {{ String.fromCharCode(65 + index) }}
                </span>
                <span>{{ option }}</span>
              </div>
            </button>
          </div>
        </div>

        <!-- 导航按钮 -->
        <div class="flex justify-between">
          <button
            @click="previousQuestion"
            :disabled="currentQuestionIndex === 0"
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            上一题
          </button>
          
          <button
            @click="nextQuestion"
            :class="[
              'px-6 py-2 rounded-lg font-medium',
              selectedAnswer !== null 
                ? 'bg-green-600 hover:bg-green-700 text-white' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
            :disabled="selectedAnswer === null"
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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            答题完成！
          </h2>
          
          <!-- 匹配度展示 -->
          <div class="max-w-md mx-auto mb-6">
            <div class="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-8 text-white">
              <div class="text-5xl font-bold mb-2">{{ result.match_percentage }}%</div>
              <div class="text-lg">{{ result.match_level }}</div>
            </div>
            
            <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="text-blue-800 font-medium text-center">
                {{ result.analysis }}
              </div>
            </div>
            
            <div class="grid grid-cols-3 gap-4 mt-6 text-center">
              <div>
                <div class="text-2xl font-bold text-green-600">{{ result.matched_count }}</div>
                <div class="text-sm text-gray-600">匹配题数</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-blue-600">{{ result.total_questions }}</div>
                <div class="text-sm text-gray-600">总题数</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-purple-600">{{ formatTime(result.time_spent) }}</div>
                <div class="text-sm text-gray-600">用时</div>
              </div>
            </div>
            
            <div v-if="result.rank" class="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div class="text-yellow-800 font-medium text-center">
                你在排行榜排名：第 {{ result.rank }} 名
              </div>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              @click="restartQuiz"
              class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200"
            >
              重新答题
            </button>
            <NuxtLink 
              to="/quiz-leaderboard"
              class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors duration-200 text-center"
            >
              查看排行榜
            </NuxtLink>
            <NuxtLink 
              to="/"
              class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200 text-center"
            >
              返回首页
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CONFIG from '../config/config'
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
const dormitoryId = ref('')
const participantName = ref('')
const targetRoommate = ref('')

// 题目相关
const questions = ref<any[]>([])
const currentQuestionIndex = ref(0)
const selectedAnswer = ref<number | null>(null)
const answers = ref<Record<number, number>>({})

// 计时器
const elapsedTime = ref(0)
let timer: NodeJS.Timeout | null = null

// 答题结果
const result = ref({
  participant_name: '',
  dormitory_id: '',
  target_roommate: '',
  matched_count: 0,
  total_questions: 0,
  match_percentage: 0,
  match_level: '',
  analysis: '',
  time_spent: 0,
  rank: null as number | null
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
    // 获取题目
    const response = await $fetch(`${API_BASE_URL}/api/quiz/questions?count=5`)
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
  answers.value[currentQuestion.value.id] = index
}

// 上一题
const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedAnswer.value = answers.value[currentQuestion.value.id] ?? null
  }
}

// 下一题
const nextQuestion = async () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    selectedAnswer.value = answers.value[currentQuestion.value.id] ?? null
  } else {
    // 提交答案
    await submitQuiz()
  }
}

// 提交答题
const submitQuiz = async () => {
  try {
    const submission = {
      dormitory_id: dormitoryId.value,
      participant_name: participantName.value,
      target_roommate: targetRoommate.value,
      answers: answers.value,
      submitted_at: new Date().toISOString()
    }

    const response = await $fetch(`${API_BASE_URL}/api/quiz/submit`, {
      method: 'POST',
      body: submission
    })

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
  dormitoryId.value = ''
  participantName.value = ''
  targetRoommate.value = ''
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