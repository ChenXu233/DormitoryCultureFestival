import { ref, reactive, onMounted, onUnmounted } from 'vue'
import type { DesktopElement, ContextMenuState } from '../components/types'
// @ts-ignore
import html2canvas from 'html2canvas'

export function useDesktopBuilder(initialElements: DesktopElement[] = [], initialBackground: string) {
  // 状态
  const desktopCanvasRef = ref<any>(null)
  const elements = ref<DesktopElement[]>(initialElements)
  const selectedElement = ref<DesktopElement | null>(null)
  const elementHovered = ref<string | null>(null)
  const draggingElement = ref<DesktopElement | null>(null)
  const dragOffset = ref({ x: 0, y: 0 })
  const background = ref(initialBackground)
  const activeCategory = ref('electronics')
  // 宿舍号（用于文件命名与图片水印）
  const dormNumber = ref<string>('')
  const contextMenu = reactive<ContextMenuState>({
    visible: false,
    x: 0,
    y: 0,
    element: null
  })
  
  // 拖拽状态
  let isDragging = false

  // 元素面板相关函数
  const onElementDragStart = (element: any, event: DragEvent) => {
    if (event.dataTransfer) {
      event.dataTransfer.setData('text/plain', JSON.stringify(element))
      event.dataTransfer.effectAllowed = 'copy'
    }
  }

  const onElementClick = (element: any) => {
    // 点击元素面板中的元素时，自动添加到桌面中间
    if (desktopCanvasRef.value) {
      const canvas = desktopCanvasRef.value.getCanvas()
      if (canvas) {
        const rect = canvas.getBoundingClientRect()
        const x = rect.width / 2 - 50
        const y = rect.height / 2 - 50
        
        const newElement: DesktopElement = {
          ...element,
          id: Date.now(),
          x: Math.max(0, Math.min(x, rect.width - 100)),
          y: Math.max(0, Math.min(y, rect.height - 100)),
          rotation: 0,
          scale: 1,
          zIndex: elements.value.length + 1,
          size: element.size || 2,
          depth: element.isCabinet ? 50 : 20,
          rotationX: 0,
          rotationY: 0,
          material: element.isCabinet ? 'wood' : 'plastic'
        }
        
        elements.value.push(newElement)
      }
    }
  }

  // 拖拽相关函数
  const onDragOver = (event: DragEvent) => {
    event.preventDefault()
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'copy'
    }
  }

  const onDrop = (event: DragEvent) => {
    event.preventDefault()
    
    if (event.dataTransfer) {
      const elementData = JSON.parse(event.dataTransfer.getData('text/plain'))
      
      if (desktopCanvasRef.value) {
        const canvas = desktopCanvasRef.value.getCanvas()
        if (canvas) {
          const rect = canvas.getBoundingClientRect()
          const x = event.clientX - rect.left - 50
          const y = event.clientY - rect.top - 50
          
          // 创建新元素实例
          const newElement: DesktopElement = {
            ...elementData,
            id: Date.now(),
            x: Math.max(0, Math.min(x, rect.width - 100)),
            y: Math.max(0, Math.min(y, rect.height - 100)),
            rotation: 0,
            scale: 1,
            zIndex: elements.value.length + 1,
            size: elementData.size || 2,
            // 初始深度根据是否是柜子设定
            depth: elementData.isCabinet ? 50 : 20,
            rotationX: 0,
            rotationY: 0,
            material: elementData.isCabinet ? 'wood' : 'plastic'
          }
          
          elements.value.push(newElement)
        }
      }
    }
  }

  const onDrag = (event: MouseEvent) => {
    if (isDragging && draggingElement.value && desktopCanvasRef.value) {
      const canvas = desktopCanvasRef.value.getCanvas()
      if (canvas) {
        const rect = canvas.getBoundingClientRect()
        const x = event.clientX - dragOffset.value.x
        const y = event.clientY - dragOffset.value.y
        
        draggingElement.value.x = Math.max(0, Math.min(x, rect.width - 50))
        draggingElement.value.y = Math.max(0, Math.min(y, rect.height - 50))
      }
    }
  }

  const startDrag = (element: DesktopElement, event: MouseEvent) => {
    event.preventDefault()
    isDragging = true
    draggingElement.value = element
    
    dragOffset.value.x = event.clientX - element.x
    dragOffset.value.y = event.clientY - element.y
    
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', stopDrag)
    window.addEventListener('mouseleave', stopDrag)
  }

  const stopDrag = () => {
    isDragging = false
    draggingElement.value = null
    document.removeEventListener('mousemove', onDrag)
    document.removeEventListener('mouseup', stopDrag)
    window.removeEventListener('mouseleave', stopDrag)
  }

  // 取消选择元素
  const deselectElement = () => {
    selectedElement.value = null
    contextMenu.visible = false
  }

  // 右键菜单
  const showContextMenu = (event: MouseEvent, element: DesktopElement) => {
    event.preventDefault()
    contextMenu.visible = true
    contextMenu.x = event.clientX
    contextMenu.y = event.clientY
    contextMenu.element = element
  }

  // 编辑元素
  const editElement = () => {
    if (contextMenu.element) {
      selectedElement.value = contextMenu.element
      contextMenu.visible = false
    }
  }

  // 删除元素
  const deleteElement = () => {
    if (contextMenu.element) {
      elements.value = elements.value.filter(
        el => el.id !== contextMenu.element!.id
      )
      contextMenu.visible = false
      selectedElement.value = null
    }
  }

  // 复制元素
  const duplicateElement = () => {
    if (contextMenu.element) {
      const original = contextMenu.element
      const newElement: DesktopElement = {
        ...original,
        id: Date.now(),
        x: original.x + 20,
        y: original.y + 20,
        zIndex: elements.value.length + 1,
        // 复制3D属性
        depth: original.depth || 20,
        rotationX: original.rotationX || 0,
        rotationY: original.rotationY || 0,
        material: original.material || 'plastic'
      }
      elements.value.push(newElement)
      contextMenu.visible = false
    }
  }

  // 旋转元素
  const rotateElement = (angle: number) => {
    if (contextMenu.element) {
      contextMenu.element.rotation = (contextMenu.element.rotation + angle) % 360
      contextMenu.visible = false
    }
  }

  // 层级控制
  const bringToFront = () => {
    if (contextMenu.element) {
      const maxZIndex = Math.max(...elements.value.map(el => el.zIndex))
      contextMenu.element.zIndex = maxZIndex + 1
      contextMenu.visible = false
    }
  }

  const sendToBack = () => {
    if (contextMenu.element) {
      const minZIndex = Math.min(...elements.value.map(el => el.zIndex))
      contextMenu.element.zIndex = Math.max(1, minZIndex - 1)
      contextMenu.visible = false
    }
  }

  // 清空桌面
  const clearDesktop = () => {
    if (confirm('确定要清空桌面吗？此操作不可撤销！')) {
      elements.value = []
      selectedElement.value = null
      contextMenu.visible = false
    }
  }

  // 保存配置
  const saveDesktop = () => {
    const config = {
      background: background.value,
      elements: elements.value,
      dormNumber: dormNumber.value,
      timestamp: new Date().toISOString()
    }
    
    localStorage.setItem('desktop-config', JSON.stringify(config))
    
    // 显示成功提示
    alert('桌面配置已保存！')
    return config
  }

  // 下载图片
  const downloadImage = async () => {
    if (typeof window !== 'undefined') {
      try {
        console.log('开始生成图片...');

        if (desktopCanvasRef.value) {
          const canvas = desktopCanvasRef.value.getCanvas()
          console.log('获取到canvas元素:', canvas);
          if (canvas) {
            // 临时添加宿舍号水印
            let watermarkEl: HTMLDivElement | null = null
            if (dormNumber.value) {
              watermarkEl = document.createElement('div')
              watermarkEl.textContent = `宿舍号：${dormNumber.value}`
              watermarkEl.style.position = 'absolute'
              watermarkEl.style.left = '47.8%'
              watermarkEl.style.top = '34px'
              watermarkEl.style.transform = 'translateX(-50%)'
              watermarkEl.style.fontSize = '24px'
              watermarkEl.style.fontWeight = '600'
              watermarkEl.style.fontFamily = 'cursive'
              watermarkEl.style.color = '#222'
              watermarkEl.style.zIndex = '9999'
              watermarkEl.style.pointerEvents = 'none'
              watermarkEl.style.textShadow = '0 2px 4px rgba(0,0,0,0.3)'
              canvas.appendChild(watermarkEl)
            }
            

            const htmlCanvas = await html2canvas(canvas, {
              scale: 2, // 提高清晰度
              useCORS: true,
              allowTaint: true,
              logging: false,
              backgroundColor: null, // 保持透明背景
              removeContainer: true,
              onclone: (clonedDoc: Document) => {
                // 在克隆的文档中移除所有oklch颜色
                const allElements = clonedDoc.querySelectorAll('*');
                allElements.forEach(el => {
                  const htmlEl = el as HTMLElement;
                  const computedStyle = window.getComputedStyle(htmlEl);

                  // 检查并替换背景色
                  if (computedStyle.backgroundColor && computedStyle.backgroundColor.includes('oklch')) {
                    htmlEl.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                  }

                  // 检查并替换文字颜色
                  if (computedStyle.color && computedStyle.color.includes('oklch')) {
                    htmlEl.style.color = '#333333';
                  }

                  // 检查并替换边框颜色
                  if (computedStyle.borderColor && computedStyle.borderColor.includes('oklch')) {
                    htmlEl.style.borderColor = '#cccccc';
                  }
                });
              }
            });

            // 生成后移除水印 DOM
            if (watermarkEl) {
              watermarkEl.remove()
            }

            console.log('图片生成成功');

            // 创建下载链接
            const link = document.createElement('a');
            const dateStr = new Date().toLocaleDateString()
            const baseName = dormNumber.value ? `宿舍_${dormNumber.value}_桌面设计_${dateStr}` : `桌面设计_${dateStr}`
            link.download = `${baseName}.png`;
            link.href = htmlCanvas.toDataURL('image/png');
            link.click();
            console.log('图片下载链接创建完成');
          } else {
            console.error('无法获取canvas元素');
            alert('无法获取桌面画布，请重试！');
          }
        } else {
          console.error('desktopCanvasRef为空');
          alert('桌面画布组件未准备好，请重试！');
        }
      } catch (error) {
        console.error('下载图片失败:', error);
        alert('导出图片失败，请稍后重试！');
      }
    }
  }

  // 点击其他地方关闭右键菜单
  const closeContextMenu = (event: MouseEvent) => {
    if (contextMenu.visible) {
      contextMenu.visible = false
    }
  }

  // 生命周期
  onMounted(() => {
    document.addEventListener('click', closeContextMenu)
    
    // 加载保存的配置
    const savedConfig = localStorage.getItem('desktop-config')
    if (savedConfig) {
      try {
        const config = JSON.parse(savedConfig)
        elements.value = config.elements || []
        // 为已保存的元素添加3D属性
        elements.value.forEach(el => {
          if (!el.depth) el.depth = 20
          if (el.isCabinet && !el.depth) el.depth = 50
          if (el.rotationX === undefined) el.rotationX = 0
          if (el.rotationY === undefined) el.rotationY = 0
        })
      } catch (e) {
        console.error('加载配置失败', e)
      }
    }
  })

  onUnmounted(() => {
    document.removeEventListener('click', closeContextMenu)
    window.removeEventListener('mouseleave', stopDrag)
  })

  return {
    desktopCanvasRef,
    elements,
    selectedElement,
    elementHovered,
    draggingElement,
    background,
    activeCategory,
    dormNumber,
    contextMenu,
    onElementDragStart,
    onElementClick,
    onDragOver,
    onDrop,
    startDrag,
    deselectElement,
    showContextMenu,
    editElement,
    deleteElement,
    duplicateElement,
    rotateElement,
    bringToFront,
    sendToBack,
    clearDesktop,
    saveDesktop,
    downloadImage
  }
}
