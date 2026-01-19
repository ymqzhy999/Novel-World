<template>
  <nav class="navbar">
    <router-link to="/user-home/novel-list" class="nav-item">首页</router-link>
    <router-link to="/user-home/account-info" class="nav-item">账号信息</router-link>
    <router-link to="/user-home/novel-list" class="nav-item">小说栏目</router-link>
    <router-link to="/user-home/bookshelf" class="nav-item">我的书架</router-link>
    <router-link to="/user-home/recharge" class="nav-item">充值中心</router-link>
    <router-link to="/user-home/messages" class="nav-item">消息/通知</router-link>
    <span class="nav-right">
      <span class="username">{{ username }}</span>
      <a href="#" @click.prevent="logout" class="logout">退出登录</a>
    </span>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      username: this.getUsername()
    }
  },
  methods: {
    getUsername() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.username || '未登录'
      } catch {
        return '未登录'
      }
    },
    logout() {
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  background: linear-gradient(90deg, #f7f3e8 0%, #f5ecd7 100%);
  padding: 0 32px;
  height: 54px;
  border-radius: 10px 10px 0 0;
  box-shadow: 0 2px 8px #e0c97f;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}
.nav-item {
  margin-right: 32px;
  color: #a67c00;
  text-decoration: none;
  font-size: 17px;
  font-weight: 500;
  transition: color 0.2s;
  padding: 0 4px 2px 4px;
  border-bottom: 2px solid transparent;
}
.nav-item.router-link-exact-active,
.nav-item.router-link-active {
  color: #d4a017;
  border-bottom: 2px solid #d4a017;
  background: #fdf6e3;
  border-radius: 4px 4px 0 0;
}
.nav-item:hover {
  color: #d4a017;
}
.nav-right {
  margin-left: auto;
  display: flex;
  align-items: center;
}
.username {
  color: #888;
  margin-right: 18px;
  font-size: 15px;
}
.logout {
  color: #a67c00;
  cursor: pointer;
  text-decoration: underline;
  font-size: 15px;
  margin-left: 8px;
}
.logout:hover {
  color: #d4a017;
}
</style> 