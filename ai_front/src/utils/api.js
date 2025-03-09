import { safeMarkdown } from '@/utils/mdParser'
import debounce from 'lodash.debounce';
import { nextTick } from 'vue';  // 导入 Vue 的 nextTick


// 在 api.js 中导入 renderMarkdown
import { renderMarkdown } from '@/utils/markdown';  // 根据你的路径来修改
export const chatAPI = {
  stream: async (payload, aiMessage) => {
    const response = await fetch('/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-G0483zq1XMOa0XAriQSMb5uDo6npYFNnWUPt7zgk3ouemcaI'
      },
      body: JSON.stringify({
        model: payload.model,
        messages: payload.messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        stream: true
      })
    })

    const reader = response.body.getReader()
    let done = false
    let buffer = ''
    let tempContent = ''

    // 创建防抖更新函数
    const debouncedUpdate = debounce(async () => {
      aiMessage.content = tempContent
      aiMessage.htmlContent = renderMarkdown(tempContent)
      await nextTick()
      // scrollToBottom()
    }, 150, { maxWait: 500 })

    try {
      while (!done) {
        const { value, done: chunkDone } = await reader.read()
        done = chunkDone
        
        if (value) {
          buffer += new TextDecoder().decode(value, { stream: true })
          
          // 优化分包处理逻辑
          const chunks = buffer.split('\n\n')
          buffer = chunks.pop() || '' // 保留未完成的数据

          for (const chunk of chunks) {
            const lines = chunk.split('\n').filter(line => {
              const text = line.replace(/^data: /, '').trim()
              return text !== '' && text !== '[DONE]'
            })

            for (const line of lines) {
              try {
                const data = JSON.parse(line.replace(/^data: /, ''))
                const content = data?.choices?.[0]?.delta?.content || ''
                
                // 累积内容并触发更新
                if (content) {
                  tempContent += content
                  
                  // 触发防抖更新（每50字符或maxWait时触发）
                  if (tempContent.length % 5 === 0) {
                    debouncedUpdate()
                  }
                }
              } catch (error) {
                console.error('解析错误:', error)
              }
            }
          }
        }

        // 最终更新确保内容完整
        if (done) {
          debouncedUpdate.cancel() // 取消未执行的防抖
          aiMessage.content = tempContent
          aiMessage.htmlContent = renderMarkdown(tempContent)
          await nextTick()
          // scrollToBottom()
        }
      }
    } catch (error) {
      console.error('流处理错误:', error)
      // 确保最终状态更新
      aiMessage.content = tempContent
      aiMessage.htmlContent = renderMarkdown(tempContent)
    }
  },


  normal: async (payload) => {
    const response = await fetch('/kenger/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_OPENAI_API_KEY'
      },
      body: JSON.stringify({
        model: payload.model,
        messages: payload.messages.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      })
    })
    return response.json()
  }
}