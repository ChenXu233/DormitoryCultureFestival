// 桌面元素接口定义
export interface DesktopElement {
  id: number | string
  name: string
  icon: string
  x: number
  y: number
  rotation: number
  scale: number
  zIndex: number
  size?: number
  category?: string
  isCabinet?: boolean
  depth?: number
  rotationX?: number
  rotationY?: number
  material?: string
}

// 元素类别接口
export interface ElementCategory {
  id: string
  name: string
}

// 可拖拽元素接口
export interface DraggableElement {
  name: string
  icon: string
  category?: string
  size?: number
  isCabinet?: boolean
  variants?: string[] // 图片变体数组
}

// 右键菜单状态接口
export interface ContextMenuState {
  visible: boolean
  x: number
  y: number
  element: DesktopElement | null
}

// 桌面配置接口
export interface DesktopConfig {
  background: string
  elements: DesktopElement[]
  timestamp: string
}