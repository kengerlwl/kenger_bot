import { ref, reactive, computed } from 'vue'
import { safeMarkdown } from '@/utils/mdParser'
import { MODELS } from '@/constants/models'
import { chatAPI } from '@/utils/api'
import { renderMarkdown } from '@/utils/markdown';  // 根据你的路径来修改


export const useChat = () => {
  // 使用 reactive 包装整个 messages 数组，确保其内部对象是响应式的
  const messages = reactive([])

  const selectedModel = ref(MODELS[0].value)
  const streamMode = ref(true)
  const inputMessage = ref('')
  const loading = ref(false)

  const selectedModelLabel = computed(() => {
    return MODELS.find(m => m.value === selectedModel.value)?.label || ''
  })

  const createMessage = (role, content = '') => {
    const newMessage = reactive({
      role,
      content,
      htmlContent: safeMarkdown(content),
      time: Date.now(),
      loading: role === 'assistant'
    })
    messages.push(newMessage)  // 直接将响应式对象添加到 messages 数组
    return newMessage
  }

  const handleSend = async (e) => {
    if (loading.value || !inputMessage.value.trim()) return
    if (e && e.shiftKey) return

    try {
      loading.value = true
      const userMessage = createMessage('user', inputMessage.value.trim())
      const aiMessage = createMessage('assistant')

      inputMessage.value = ''
      console.log(inputMessage)


      if (streamMode.value) {
        await chatAPI.stream({
          model: selectedModel.value,
          messages: [userMessage]
        }, aiMessage)

        // 不需要手动强制更新，直接修改 aiMessage 的内容即可
      } else {
        const response = await chatAPI.normal({
          model: selectedModel.value,
          messages: [userMessage]
        })
        aiMessage.content = response.choices[0].message.content
        aiMessage.htmlContent = renderMarkdown(aiMessage.content)
      }
    } catch (error) {
      console.error('请求错误:', error)
    } finally {
      loading.value = false
    }
  }

  return {
    messages,
    handleSend,
    selectedModel,
    streamMode,
    inputMessage,
    loading,
    models: MODELS,
    roleMap: { user: '你', assistant: 'AI助手' },
    formatTime: (time) => new Date(time).toLocaleTimeString(),
    selectedModelLabel
  }
}