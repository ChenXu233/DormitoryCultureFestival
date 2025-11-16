# 寝室桌面搭建模块

## 功能概述

寝室桌面搭建模块是一个交互式的桌面设计工具，允许用户通过拖拽方式搭建个性化的寝室桌面布局。

## 核心功能

### 1. 元素选择与拖拽
- **分类元素库**：提供学习用品、电子设备、生活用品、装饰物品等分类
- **拖拽操作**：支持从元素面板拖拽元素到桌面画布
- **实时预览**：拖拽过程中实时显示元素位置

### 2. 桌面元素操作
- **移动**：拖拽元素到桌面任意位置
- **旋转**：支持元素旋转（0-360度）
- **缩放**：支持元素大小缩放（50%-200%）
- **层级控制**：置顶/置底元素层级
- **删除**：移除不需要的元素

### 3. 背景定制
- **预设背景**：提供木质、白色、黑色、蓝色等多种桌面背景
- **自定义颜色**：支持自定义背景颜色选择
- **渐变效果**：支持渐变背景设置
- **纹理图案**：可选纹理背景效果

### 4. 保存与分享
- **设计保存**：保存桌面设计到本地存储
- **设计管理**：查看、加载、删除已保存的设计
- **分享链接**：生成可分享的设计链接
- **社交媒体分享**：支持微信、QQ等平台分享
- **图片导出**：将设计导出为图片（需集成html2canvas）

## 技术实现

### 前端架构
- **框架**：Nuxt 3 + Vue 3 + TypeScript
- **样式**：Tailwind CSS
- **状态管理**：Vue Composition API
- **拖拽交互**：原生HTML5 Drag & Drop API

### 组件结构
```
components/
├── DesktopBuilder.vue      # 桌面搭建主组件
├── ElementPanel.vue        # 元素选择面板
├── BackgroundPanel.vue     # 背景选择面板
└── SaveSharePanel.vue      # 保存分享面板

pages/
└── desktop-builder.vue     # 桌面搭建页面
```

### 数据模型
```typescript
interface DesktopElement {
  id: string
  name: string
  icon: string
  category: string
  x: number
  y: number
  rotation: number
  scale: number
  zIndex: number
}

interface Background {
  id: number | string
  name: string
  color: string
  type: 'solid' | 'gradient' | 'pattern'
}

interface DesignData {
  elements: DesktopElement[]
  background: Background
  canvasSize: { width: number; height: number }
}
```

## 使用说明

### 1. 访问页面
- 打开首页，点击"寝室桌面搭建"卡片
- 或直接访问 `/desktop-builder` 路由

### 2. 搭建桌面
1. **选择背景**：在左侧面板选择喜欢的桌面背景
2. **添加元素**：从元素面板拖拽元素到桌面
3. **调整元素**：
   - 拖拽移动元素位置
   - 使用工具栏旋转和缩放
   - 右键菜单进行更多操作
4. **层级管理**：调整元素的前后顺序

### 3. 保存设计
1. 点击顶部"保存与分享"按钮
2. 输入设计名称
3. 点击"保存设计"

### 4. 分享设计
1. 生成分享链接
2. 复制链接或分享到社交媒体
3. 导出为图片（可选）

## 开发说明

### 环境要求
- Node.js 16+
- npm 或 yarn

### 安装依赖
```bash
cd frontend
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

## 扩展功能建议

### 1. 图片导出增强
- 集成html2canvas库实现高质量图片导出
- 支持多种图片格式（PNG、JPG、SVG）
- 自定义导出尺寸和分辨率

### 2. 云端存储
- 用户账户系统
- 云端设计保存和同步
- 设计版本管理

### 3. 模板系统
- 预设桌面模板
- 热门设计推荐
- 模板导入导出

### 4. 高级编辑功能
- 元素分组管理
- 对齐和分布工具
- 网格吸附功能
- 快捷键支持

### 5. 社交功能
- 设计作品展示
- 点赞和评论
- 设计灵感社区

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 性能优化

- 虚拟滚动处理大量元素
- 图片懒加载
- 操作防抖处理
- 内存泄漏预防

## 注意事项

1. 图片导出功能需要额外集成html2canvas库
2. 分享链接功能需要后端支持实现真实链接生成
3. 移动端适配需要额外优化触控交互

## 贡献指南

欢迎提交Issue和Pull Request来改进这个模块！