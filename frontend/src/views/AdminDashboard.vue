<template>
  <div class="admin-dashboard">
    <div class="admin-header">
      <h2>管理员后台</h2>
      <button class="logout-btn" @click="logout">退出登录</button>
    </div>
    <div class="admin-menu">
      <button :class="{active: tab==='books'}" @click="tab='books'">书籍管理</button>
      <button :class="{active: tab==='users'}" @click="tab='users'">用户管理</button>
      <button :class="{active: tab==='recharge'}" @click="tab='recharge'">充值审核</button>
      <button :class="{active: tab==='announcements'}" @click="tab='announcements'">公告管理</button>
      <button :class="{active: tab==='stats'}" @click="tab='stats'">数据统计</button>
    </div>
    <div class="admin-content">
      <BookManager v-if="tab==='books'" />
      <UserManager v-if="tab==='users'" />
      <RechargeManager v-if="tab==='recharge'" />
      <AnnouncementManager v-if="tab==='announcements'" />
      <StatsPanel v-if="tab==='stats'" />
    </div>
  </div>
</template>

<script>
import BookManager from './BookManager.vue'
import UserManager from './UserManager.vue'
import RechargeManager from './RechargeManager.vue'
import StatsPanel from './StatsPanel.vue'
import AnnouncementManager from './AnnouncementManager.vue'
export default {
  name: 'AdminDashboard',
  components: { BookManager, UserManager, RechargeManager, StatsPanel, AnnouncementManager },
  data() {
    return { tab: 'books' }
  },
  mounted() {
    // 可加身份校验，防止普通用户直接访问
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (!user.is_admin && user.role !== 'admin') {
      this.$router.push('/login')
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 900px;
  margin: 60px auto;
  background: #fffbe6;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 40px 32px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.logout-btn {
  background: #fff;
  color: #a67c00;
  border: 1px solid #e0c97f;
  border-radius: 5px;
  padding: 8px 18px;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.logout-btn:hover {
  background: #d4a017;
  color: #fff;
}
.admin-menu {
  display: flex;
  gap: 18px;
  margin-bottom: 32px;
  justify-content: center;
}
.admin-menu button {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 5px;
  padding: 10px 28px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.admin-menu button.active, .admin-menu button:hover {
  background: #d4a017;
  color: #fff;
}
.admin-content {
  background: #fdf6e3;
  border-radius: 8px;
  min-height: 300px;
  padding: 32px 24px;
}
</style> 