<template>
  <a-layout class="ai-prob-container">
    <a-layout-header class="header">
      <div class="title">AI 生成概率检测</div>
    </a-layout-header>

    <a-layout-content class="content">
      <a-textarea
        v-model:value="inputText"
        placeholder="输入文本，每行一个"
        :auto-size="{ minRows: 6, maxRows: 10 }"
      />
      <a-button type="primary" @click="analyzeText" :loading="loading" class="analyze-button">
        检测
      </a-button>
      
      <a-list v-if="results.length" :data-source="results" bordered>
        <template #renderItem="{ item }">
          <a-list-item>
            <div class="result-item">
              <div class="text">{{ item.text }}</div>
              <div class="probability">概率: {{ item.probability }}</div>
              <div class="response">AI 响应: {{ item.response }}</div>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </a-layout-content>
  </a-layout>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const inputText = ref('');
const results = ref([]);
const loading = ref(false);

const analyzeText = async () => {
  if (!inputText.value.trim()) return;
  
  loading.value = true;
  try {
    const response = await axios.post('/kenger/ai_prob', { text: inputText.value });
    results.value = response.data.map((res, index) => ({
      text: inputText.value.split('\n')[index],
      probability: res[0].toFixed(2) + '%', // 保留两位小数，并加上百分号
      response: res[1],
    }));
  } catch (error) {
    console.error('Error fetching AI probability:', error);
  } finally {
    loading.value = false;
  }
};

</script>

<style scoped>
.ai-prob-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.header {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  background: #f0f2f5;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.analyze-button {
  margin-top: 10px;
}

.result-item {
  display: flex;
  flex-direction: column;
}

.text {
  font-weight: bold;
}

.probability, .response {
  font-size: 14px;
  color: #555;
}
</style>
