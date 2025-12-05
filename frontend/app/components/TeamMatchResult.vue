<template>
  <div class="flex flex-col items-center ">
    <div id="certificate-node">
    <!-- 证书主体 (A4 比例) -->
    <div 
      class="a4-page relative bg-white shadow-2xl overflow-hidden transition-transform duration-300"
    >
      <!-- 装饰性外框 -->
      <div class="border-frame"></div>

      <div class="content h-full flex flex-col p-8 relative z-10">
        <!-- 头部区域 -->
        <div class="header text-center mb-5">
          <div class="main-title">Z世代寝室图鉴</div>
          <div class="sub-title">寝室文化节 · 默契度检测报告</div>
        </div>

        <!-- 宿舍信息栏 -->
        <div class="dorm-info-bar flex items-center justify-between mb-6">
          <div class="dorm-input-wrapper flex items-center">
            <span class="text-2xl font-bold text-[#D84315] mr-2">#</span>
            <input 
              v-model="dormNumber" 
              type="text" 
              placeholder="输入寝室号" 
              class="dorm-input text-2xl font-bold text-[#D84315] bg-transparent border-b-2 border-dashed border-[#bbb] focus:outline-none focus:border-[#D84315] w-32 placeholder-gray-300"
            />
          </div>
          <div class="members-wrapper flex items-center gap-2">
            <span 
              v-for="(member, index) in matchResult.participants" 
              :key="member.code"
              class="member-name inline-block"
            >
              {{ member.name || `成员${member.code}` }}
            </span>
          </div>
        </div>

        <!-- 照片区域 (Slot) - 放大并自适应 -->
        <div class="photo-container flex-1 min-h-0 mb-4 relative w-full flex flex-col">
          <slot name="image-upload"></slot>
        </div>

        <!-- 分数与类型 -->
        <div class="score-card flex items-center bg-white border-[3px] border-[#4E342E] rounded-2xl mb-4 shadow-[4px_4px_0px_#4E342E] overflow-hidden shrink-0" style="z-index: 0;">
          <div class="score-left w-1/3 bg-[#4E342E] text-white text-center py-3 flex flex-col justify-center">
            <div class="score-number text-5xl font-black leading-none text-[#F9A825]">
              {{ matchResult.team_compatibility_score }}
            </div>
            <div class="score-label text-[10px] opacity-80 mt-1 tracking-widest font-light">默契度评分</div>
          </div>
          <div class="score-right flex-1 flex items-center px-4 py-2 bg-white justify-between">
            <div class="flex items-center">
              <div class="type-emoji-large text-4xl mr-3 drop-shadow-sm">
                {{ getScoreEmoji(matchResult.team_compatibility_score) }}
              </div>
              <div class="type-content flex flex-col items-start">
                <div class="type-title text-xl font-extrabold text-[#3E2723] mb-0.5">
                  {{ matchResult.team_commentary?.title || '默契团队' }}
                </div>
                <div class="type-badge bg-[#D84315] text-white text-[10px] px-2 py-0.5 rounded uppercase font-bold tracking-wider">
                  DORMITORY BOND TYPE
                </div>
              </div>
            </div>
            <!-- 匹配类型图片 -->
            <img 
              v-if="matchResult.team_commentary?.title"
              :src="`特质匹配图片/${matchResult.team_commentary?.title}.jpg`" 
              :alt="matchResult.team_commentary?.title"
              class="h-12 w-12 object-contain rounded-md border border-gray-200 shadow-sm ml-2"
            />
          </div>
        </div>

        <!-- 雷达图与特质 Tags (合并为一行) -->
        <div class="flex flex-row gap-3 mb-4 h-64 shrink-0">
             <!-- 雷达图 -->
             <div class="w-1/2 bg-white/80 border-2 border-[#4E342E] rounded-xl p-1 flex flex-col items-center justify-center relative">
                 <div class="absolute top-0 left-2 -translate-y-1/2 bg-[#4E342E] text-white text-[10px] px-2 py-0.5 rounded">维度分析</div>
                 <client-only>
                   <RadarChart 
                     v-if="teamRadarData" 
                    :multi-radar-data="teamRadarData"
                    :dimension-emojis="matchResult.dimension_emojis"
                    width="93%"
                    :height="270"
                    :lenendbignum1="1"  
                    :lenendbignum2="9"
                    :full-width="true"
                   />
                 </client-only>
             </div>

             <!-- 特质 Tags -->
             <div class="w-1/2 flex flex-col gap-2 justify-between">
                <div 
                  v-for="(traitInfo, dimension) in displayedTraits" 
                  :key="dimension"
                  class="tag-item flex-1 border-2 border-[#4E342E] rounded-xl p-2 flex items-center bg-white/80"
                >
                    <div class="tag-icon text-xl mr-2 w-8 h-8 rounded-full bg-[#FFFDF0] border-2 border-[#4E342E] flex items-center justify-center text-[#3E2723]">
                        {{ matchResult.dimension_emojis?.[dimension] || '🌟' }}
                    </div>
                    <div class="tag-content">
                        <h4 class="text-[10px] text-[#6D4C41] mb-0 uppercase">{{ dimension }}</h4>
                        <span class="text-sm font-extrabold text-[#D84315]">{{ traitInfo.trait }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 评语区域 -->
        <div class="comment-box w-full bg-white/50 border-l-[5px] border-[#D84315] p-4 text-[15px] leading-relaxed text-[#3E2723] italic relative mb-auto">
          <div class="quote-mark absolute top-1 left-2 text-4xl text-[#D84315] opacity-40 font-serif leading-none">“</div>
          <div class="comment-content relative z-10 indent-8">
            {{ matchResult.team_commentary?.commentary || matchResult.team_commentary }}
          </div>
        </div>

        <!-- 底部 -->
        <div class="footer w-full border-t border-[#4E342E]/20 pt-4 mt-4 flex justify-between items-end">
          <div class="organizers flex flex-col gap-1">
            <div class="org-name text-xs font-bold text-[#6D4C41] flex items-center before:content-[''] before:inline-block before:w-1.5 before:h-1.5 before:bg-[#F9A825] before:rounded-full before:mr-2">
              主办：信息科学与工程学院学生会 x CIC计算机信息交流协会
            </div>
          </div>
          <div class="footer-right flex flex-col items-end gap-2">
            <div class="logos flex gap-2">
               <div class="logo-box w-10 h-10 bg-white border border-[#4E342E]/20 rounded-full overflow-hidden p-0.5 flex items-center justify-center">
                 <img src="/logo.jpg" alt="ISE Logo" class="w-full h-full object-contain rounded-full">
               </div>
               <div class="logo-box w-10 h-10 bg-white border border-[#4E342E]/20 rounded-full overflow-hidden p-0.5 flex items-center justify-center">
                 <img src="/cic-logo.png" alt="CIC Logo" class="w-full h-full object-contain rounded-full">
               </div>
            </div>
            <div class="date-str text-[10px] text-[#6D4C41] opacity-70 font-mono">
              生成日期：{{ currentDate }}
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">
      <button 
        class="px-8 py-3 bg-white border-2 border-gray-200 text-gray-600 font-semibold rounded-xl hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800 transition-all duration-200 flex items-center gap-2"
        @click="$emit('reset')"
      >
        <span>🔄</span> 重新匹配
      </button>
      <button
        class="px-8 py-3 bg-[#D84315] text-white font-bold rounded-xl hover:bg-[#bf360c] shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2 transform hover:-translate-y-0.5"
        @click="saveReport"
      >
        <span>💾</span> 保存证书图片
      </button>
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import RadarChart from './RadarChart.vue'
import { toPng } from 'html-to-image'

interface Props {
  matchResult: any
  hasImage?: boolean
}

interface Emits {
  (e: 'reset'): void
}

const props = defineProps<Props>()
defineEmits<Emits>()

const dormNumber = ref('')
const currentDate = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '.')

