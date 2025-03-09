import DOMPurify from 'dompurify';
import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

// 配置 marked 使用 highlight.js 进行代码高亮
marked.setOptions({
  highlight: (code, lang) => {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
    return hljs.highlight(code, { language }).value;
  },
  langPrefix: 'hljs-', // 与 highlight.js 的样式类名保持一致
});

const ALLOWED_TAGS = [
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'pre', 'code', 'span', 'div',
  'p', 'br', 'em', 'strong', 'ul', 'ol', 'li'
];

const ALLOWED_ATTR = [
  'class',         // 保留 class 属性用于语法高亮
  'data-language'  // 保留语言信息
];

export const renderMarkdown = (content: string) => {
  const rawHtml = marked(content);
  let tempHtml = DOMPurify.sanitize(rawHtml, {
    ALLOWED_TAGS,
    ALLOWED_ATTR,
    FORBID_ATTR: ['style', 'onerror'],
    ALLOW_DATA_ATTR: false,
    USE_PROFILES: {
      html: true,
      svg: false,
      svgFilters: false,
      mathMl: false,
    }
  });
  console.log(tempHtml);
  return tempHtml;
};