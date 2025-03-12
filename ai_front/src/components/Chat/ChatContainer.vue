<template>
  <a-layout class="chat-container">
    <!-- 模型选择区 -->
    <a-layout-header class="header">
      <div class="controls">
        <a-select
          v-model:value="selectedModel"
          style="width: 200px"
          :options="models"
          placeholder="选择AI模型"
        />
        <a-switch 
          v-model:checked="streamMode"
          checked-children="流式" 
          un-checked-children="非流式"
        />
      <a-button type="primary" @click="goToAiDetect" style="margin-left: 10px">
        AI 检测
      </a-button>
      </div>
      <div class="model-tips">
        当前模型：{{ selectedModelLabel }} | 模式：{{ streamMode ? '流式' : '非流式' }}
      </div>
    </a-layout-header>

    <!-- 聊天内容区 -->
    <a-layout-content class="content">
      <div ref="messagesEnd" class="messages-container">
        <a-list :data-source="messages">
          <template #renderItem="{ item }">
            <a-list-item :key="item.time">
              <div :class="['message-bubble', item.role]">
                <div class="message-content" v-html="renderMarkdown(item.htmlContent)"></div>
                <div class="message-time">{{ formatTime(item.time) }}</div>
              </div>
            </a-list-item>
          </template>
        </a-list>
      </div>
    </a-layout-content>

    <!-- 输入区 -->
    <a-layout-footer class="footer">
      <div class="input-container">
        <a-textarea

          v-model:value="inputMessage"
          placeholder="输入你的消息..."
          :auto-size="{ minRows: 3, maxRows: 6 }"
          @pressEnter="handleSend"
          :disabled="loading"
        />
        <a-button
          type="primary"
          @click="handleSend"
          :loading="loading"
          class="send-button"
        >
          发送
          <template #icon><SendOutlined /></template>
        </a-button>
      </div>
      <div class="tips">支持Markdown格式 | 按Enter发送，Shift+Enter换行</div>
    </a-layout-footer>
  </a-layout>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { useChat } from '@/hooks/useChat'
import { marked } from 'marked';
import { renderMarkdown } from '@/utils/markdown'; // 修改引入路径
import 'highlight.js/styles/github-dark.css'; // 直接引入样式
import { useRouter } from 'vue-router';
const router = useRouter();

const {
  messages,
  handleSend,
  selectedModel,
  streamMode,
  inputMessage,
  loading,
  models,
  roleMap,
  formatTime,
  selectedModelLabel
} = useChat()

const messagesEnd = ref(null)
const goToAiDetect = () => {
  router.push('/aidetect');
};
// 自动滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesEnd.value) {
      messagesEnd.value.scrollIntoView({ behavior: 'smooth' })
    }
  })
}

// 监听 messages 变化，并自动滚动
watch(messages, () => {
  scrollToBottom()
})


</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.messages-container {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.footer {
  padding: 10px;
  background: #f0f2f5;
}

.send-button {
  margin-left: 10px;
}

.tips {
  font-size: 12px;
  color: #999;
}

.message-bubble {
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 80%;
}

.message-bubble.user {
  background-color: #e0f7fa;
  align-self: flex-start;
}

.message-bubble.assistant {
  background-color: #f1f1f1;
  align-self: flex-end;
}

.message-time {
  font-size: 12px;
  color: #888;
  text-align: right;
}

pre {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

code {
  font-family: monospace;
  font-size: 14px;
  background-color: #000;
}

</style>