<template>
  <div class="bg-white rounded-3xl shadow-xl overflow-hidden mt-8 transition-all duration-300 hover:shadow-2xl">
    <!-- 顶部装饰条 -->
    <div class="h-2 bg-gradient-to-r from-green-400 via-blue-500 to-purple-500"></div>

    <div class="p-8 md:p-10">
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-green-50 rounded-full mb-6 animate-bounce-slow">
          <span class="text-4xl">🎉</span>
        </div>
        
        <h2 class="text-3xl font-bold text-gray-800 mb-2 tracking-tight">
          团队匹配报告
        </h2>
        <p class="text-gray-500">
          探索你们的团队化学反应 🧪
        </p>
      </div>
      
      <slot name="image-upload"></slot>
      
      <!-- 核心匹配度展示 -->
      <div class="max-w-2xl mx-auto mb-12">
        <div class="relative overflow-hidden bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl p-8 text-white shadow-lg transform transition hover:scale-[1.02] duration-300">
          <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white opacity-10 rounded-full blur-xl"></div>
          <div class="absolute bottom-0 left-0 -mb-4 -ml-4 w-32 h-32 bg-white opacity-10 rounded-full blur-xl"></div>
          
          <div class="relative z-10 text-center">
            <div class="text-lg font-medium opacity-90 mb-2">💖 团队默契指数</div>
            <div class="text-6xl md:text-7xl font-black tracking-tighter mb-2 drop-shadow-sm">
              {{ matchResult.team_compatibility_score }}<span class="text-3xl md:text-4xl align-top">%</span>
            </div>
            <div class="inline-block px-4 py-1 bg-white/20 rounded-full text-sm backdrop-blur-sm">
              {{ getScoreLabel(matchResult.team_compatibility_score) }}
            </div>
          </div>
        </div>
        
        <!-- 团队画像卡片 -->
        <div class="mt-8 bg-white border border-gray-100 rounded-2xl shadow-sm overflow-hidden">
          <div class="md:flex">
            <div class="md:w-1/3 bg-gray-50 flex items-center justify-center p-6">
               <img 
                :src="`特质匹配图片/${matchResult.team_commentary?.title}.jpg`" 
                :alt="matchResult.team_commentary?.title || '团队特质'"
                class="w-full h-auto max-h-48 object-contain rounded-lg shadow-md transform hover:rotate-2 transition duration-300"
              />
            </div>
            <div class="md:w-2/3 p-6 flex flex-col justify-center">
              <div class="flex items-center gap-2 mb-3">
                <span class="text-2xl">🔍</span>
                <h3 class="text-xl font-bold text-gray-800">
                  {{ matchResult.team_commentary?.title || '团队特质分析' }}
                </h3>
              </div>
              <p class="text-gray-600 leading-relaxed text-justify">
                {{ matchResult.team_commentary?.commentary || matchResult.team_commentary }}
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 数据可视化区域 -->
      <div class="grid grid-cols-1 gap-8 mb-12">
        <!-- 雷达图 -->
        <div class="bg-gray-50 rounded-2xl p-6 border border-gray-100">
          <h3 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <span>📊</span> 维度分布
          </h3>
             <client-only>
               <RadarChart 
                 v-if="teamRadarData" 
                 :multi-radar-data="teamRadarData"
                 :dimension-emojis="matchResult.dimension_emojis"
                 max-width="100%"
               />
             </client-only>
        </div>

        <!-- 核心特质 -->
        <div class="bg-gray-50 rounded-2xl p-6 border border-gray-100">
          <h3 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <span>🌟</span> 团队基因
          </h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
              v-for="(traitInfo, dimension) in matchResult.team_trait_analysis?.dominant_traits" 
              :key="dimension"
              class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div class="text-xs text-gray-500 mb-1 uppercase tracking-wider flex items-center gap-1">
                <span>{{ matchResult.dimension_emojis?.[dimension] }}</span>
                {{ dimension }}
              </div>
              <div class="font-bold text-lg text-gray-800 mb-1">{{ traitInfo.trait }}</div>
              <div class="w-full bg-gray-100 rounded-full h-1.5 mt-2">
                <div 
                  class="bg-green-500 h-1.5 rounded-full" 
                  :style="{ width: `${(traitInfo.count / 4) * 100}%` }"
                ></div>
              </div>
              <div class="text-right text-xs text-gray-400 mt-1">{{ traitInfo.count }}/4 成员</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 成员详情 -->
      <div class="mb-12">
        <h3 class="text-2xl font-bold text-gray-800 mb-8 flex items-center justify-center gap-2">
          <span>👥</span> 成员档案
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          <div
            v-for="(member, index) in matchResult.participants" 
            :key="member.code" 
            class="group bg-white border border-gray-200 rounded-2xl p-5 hover:border-blue-300 hover:shadow-lg transition-all duration-300"
          >
            <div class="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center text-lg">
                {{ ['🐶', '🐱', '🦊', '🐼'][index % 4] }}
              </div>
              <div>
                <h4 class="font-bold text-gray-800">{{ member.name || `成员${member.code}` }}</h4>
                <div class="text-xs text-gray-500">ID: {{ member.code }}</div>
              </div>
            </div>
            
            <div class="space-y-3">
              <div 
                v-for="(trait, dimension) in member.primary_traits" 
                :key="dimension"
                class="flex justify-between items-center text-sm"
              >
                <span class="text-gray-500 flex items-center gap-1">
                  <span class="text-xs">{{ matchResult.dimension_emojis?.[dimension] }}</span>
                  {{ dimension }}
                </span>
                <span class="font-medium text-gray-700 bg-gray-50 px-2 py-0.5 rounded text-xs group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                  {{ trait }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8 border-t border-gray-100">
        <button 
          class="px-8 py-3 bg-white border-2 border-gray-200 text-gray-600 font-semibold rounded-xl hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800 transition-all duration-200 flex items-center gap-2"
          @click="$emit('reset')"
        >
          <span>🔄</span> 重新匹配
        </button>
          <button
            class="px-8 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all duration-200 flex items-center gap-2"
            @click="saveReport"
          >
            <span>💾</span> 保存报告
          </button>
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import RadarChart from './RadarChart.vue'

