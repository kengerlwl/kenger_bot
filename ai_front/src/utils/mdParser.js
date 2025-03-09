import { marked } from 'marked'
import DOMPurify from 'dompurify'

// 配置marked
marked.setOptions({
  breaks: true,
  highlight: (code) => 
    require('highlight.js').highlightAuto(code).value
})

// 安全过滤配置
DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName === 'A') {
    node.setAttribute('target', '_blank')
    node.setAttribute('rel', 'noopener noreferrer')
  }
})

export const safeMarkdown = (content) => {
  return DOMPurify.sanitize(marked.parse(content))
}