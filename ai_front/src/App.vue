<!-- <template>
  <div class="app-container">
    <ChatContainer />
  </div>
</template> -->

<template>
  <div id="app">
    <router-view />  <!-- 显示匹配的路由组件 -->
  </div>
</template>


<script setup>
import ChatContainer from '@/components/Chat/ChatContainer.vue'
</script>

<style>
#app {
  height: 100vh;
}
</style>