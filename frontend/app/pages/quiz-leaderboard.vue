<template>
  <div class="min-h-screen bg-linear-to-br from-purple-50 to-pink-100 py-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">
          室友默契度排行榜
        </h1>
        <p class="text-lg text-gray-600">
          查看个人匹配度排名，看看谁和室友最默契
        </p>
      </div>

      <!-- 排行榜卡片 -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        <!-- 筛选和搜索 -->
        <div class="flex flex-col md:flex-row gap-4 mb-6">
          <div class="flex-1">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="搜索姓名或寝室编号..."
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
          <div class="flex gap-2">
            <button 
              :class="[
                'px-4 py-2 rounded-lg border transition-colors duration-200',
                sortBy === 'match_percentage' 
                  ? 'bg-purple-600 text-white border-purple-600' 
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              ]"
              @click="sortBy = 'match_percentage'; sortOrder = 'desc'"
            >
              按匹配度
            </button>
            <button 
              :class="[
                'px-4 py-2 rounded-lg border transition-colors duration-200',
                sortBy === 'matched_count' 
                  ? 'bg-purple-600 text-white border-purple-600' 
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              ]"
              @click="sortBy = 'matched_count'; sortOrder = 'desc'"
            >
              按匹配题数
            </button>
          </div>
        </div>

        <!-- 排行榜列表 -->
        <div v-if="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"/>
          <p class="text-gray-600 mt-2">加载中...</p>
        </div>

        <div v-else-if="filteredLeaderboard.length === 0" class="text-center py-8">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
          <p class="text-gray-600">暂无排行榜数据</p>
        </div>

        <div v-else class="space-y-4">
          <!-- 前三名特殊样式 -->
          <div 
            v-for="(item, index) in filteredLeaderboard" 
            :key="item.participant_name + item.target_roommate"
            :class="[
              'p-6 rounded-lg border transition-all duration-200',
              index < 3 
                ? 'bg-linear-to-r shadow-lg' 
                : 'bg-white border-gray-200 hover:shadow-md'
            ]"
            :style="{
              background: index < 3 ? getRankGradient(index) : ''
            }"
          >
            <div class="flex items-center justify-between">
              <!-- 排名和用户信息 -->
              <div class="flex items-center space-x-4">
                <!-- 排名徽章 -->
                <div 
                  :class="[
                    'w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg',
                    index === 0 ? 'bg-yellow-500' :
                    index === 1 ? 'bg-gray-400' :
                    index === 2 ? 'bg-orange-500' : 'bg-gray-300'
                  ]"
                >
                  {{ item.rank }}
                </div>
                
                <!-- 用户信息 -->
                <div>
                  <h3 class="text-xl font-semibold" :class="index < 3 ? 'text-white' : 'text-gray-800'">
                    {{ item.participant_name }} ↔ {{ item.target_roommate }}
                  </h3>
                  <p :class="index < 3 ? 'text-white text-opacity-90' : 'text-gray-600'">
                    {{ item.dormitory_id }} 寝室 · {{ item.match_level }}
                  </p>
                </div>
              </div>

              <!-- 匹配度信息 -->
              <div class="text-right">
                <div :class="['text-2xl font-bold', index < 3 ? 'text-white' : 'text-purple-600']">
                  {{ item.match_percentage }}%
                </div>
                <div :class="index < 3 ? 'text-white text-opacity-90' : 'text-gray-600'">
                  匹配度
                </div>
              </div>
            </div>

            <!-- 进度条 -->
            <div class="mt-4">
              <div class="flex justify-between text-sm mb-1" :class="index < 3 ? 'text-white text-opacity-90' : 'text-gray-600'">
                <span>匹配题数</span>
                <span>{{ item.matched_count }} / {{ item.total_questions }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  :class="[
                    'h-2 rounded-full transition-all duration-500',
                    index === 0 ? 'bg-yellow-500' :
                    index === 1 ? 'bg-gray-400' :
                    index === 2 ? 'bg-orange-500' : 'bg-purple-500'
                  ]"
                  :style="{ width: Math.min((item.matched_count / item.total_questions) * 100, 100) + '%' }"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <div class="bg-white rounded-xl shadow-lg p-6 text-center">
          <div class="text-3xl font-bold text-purple-600 mb-2">{{ totalPairs }}</div>
          <div class="text-gray-600">测试组合</div>
        </div>
        <div class="bg-white rounded-xl shadow-lg p-6 text-center">
          <div class="text-3xl font-bold text-green-600 mb-2">{{ averageMatchPercentage }}%</div>
          <div class="text-gray-600">平均匹配度</div>
        </div>
        <div class="bg-white rounded-xl shadow-lg p-6 text-center">
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ highestMatchPercentage }}%</div>
          <div class="text-gray-600">最高匹配度</div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="text-center mt-8 space-x-4">
        <NuxtLink 
          to="/quiz"
          class="inline-block px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors duration-200"
        >
          开始答题
        </NuxtLink>
        <NuxtLink 
          to="/"
          class="inline-block px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          返回首页
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 设置页面元信息
useSeoMeta({
  title: '室友默契度排行榜 - 宿舍文化节',
  description: '查看个人匹配度排名，看看谁和室友最默契'
})

// 页面配置
definePageMeta({
  layout: false
})

// 排行榜数据
const leaderboard = ref<any[]>([])
const loading = ref(true)
const searchQuery = ref('')
const sortBy = ref('match_percentage')
const sortOrder = ref('desc')

// 计算筛选后的排行榜
const filteredLeaderboard = computed(() => {
  let filtered = leaderboard.value
  
  // 搜索筛选
  if (searchQuery.value) {
    filtered = filtered.filter(item => 
      item.participant_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.target_roommate.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.dormitory_id.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  // 排序
  filtered.sort((a, b) => {
    if (sortOrder.value === 'desc') {
      return b[sortBy.value] - a[sortBy.value]
    } else {
      return a[sortBy.value] - b[sortBy.value]
    }
  })
  
  return filtered
})

// 统计信息
const totalPairs = computed(() => leaderboard.value.length)
const averageMatchPercentage = computed(() => {
  if (leaderboard.value.length === 0) return 0
  const total = leaderboard.value.reduce((sum, item) => sum + item.match_percentage, 0)
  return Math.round(total / leaderboard.value.length)
})
const highestMatchPercentage = computed(() => {
  if (leaderboard.value.length === 0) return 0
  return Math.max(...leaderboard.value.map(item => item.match_percentage))
})

// 获取排名渐变背景
const getRankGradient = (index: number) => {
  switch (index) {
    case 0:
      return 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)'
    case 1:
      return 'linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)'
    case 2:
      return 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)'
    default:
      return ''
  }
}

// 加载排行榜数据
const loadLeaderboard = async () => {
  try {
    loading.value = true
    const response = await $fetch('/api/quiz/leaderboard')
    leaderboard.value = response || []
  } catch (error) {
    console.error('加载排行榜失败:', error)
    leaderboard.value = []
  } finally {
    loading.value = false
  }
}

// 页面加载时获取数据
onMounted(() => {
  loadLeaderboard()
})
</script>

<style scoped>
/* 自定义样式 */
</style>