const saveReport = async () => {
  if (!props.hasImage) {
    alert('请先上传团队合影！')
    return
  }
  if (!dormNumber.value.trim()) {
    alert('请输入寝室号！')
    return
  }

  const node = document.getElementById('certificate-node')
  if (!node) return
  
  try {
    const dataUrl = await toPng(node, { backgroundColor: '#fff' })
    const link = document.createElement('a')
    link.download = `寝室报告_${dormNumber.value}.png`
    link.href = dataUrl
    link.click()
  } catch (error) {
    console.error('Failed to generate image:', error)
    alert('生成图片失败，请重试')
  }
}

const getScoreEmoji = (score: number) => {
  if (score >= 90) return '🌟'
  if (score >= 80) return '✨'
  if (score >= 70) return '🤝'
  if (score >= 60) return '🌱'
  return '🔧'
}

const displayedTraits = computed(() => {
    if (!props.matchResult?.team_trait_analysis?.dominant_traits) return {}
    const traits = props.matchResult.team_trait_analysis.dominant_traits
    const keys = Object.keys(traits).slice(0, 2)
    const result: any = {}
    keys.forEach(k => result[k] = traits[k])
    return result
})

const teamRadarData = computed(() => {
  if (!props.matchResult?.participants || props.matchResult.participants.length === 0) return null
  
  const firstParticipantWithData = props.matchResult.participants.find((p: any) => p.radar_data)
  if (!firstParticipantWithData) return null

  const dimensions = firstParticipantWithData.radar_data.dimensions
  const max_score = firstParticipantWithData.radar_data.max_score

  const colors = ['#D84315', '#F9A825', '#4E342E', '#6D4C41'] 

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
/* 引入证书生成的 CSS 变量和特定样式 */
.a4-page {
    width: 210mm;
    height: 297mm;
    margin: 0 auto;
    background: linear-gradient(160deg, var(--bg-start) 0%, var(--bg-end) 100%);
    color: var(--text-main);
    font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
    
    /* 邻近色配色定义 */
    --bg-start: #FFFDF0;    /* 奶油白 */
    --bg-end: #FFE0B2;      /* 杏仁黄 */
    --border-color: #4E342E;/*以此深咖色为主色调，替代黑色 */
    --accent-1: #D84315;    /* 砖红/深橙 - 强调色 */
    --accent-2: #F9A825;    /* 姜黄 - 辅助色 */
    --text-main: #3E2723;   /* 深褐文字 */
    --text-sub: #6D4C41;    /* 浅褐文字 */
    --white-glass: rgba(255, 255, 255, 0.65); /* 磨砂玻璃白 */

    background: linear-gradient(160deg, var(--bg-start) 0%, var(--bg-end) 100%);
    color: var(--text-main);
    font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
}

.border-frame {
    position: absolute;
    top: 1mm;
    left: 1mm;
    right: 1mm;
    bottom: 1mm;
    border: 6px solid var(--border-color);
    border-radius: 20px;
    z-index: 1;
    pointer-events: none;
}

.main-title {
    font-size: 50px;
    font-weight: 900;
    color: var(--border-color);
    letter-spacing: 3px;
    margin-bottom: 8px;
}

.sub-title {
    font-size: 20px;
    background: var(--border-color);
    color: #fff;
    display: inline-block;
    padding: 4px 16px;
    border-radius: 20px;
    letter-spacing: 2px;
}

.dorm-info-bar {
    background: var(--white-glass);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    padding: 12px 25px;
    box-shadow: 4px 4px 0px rgba(78, 52, 46, 0.1);
}

.members-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 8px;
}

.member-name {
    font-size: 16px;
    color: var(--text-sub);
    background: #fff;
    padding: 4px 12px;
    border-radius: 6px;
    border: 1px solid #e0e0e0;
    font-weight: 600;
    white-space: nowrap;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .a4-page {
        width: 100%;
        height: auto;
        aspect-ratio: auto;
        min-height: auto;
    }
    .border-frame {
        top: 10px; left: 10px; right: 10px; bottom: 10px;
    }
    .content {
        padding: 20px;
    }
    .main-title {
        font-size: 24px;
    }
    .dorm-info-bar {
        flex-direction: column;
        gap: 12px;
        align-items: stretch;
    }
    
    .members-wrapper {
        justify-content: center;
    }
    
    .member-name {
        font-size: 14px;
        padding: 3px 10px;
    }
}
</style>