/**
 * 图片上传到图床的组合式函数
 * 简化版：直接使用 Base64 编码
 */

export const useImageUpload = () => {
  const uploading = ref(false)
  const uploadProgress = ref(0)

  /**
   * 将图片转换为 Base64 DataURL
   * @param file 图片文件
   * @returns Base64 DataURL
   */
  const uploadImage = async (file: File): Promise<string> => {
    uploading.value = true
    uploadProgress.value = 0

    try {
      // 直接转换为 Base64
      const base64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        
        reader.onprogress = (e) => {
          if (e.lengthComputable) {
            uploadProgress.value = Math.round((e.loaded / e.total) * 100)
          }
        }
        
        reader.onload = () => {
          resolve(reader.result as string)
        }
        
        reader.onerror = () => {
          reject(new Error('图片读取失败'))
        }
        
        reader.readAsDataURL(file)
      })

      uploadProgress.value = 100
      console.log('✅ 图片已转换为 Base64')
      return base64
    } catch (error) {
      console.error('❌ Base64 转换失败:', error)
      throw new Error('图片处理失败，请检查图片格式和大小')
    } finally {
      uploading.value = false
    }
  }

  return {
    uploading,
    uploadProgress,
    uploadImage
  }
}
