<template>
    <a-row justify="center" align="middle" class="register-container">
      <a-col :span="8">
        <a-card title="注册">
          <a-form
            v-model="registerForm"
            @submit="handleRegister"
          >
            <a-form-item label="用户名" :rules="usernameRules">
              <a-input v-model:value="registerForm.username" placeholder="请输入用户名" />
            </a-form-item>
            <a-form-item label="密码" :rules="passwordRules">
              <a-input-password v-model:value="registerForm.password" placeholder="请输入密码" />
            </a-form-item>
            <a-form-item>
              <a-button type="primary" html-type="submit" block>注册</a-button>
            </a-form-item>
            <a-form-item>
              <a-button @click="goToLogin" type="link" block>已有账号？去登录</a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </a-col>
    </a-row>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { message } from 'ant-design-vue'
  
  const router = useRouter()
  
  const registerForm = ref({
    username: '',
    password: ''
  })
  
  const usernameRules = [
    { required: true, message: '请输入用户名' }
  ]
  
  const passwordRules = [
    { required: true, message: '请输入密码' }
  ]
  
  const handleRegister = async () => {
    if (!registerForm.value.username || !registerForm.value.password) {
      message.error('请填写完整信息！')
      return
    }
  
    try {
      // 使用 fetch 请求替代 axios
      const response = await fetch('/kenger/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',  // 设置请求头
        },
        body: JSON.stringify({
          username: registerForm.value.username,
          password: registerForm.value.password
        })
      });

      // 检查响应状态
      if (!response.ok) {
        // 如果响应状态不是 2xx，会抛出异常
        throw new Error(`登录失败：${response.statusText}`);
      }

      // 解析响应的 JSON 数据
      const data = await response.json();

      // 登录成功，存储 token，并跳转到首页
      const token = data.access_token;
      localStorage.setItem('access_token', token);
      message.success('登录成功！');
      router.push('/');
    } catch (error) {
      // 错误处理
      console.error(error);
      message.error('登录失败：' + error.message);
    }
  }
  
  const goToLogin = () => {
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .register-container {
    height: 100vh;
  }
  </style>