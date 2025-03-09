import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './App.vue'
import 'ant-design-vue/dist/reset.css'
import './assets/styles/global.css'
import './assets/styles/markdown.css'
import hljs from 'highlight.js'
import router from './router'  // 导入路由配置


// 初始化代码高亮
hljs.configure({
  languages: ['javascript', 'python', 'java', 'bash', 'json', 'html', 'css']
})

const app = createApp(App)
app.use(Antd)
app.use(router)  // 使用路由

app.mount('#app')