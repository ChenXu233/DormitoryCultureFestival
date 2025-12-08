/**
 * AI 图生图功能的组合式函数
 */
import CONFIG from '../config/config'

export interface AIImageGenerationOptions {
  model?: string
  prompt: string
  imageUrl: string
  size?: '1K' | '2K' | '4K'
  watermark?: boolean
}

export const useAIImageGeneration = () => {
  const generating = ref(false)
  const error = ref<string | null>(null)

  /**
   * 调用后端 AI 图生图 API
   * @param options 生成选项
   * @returns 生成的图片 URL (Blob URL)
   */
  const generateImage = async (options: AIImageGenerationOptions): Promise<string> => {
    const {
      model = 'doubao-seedream-4-0-250828',
      prompt,
      imageUrl,
      size = '2K',
      watermark = false
    } = options

    try {
      generating.value = true
      error.value = null

      // 确保 API_BASE_URL 不以 / 结尾
      const baseUrl = CONFIG.apiBaseUrl.replace(/\/$/, '')
      
      const response = await fetch(`${baseUrl}/api/ai/generate-image`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model,
          prompt,
          image_url: imageUrl,
          size,
          watermark
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API 请求失败: ${response.status}`)
      }

      // 直接获取图片 Blob
      const blob = await response.blob()
      return URL.createObjectURL(blob)

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '图片生成失败'
      error.value = errorMessage
      console.error('AI 图生图失败:', err)
      throw new Error(errorMessage)
    } finally {
      generating.value = false
    }
  }

  /**
   * 生成团队合影的艺术化版本
   * @param imageUrl 原始图片 URL
   * @param teamName 团队名称（可选）
   * @returns 生成的图片 URL
   */
  const generateTeamPhoto = async (imageUrl: string, teamName?: string): Promise<string> => {
    const prompts = [
      '将这张团队合影转换为温馨的插画风格，保持人物特征，添加温暖的色调和宿舍文化节的氛围',
      '生成一张充满活力和青春气息的团队合影，保留原图构图，增强色彩饱和度，添加宿舍文化节的装饰元素',
      '将团队合影优化为专业证件照风格，保持自然表情，优化光线和背景',
      '创作一张艺术化的团队合影，采用温暖的色调，添加青春活力的元素，体现团队凝聚力'
    ]

    // 随机选择一个 prompt 或根据团队名称定制
    const prompt = teamName 
      ? `为"${teamName}"团队生成一张充满活力的合影照片，优化光线和色彩，添加温馨的宿舍文化氛围`
      : prompts[Math.floor(Math.random() * prompts.length)]

    return await generateImage({
      prompt: prompt ?? '',
      imageUrl,
      size: '2K',
      watermark: false
    })
  }

  return {
    generating,
    error,
    generateImage,
    generateTeamPhoto
  }
}