import { toPng } from 'html-to-image'

interface Props {
  matchResult: any
}

interface Emits {
  (e: 'reset'): void
}

const props = defineProps<Props>()
defineEmits<Emits>()

const saveReport = async () => {
  const node = document.querySelector('.bg-white.rounded-3xl.shadow-xl') as HTMLElement
  if (!node) return
  
  try {
    const dataUrl = await toPng(node, { backgroundColor: '#fff' })
    const link = document.createElement('a')
    link.download = '团队匹配报告.png'
    link.href = dataUrl
    link.click()
  } catch (error) {
    console.error('Failed to generate image:', error)
  }
}

const getScoreLabel = (score: number) => {
  if (score >= 90) return '天作之合 🌟'
  if (score >= 80) return '相见恨晚 ✨'
  if (score >= 70) return '志同道合 🤝'
  if (score >= 60) return '求同存异 🌱'
  return '磨合期 🔧'
}

const teamRadarData = computed(() => {
  if (!props.matchResult?.participants || props.matchResult.participants.length === 0) return null
  
  // Assuming all participants have the same dimensions in their radar_data
  // We take dimensions from the first participant who has radar_data
  const firstParticipantWithData = props.matchResult.participants.find((p: any) => p.radar_data)
  if (!firstParticipantWithData) return null

  const dimensions = firstParticipantWithData.radar_data.dimensions
  const max_score = firstParticipantWithData.radar_data.max_score

  const colors = ['#22c55e', '#3b82f6', '#a855f7', '#f97316'] // Green, Blue, Purple, Orange

  const datasets = props.matchResult.participants.map((p: any, index: number) => ({
    label: p.name || `成员${p.code}`,
    scores: p.radar_data?.scores || [],
    color: colors[index % colors.length]
  }))

  return {
    dimensions,
    datasets,
    max_score
  }
})
</script>

<style scoped>
.animate-bounce-slow {
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 100% {
    transform: translateY(-5%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
</style>
