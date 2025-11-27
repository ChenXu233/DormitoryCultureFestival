import type { ElementCategory } from '../components/types'

// 预定义的元素类别
export const elementCategories: ElementCategory[] = [
  { id: 'electronics', name: '电子设备' },
  { id: 'study', name: '学习资料' },
  { id: 'tools', name: '小工具' },
  { id: 'daily', name: '生活用品' }
]

// 预定义的可拖拽元素
export const availableElements = [
  // 电子设备 - 电脑套装
  { name: '电脑1', icon: '/桌面程序贴图/电子设备/电脑 (1).png', category: 'electronics' },
  { name: '电脑2', icon: '/桌面程序贴图/电子设备/电脑 (2).png', category: 'electronics' },
  { name: '电脑3', icon: '/桌面程序贴图/电子设备/电脑 (3).png', category: 'electronics' },
  { name: '键盘1', icon: '/桌面程序贴图/电子设备/键盘 (1).png', category: 'electronics' },
  { name: '键盘2', icon: '/桌面程序贴图/电子设备/键盘 (2).png', category: 'electronics' },
  { name: '键盘3', icon: '/桌面程序贴图/电子设备/键盘 (3).png', category: 'electronics' },
  { name: '键盘4', icon: '/桌面程序贴图/电子设备/键盘 (4).png', category: 'electronics' },
  { name: '键盘5', icon: '/桌面程序贴图/电子设备/键盘 (5).png', category: 'electronics' },
  { name: '键盘6', icon: '/桌面程序贴图/电子设备/键盘 (6).png', category: 'electronics' },
  { name: '鼠标1', icon: '/桌面程序贴图/电子设备/鼠标  (1).png', category: 'electronics' },
  { name: '鼠标2', icon: '/桌面程序贴图/电子设备/鼠标  (2).png', category: 'electronics' },
  { name: '鼠标3', icon: '/桌面程序贴图/电子设备/鼠标  (3).png', category: 'electronics' },
  { name: '鼠标4', icon: '/桌面程序贴图/电子设备/鼠标  (4).png', category: 'electronics' },
  { name: '鼠标5', icon: '/桌面程序贴图/电子设备/鼠标  (5).png', category: 'electronics' },
  { name: '鼠标6', icon: '/桌面程序贴图/电子设备/鼠标  (6).png', category: 'electronics' },
  
  // 电子设备 - 移动设备
  { name: '手机1', icon: '/桌面程序贴图/电子设备/手机 (1).png', category: 'electronics' },
  { name: '手机2', icon: '/桌面程序贴图/电子设备/手机 (2).png', category: 'electronics' },
  { name: '手机3', icon: '/桌面程序贴图/电子设备/手机 (3).png', category: 'electronics' },
  { name: '平板1', icon: '/桌面程序贴图/电子设备/平板 (1).png', category: 'electronics' },
  { name: '平板2', icon: '/桌面程序贴图/电子设备/平板 (2).png', category: 'electronics' },
  { name: '平板3', icon: '/桌面程序贴图/电子设备/平板 (3).png', category: 'electronics' },
  { name: '平板4', icon: '/桌面程序贴图/电子设备/平板 (4).png', category: 'electronics' },
  
  // 电子设备 - 音频设备
  { name: '耳机1', icon: '/桌面程序贴图/电子设备/耳机 (1).png', category: 'electronics' },
  { name: '耳机2', icon: '/桌面程序贴图/电子设备/耳机 (2).png', category: 'electronics' },
  { name: '耳机3', icon: '/桌面程序贴图/电子设备/耳机 (3).png', category: 'electronics' },
  { name: '耳机4', icon: '/桌面程序贴图/电子设备/耳机 (4).png', category: 'electronics' },
  { name: '耳机5', icon: '/桌面程序贴图/电子设备/耳机 (5).png', category: 'electronics' },
  { name: '耳机6', icon: '/桌面程序贴图/电子设备/耳机 (6).png', category: 'electronics' },
  
  // 学习资料 - 书籍资料
  { name: '书本1', icon: '/桌面程序贴图/学习用品/书本 (1).png', category: 'study' },
  { name: '书本2', icon: '/桌面程序贴图/学习用品/书本 (2).png', category: 'study' },
  { name: '书本3', icon: '/桌面程序贴图/学习用品/书本 (3).png', category: 'study' },
  
  // 学习资料 - 书写工具
  { name: '铅笔1', icon: '/桌面程序贴图/学习用品/铅笔 (1).png', category: 'study' },
  { name: '铅笔2', icon: '/桌面程序贴图/学习用品/铅笔 (2).png', category: 'study' },
  { name: '铅笔3', icon: '/桌面程序贴图/学习用品/铅笔 (3).png', category: 'study' },
  { name: '铅笔4', icon: '/桌面程序贴图/学习用品/铅笔 (4).png', category: 'study' },
  { name: '铅笔5', icon: '/桌面程序贴图/学习用品/铅笔 (5).png', category: 'study' },
  { name: '钢笔1', icon: '/桌面程序贴图/学习用品/钢笔 (1).png', category: 'study' },
  { name: '钢笔2', icon: '/桌面程序贴图/学习用品/钢笔 (2).png', category: 'study' },
  { name: '钢笔3', icon: '/桌面程序贴图/学习用品/钢笔 (3).png', category: 'study' },
  { name: '钢笔4', icon: '/桌面程序贴图/学习用品/钢笔 (4).png', category: 'study' },
  { name: '钢笔5', icon: '/桌面程序贴图/学习用品/钢笔 (5).png', category: 'study' },
  
  // 学习资料 - 笔记用品
  { name: '便利贴1', icon: '/桌面程序贴图/学习用品/便利贴(1).png', category: 'study' },
  { name: '便利贴2', icon: '/桌面程序贴图/学习用品/便利贴(2).png', category: 'study' },
  { name: '便利贴3', icon: '/桌面程序贴图/学习用品/便利贴(3).png', category: 'study' },
  { name: '便利贴4', icon: '/桌面程序贴图/学习用品/便利贴(4).png', category: 'study' },
  
  // 小工具 - 办公工具
  { name: '美工刀1', icon: '/桌面程序贴图/实用小物件/美工刀 (1).png', category: 'tools' },
  { name: '美工刀2', icon: '/桌面程序贴图/实用小物件/美工刀 (2).png', category: 'tools' },
  { name: '美工刀3', icon: '/桌面程序贴图/实用小物件/美工刀 (3).png', category: 'tools' },
  { name: '美工刀4', icon: '/桌面程序贴图/实用小物件/美工刀 (4).png', category: 'tools' },
  { name: '订书机1', icon: '/桌面程序贴图/实用小物件/订书机 (1).png', category: 'tools' },
  { name: '订书机2', icon: '/桌面程序贴图/实用小物件/订书机 (2).png', category: 'tools' },
  { name: '订书机3', icon: '/桌面程序贴图/实用小物件/订书机 (3).png', category: 'tools' },
  { name: '订书机4', icon: '/桌面程序贴图/实用小物件/订书机 (4).png', category: 'tools' },
  { name: '纸巾1', icon: '/桌面程序贴图/生活用品/纸巾 (1).png', category: 'tools' },
  { name: '纸巾2', icon: '/桌面程序贴图/生活用品/纸巾 (2).png', category: 'tools' },
  { name: '纸巾3', icon: '/桌面程序贴图/生活用品/纸巾 (3).png', category: 'tools' },
  { name: '纸巾4', icon: '/桌面程序贴图/生活用品/纸巾 (4).png', category: 'tools' },
  
  // 小工具 - 存储设备
  { name: 'U盘1', icon: '/桌面程序贴图/实用小物件/U盘 (1).png', category: 'tools' },
  { name: 'U盘2', icon: '/桌面程序贴图/实用小物件/U盘 (2).png', category: 'tools' },
  { name: 'U盘3', icon: '/桌面程序贴图/实用小物件/U盘 (3).png', category: 'tools' },
  { name: 'U盘4', icon: '/桌面程序贴图/实用小物件/U盘 (4).png', category: 'tools' },
  { name: 'U盘5', icon: '/桌面程序贴图/实用小物件/U盘 (5).png', category: 'tools' },

  // 小工具 - 时间工具
  { name: '计算器1', icon: '/桌面程序贴图/实用小物件/计算器 (1).png', category: 'tools' },
  { name: '计算器2', icon: '/桌面程序贴图/实用小物件/计算器 (2).png', category: 'tools' },
  { name: '计算器3', icon: '/桌面程序贴图/实用小物件/计算器 (3).png', category: 'tools' },
  { name: '计算器4', icon: '/桌面程序贴图/实用小物件/计算器 (4).png', category: 'tools' },
  { name: '计算器5', icon: '/桌面程序贴图/实用小物件/计算器 (5).png', category: 'tools' },
  { name: '闹钟1', icon: '/桌面程序贴图/实用小物件/闹钟 (1).png', category: 'tools' },
  { name: '闹钟2', icon: '/桌面程序贴图/实用小物件/闹钟 (2).png', category: 'tools' },
  { name: '闹钟3', icon: '/桌面程序贴图/实用小物件/闹钟 (3).png', category: 'tools' },
  { name: '闹钟4', icon: '/桌面程序贴图/实用小物件/闹钟 (4).png', category: 'tools' },
  { name: '闹钟5', icon: '/桌面程序贴图/实用小物件/闹钟 (5).png', category: 'tools' },
  { name: '闹钟6', icon: '/桌面程序贴图/实用小物件/闹钟 (6).png', category: 'tools' },
  { name: '闹钟7', icon: '/桌面程序贴图/实用小物件/闹钟 (7).png', category: 'tools' },
  
  // 生活用品 - 照明用品
  { name: '台灯1', icon: '/桌面程序贴图/生活用品/台灯 (1).png', category: 'daily' },
  { name: '台灯2', icon: '/桌面程序贴图/生活用品/台灯 (2).png', category: 'daily' },
  { name: '台灯3', icon: '/桌面程序贴图/生活用品/台灯 (3).png', category: 'daily' },
  { name: '台灯4', icon: '/桌面程序贴图/生活用品/台灯 (4).png', category: 'daily' },
  { name: '台灯5', icon: '/桌面程序贴图/生活用品/台灯（5）.png', category: 'daily' },
  
  // 生活用品 - 饮水用品
  { name: '水杯1', icon: '/桌面程序贴图/生活用品/水杯 (1).png', category: 'daily' },
  { name: '水杯2', icon: '/桌面程序贴图/生活用品/水杯 (2).png', category: 'daily' },
  { name: '水杯3', icon: '/桌面程序贴图/生活用品/水杯 (3).png', category: 'daily' },
  { name: '水杯4', icon: '/桌面程序贴图/生活用品/水杯 (4).png', category: 'daily' },
  
  // 生活用品 - 个人物品
  { name: '薯片1', icon: '/桌面程序贴图/生活用品/薯片 (1).png', category: 'daily' },
  { name: '薯片2', icon: '/桌面程序贴图/生活用品/薯片 (2).png', category: 'daily' },
  { name: '薯片3', icon: '/桌面程序贴图/生活用品/薯片 (3).png', category: 'daily' },
  { name: '蛋糕1', icon: '/桌面程序贴图/生活用品/蛋糕 (1).png', category: 'daily' },
  { name: '蛋糕2', icon: '/桌面程序贴图/生活用品/蛋糕 (2).png', category: 'daily' },
  { name: '蛋糕3', icon: '/桌面程序贴图/生活用品/蛋糕 (3).png', category: 'daily' },
  { name: '镜子1', icon: '/桌面程序贴图/生活用品/镜子 (1).png', category: 'daily' },
  { name: '镜子2', icon: '/桌面程序贴图/生活用品/镜子 (2).png', category: 'daily' },
  { name: '镜子3', icon: '/桌面程序贴图/生活用品/镜子 (3).png', category: 'daily' },
  { name: '镜子4', icon: '/桌面程序贴图/生活用品/镜子 (4).png', category: 'daily' },
  { name: '镜子5', icon: '/桌面程序贴图/生活用品/镜子 (5).png', category: 'daily' },
  { name: '镜子6', icon: '/桌面程序贴图/生活用品/镜子 (6).png', category: 'daily' },
  { name: '镜子7', icon: '/桌面程序贴图/生活用品/镜子 (7).png', category: 'daily' },
  { name: '口红1', icon: '/桌面程序贴图/生活用品/口红 (1).png', category: 'daily' },
  { name: '口红2', icon: '/桌面程序贴图/生活用品/口红 (2).png', category: 'daily' },
  { name: '口红3', icon: '/桌面程序贴图/生活用品/口红 (3).png', category: 'daily' },
  { name: '口红4', icon: '/桌面程序贴图/生活用品/口红 (4).png', category: 'daily' },
  { name: '口红5', icon: '/桌面程序贴图/生活用品/口红 (5).png', category: 'daily' },
  { name: '口红6', icon: '/桌面程序贴图/生活用品/口红 (6).png', category: 'daily' },
  { name: '口红7', icon: '/桌面程序贴图/生活用品/口红 (7).png', category: 'daily' },
  { name: '粉饼1', icon: '/桌面程序贴图/生活用品/粉饼 (1).png', category: 'daily' },
  { name: '粉饼2', icon: '/桌面程序贴图/生活用品/粉饼 (2).png', category: 'daily' },
  { name: '粉饼3', icon: '/桌面程序贴图/生活用品/粉饼 (3).png', category: 'daily' }
]
