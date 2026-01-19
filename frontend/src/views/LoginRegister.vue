<template>
  <div class="login-register-container">
    <h1 class="app-title">小说阅读平台</h1>
    <div class="tab">
      <span :class="{active: mode==='login'}" @click="mode='login'">登录</span>
      <span :class="{active: mode==='register'}" @click="mode='register'">注册</span>
    </div>
    <form v-if="mode==='login'" @submit.prevent="login">
      <input v-model="loginForm.username" placeholder="用户名" required />
      <input v-model="loginForm.password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
      <p v-if="loginError" class="error">{{ loginError }}</p>
    </form>
    <form v-else @submit.prevent="register">
      <input v-model="registerForm.username" placeholder="用户名" required />
      <input v-model="registerForm.email" placeholder="邮箱" required />
      <input v-model="registerForm.password" type="password" placeholder="密码" required />
      <input v-model="registerForm.confirm" type="password" placeholder="确认密码" required />
      <button type="submit">注册</button>
      <p v-if="registerError" class="error">{{ registerError }}</p>
    </form>
  </div>
</template>

<script>
function validateEmail(email) {
  return /^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$/.test(email)
}
export default {
  data() {
    return {
      mode: 'login',
      loginForm: { username: '', password: '' },
      registerForm: { username: '', email: '', password: '', confirm: '' },
      loginError: '',
      registerError: ''
    }
  },
  methods: {
    async login() {
      this.loginError = ''
      if (!this.loginForm.username || !this.loginForm.password) {
        this.loginError = '请输入用户名和密码'
        return
      }
      try {
        const res = await fetch('/api/user/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.loginForm)
        })
        const data = await res.json()
        if (data.success) {
          localStorage.setItem('user', JSON.stringify(data.user))
          if (data.user.is_admin || data.user.role === 'admin') {
            this.$router.push('/admin')
          } else {
            this.$router.push('/user-home/account-info')
          }
        } else {
          this.loginError = data.msg || '登录失败'
        }
      } catch (e) {
        this.loginError = '网络错误'
      }
    },
    async register() {
      this.registerError = ''
      const { username, email, password, confirm } = this.registerForm
      if (!username || !email || !password || !confirm) {
        this.registerError = '请填写所有字段'
        return
      }
      if (!validateEmail(email)) {
        this.registerError = '邮箱格式不正确'
        return
      }
      if (password.length < 6) {
        this.registerError = '密码长度至少6位'
        return
      }
      if (password !== confirm) {
        this.registerError = '两次输入的密码不一致'
        return
      }
      try {
        const res = await fetch('/api/user/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, email, password })
        })
        const data = await res.json()
        if (data.success) {
          localStorage.setItem('user', data.user.username)
          this.$router.push('/user-home/account-info')
        } else {
          this.registerError = data.msg || '注册失败'
        }
      } catch (e) {
        this.registerError = '网络错误'
      }
    }
  }
}
</script>

<style scoped>
.login-register-container {
  max-width: 350px;
  margin: 80px auto;
  background: #fffbe6;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 36px 32px 28px 32px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}
.app-title {
  font-size: 28px;
  color: #a67c00;
  text-align: center;
  margin-bottom: 28px;
  letter-spacing: 2px;
  text-shadow: 1px 1px 0 #f5ecd7;
}
.tab {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}
.tab span {
  font-size: 18px;
  color: #a67c00;
  margin: 0 24px;
  cursor: pointer;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
  transition: border 0.2s, color 0.2s;
}
.tab .active {
  color: #d4a017;
  border-bottom: 2px solid #d4a017;
}
form {
  display: flex;
  flex-direction: column;
}
input {
  margin-bottom: 16px;
  padding: 8px 12px;
  border: 1px solid #e0c97f;
  border-radius: 5px;
  font-size: 15px;
  background: #fdf6e3;
}
button {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 5px;
  padding: 10px 0;
  font-size: 16px;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s;
}
button:hover {
  background: #f5e6b2;
}
.error {
  color: #d8000c;
  margin-top: 8px;
  font-size: 14px;
  text-align: center;
}
</style> 