/**
 * AI 图生图的预设风格配置
 */

export interface AIStylePreset {
  id: string
  name: string
  description: string
  icon: string
  prompt: string
  negativePrompt: string
  aspectRatio?: string
  style?: string
  strength?: number
}

export const AI_STYLE_PRESETS: AIStylePreset[] = [
  {
    id: 'cosmic',
    name: '宇宙星空风',
    description: '手绘插画风格，星空与星座图案，米色背景',
    icon: '🌌',
    negativePrompt: 'extra people, crowd, background characters, photorealistic, 3d render, realistic lighting, shadows, multiple faces, distorted anatomy, ugly, deformed, bad hands, text, watermark, signature, frame, border, other colors, gradient background',
    prompt: 'hand-drawn illustration of the EXACT SAME 4 individuals from uploaded photo, identical facial features and body proportions, stylized cartoon line art, vibrant uniform BEIGE (#FFF8DC) background with hand-drawn constellation patterns and simple planet outlines, no shading, flat color design, character sheet style, minimal decorative elements, no other humans or characters, pure beige backdrop, anime-inspired but not Japanese style, distinctive cosmic theme markers',
    aspectRatio: '16:9',
    style: 'raw',
    strength: 50
  },
  {
    id: 'fantasy',
    name: '异世界奇幻风',
    description: '奇幻 RPG 角色设计，浮空岛与魔法阵，米色背景',
    icon: '🏰',
    negativePrompt: 'extra people, crowd, background characters, photorealistic, 3d render, realistic lighting, shadows, multiple faces, distorted anatomy, ugly, deformed, bad hands, text, watermark, signature, frame, border, other colors, gradient background',
    prompt: 'hand-drawn illustration of the EXACT SAME 4 individuals from uploaded photo, identical appearance and builds, stylized fantasy RPG character designs, vibrant uniform BEIGE (#FFF8DC) background with hand-drawn floating island wireframes and magic circle patterns, line art only, no gradients, flat coloring, character turn-around sheet style, uniform beige tone throughout, distinct magical elements, absolutely no other people, beige canvas only',
    aspectRatio: '16:9',
    strength: 50
  },
  {
    id: 'cyberpunk',
    name: '赛博朋克风',
    description: '赛博朋克角色设计，霓虹电路与全息界面，米色背景',
    icon: '🤖',
    negativePrompt: 'extra people, crowd, background characters, photorealistic, 3d render, realistic lighting, shadows, multiple faces, distorted anatomy, ugly, deformed, bad hands, text, watermark, signature, frame, border, other colors, gradient background',
    prompt: 'hand-drawn illustration of the EXACT SAME 4 individuals from uploaded photo, identical features and body types, stylized cyberpunk character designs, vibrant uniform BEIGE (#FFF8DC) background with hand-drawn neon circuit line patterns and holographic UI wireframes, technical line art, flat color blocks, character design sheet style, strict beige coloration, cybernetic decorative motifs, no other humans present, beige-only backdrop',
    aspectRatio: '16:9',
    strength: 50
  },
  {
    id: 'chinese-ink',
    name: '国风水墨风',
    description: '中国风卡通风格，竹子与山水轮廓，米色宣纸质感',
    icon: '🎋',
    negativePrompt: 'extra people, crowd, background characters, photorealistic, 3d render, realistic lighting, shadows, multiple faces, distorted anatomy, ugly, deformed, bad hands, text, watermark, signature, frame, border, other colors, gradient background',
    prompt: 'hand-drawn illustration of the EXACT SAME 4 individuals from uploaded photo, identical facial structure and stature, stylized Chinese cartoon style, vibrant uniform BEIGE (#FFF8DC) rice-paper textured background with hand-drawn bamboo and mountain contour lines, minimalist line art, flat wash colors, character model sheet format, warm beige tone mandatory, traditional decorative patterns, absolutely no extra people, solid beige background',
    aspectRatio: '4:3',
    style: 'raw',
    strength: 50
  },
  {
    id: 'superhero',
    name: '超级英雄风',
    description: '超级英雄团队设计，漫画爆炸线与动作特效，米色背景',
    icon: '⚡',
    negativePrompt: 'extra people, crowd, background characters, photorealistic, 3d render, realistic lighting, shadows, multiple faces, distorted anatomy, ugly, deformed, bad hands, text, watermark, signature, frame, border, other colors, gradient background',
    prompt: 'hand-drawn illustration of the EXACT SAME 4 individuals from uploaded photo, identical facial features and physiques, stylized superhero character designs, vibrant uniform BEIGE (#FFF8DC) background with hand-drawn comic explosion lines and action effect doodles, bold line art, flat color design, superhero team character sheet, strict beige background color, dynamic decorative marks, absolutely no additional characters, pure beige backdrop',
    aspectRatio: '16:9',
    strength: 50
  }
]

/**
 * 根据 ID 获取风格预设
 */
export const getStylePresetById = (id: string): AIStylePreset | undefined => {
  return AI_STYLE_PRESETS.find(preset => preset.id === id)
}

/**
 * 获取默认风格
 */
export const getDefaultStylePreset = (): AIStylePreset => {
  const preset = AI_STYLE_PRESETS[0]
  if (!preset) {
    throw new Error('No default AI style preset found.')
  }
  return preset
}
