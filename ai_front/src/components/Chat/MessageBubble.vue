<template>
  <div :class="['message-bubble', item.role]">
    <div class="message-content" v-html="item.htmlContent"></div>
    <div class="message-time">{{ formatTime(item.time) }}</div>
  </div>
</template>

<script setup>
defineProps({
  item: Object,
  roleMap: Object,
  formatTime: Function
})
</script>

<style scoped>
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
</style>