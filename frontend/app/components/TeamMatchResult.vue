<template>
  <div class="bg-white rounded-xl shadow-lg p-8 mt-8">
    <div class="text-center">
      <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">
        团队匹配结果
      </h2>
      
      <slot name="image-upload"></slot>
      
      <!-- 匹配度展示 -->
      <div class="max-w-md mx-auto mb-6">
        <div class="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-8 text-white">
          <div class="text-5xl font-bold mb-2">{{ matchResult.team_compatibility_score }}%</div>
          <div class="text-lg">团队特质匹配度</div>
        </div>
        
        <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="text-blue-800 font-medium text-center">
              <img 
                :src="`特质匹配图片/${matchResult.team_commentary?.title}.jpg`" 
                :alt="matchResult.team_commentary?.title || '团队特质分析'"
                class="max-w-full h-auto rounded-lg shadow-md max-h-64 object-contain flex justify-center mx-auto mb-4"
              />

            <div class="text-lg font-bold mb-2">{{ matchResult.team_commentary?.title || '团队特质分析' }}</div>
            <div class="text-sm">{{ matchResult.team_commentary?.commentary || matchResult.team_commentary }}</div>
          </div>
        </div>
      </div>
      
      <!-- 特质分析 -->
      <div class="mt-8">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">团队特质分析</h3>
        
        <div class="mb-8 flex justify-center">
           <client-only>
             <RadarChart 
               v-if="teamRadarData" 
               :multi-radar-data="teamRadarData"
               :dimension-emojis="matchResult.dimension_emojis"
               max-width="100%"
             />
           </client-only>
        </div>

        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
              v-for="(traitInfo, dimension) in matchResult.team_trait_analysis?.dominant_traits" 
              :key="dimension"
              class="text-center"
            >
              <div class="text-sm text-gray-600 mb-1">
                <span class="mr-1" v-if="matchResult.dimension_emojis?.[dimension]">{{ matchResult.dimension_emojis[dimension] }}</span>
                {{ dimension }}
              </div>
              <div class="font-medium text-green-600">{{ traitInfo.trait }}</div>
              <div class="text-xs text-gray-500">{{ traitInfo.count }}/4人</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 成员特质展示 -->
      <div class="mt-8">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">成员特质详情</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="member in matchResult.participants" 
            :key="member.code" 
            class="bg-gray-50 border border-gray-200 rounded-lg p-4"
          >
            <h4 class="font-medium text-gray-800 mb-3">{{ member.name || `成员${member.code}` }}</h4>
            <div class="space-y-2">
              <div 
                v-for="(trait, dimension) in member.primary_traits" 
                :key="dimension"
                class="flex justify-between items-center"
              >
                <span class="text-sm text-gray-600">
                  <span class="mr-1" v-if="matchResult.dimension_emojis?.[dimension]">{{ matchResult.dimension_emojis[dimension] }}</span>
                  {{ dimension }}
                </span>
                <span class="font-medium text-green-600">{{ trait }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center mt-8">
        <button 
          class="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors duration-200"
          @click="$emit('reset')"
        >
          重新匹配
        </button>
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import RadarChart from './RadarChart.vue'

interface Props {
  matchResult: any
}

interface Emits {
  (e: 'reset'): void
}

const props = defineProps<Props>()
defineEmits<Emits>()

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
