<template>
  <div class="account-info-container">
    <h2>账号信息</h2>
    <table class="info-table">
      <tr>
        <th>用户名</th>
        <td>{{ user.username }}</td>
      </tr>
      <tr>
        <th>邮箱</th>
        <td>{{ user.email }}</td>
      </tr>
      <tr>
        <th>余额</th>
        <td>{{ user.balance }}</td>
      </tr>
    </table>

    <div class="history-section">
      <h3>历史浏览</h3>
      <ul v-if="history.length">
        <li v-for="item in history" :key="item.id" @click="goToNovel(item.novel_id)" class="history-item">
          <span>{{ item.novel_title }}</span>
          <span v-if="item.chapter_title"> - {{ item.chapter_title }}</span>
          <span class="history-time">{{ formatTime(item.search_time) }}</span>
        </li>
      </ul>
      <div v-else class="no-data">暂无历史浏览</div>
    </div>

    <div class="comment-section">
      <h3>我的评论</h3>
      <ul v-if="comments.length">
        <li v-for="c in comments" :key="c.id">
          <span class="comment-novel">{{ c.novel_title }}</span>
          <span class="comment-time">{{ formatTime(c.created_at) }}</span>
          <div class="comment-content">{{ c.content }}</div>
        </li>
      </ul>
      <div v-else class="no-data">暂无评论</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {},
      history: [],
      comments: []
    }
  },
  async mounted() {
    // 获取当前登录用户id
    const userObj = JSON.parse(localStorage.getItem('user') || '{}')
    const userId = userObj.id
    // 获取用户信息
    const userRes = await fetch(`/api/user/info/?user_id=${userId}`)
    this.user = await userRes.json()
    // 获取历史浏览
    const historyRes = await fetch(`/api/user/${this.user.id}/history/`)
    this.history = await historyRes.json()
    // 获取评论
    const commentRes = await fetch(`/api/user/${this.user.id}/comments/`)
    this.comments = await commentRes.json()
  },
  methods: {
    formatTime(t) {
      return t ? t.replace('T', ' ').slice(0, 19) : ''
    },
    goToNovel(novelId) {
      this.$router.push(`/user-home/novel-list/${novelId}`)
    }
  }
}
</script>

<style scoped>
.account-info-container {
  max-width: 600px;
  margin: 40px auto;
  background: #fffbe6;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 36px 32px 28px 32px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}
.info-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 32px;
  background: #fdf6e3;
}
.info-table th, .info-table td {
  border: 1px solid #e0c97f;
  padding: 10px 16px;
  text-align: left;
  font-size: 16px;
}
.info-table th {
  background: #f5ecd7;
  color: #a67c00;
  width: 90px;
}
.history-section, .comment-section {
  margin-top: 24px;
}
.history-section h3, .comment-section h3 {
  font-size: 18px;
  color: #a67c00;
  margin-bottom: 10px;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li {
  border-bottom: 1px solid #f0e6c2;
  padding: 8px 0;
  font-size: 15px;
}
.history-time, .comment-time {
  color: #b3a16c;
  font-size: 13px;
  margin-left: 12px;
}
.comment-novel {
  color: #d4a017;
  font-weight: bold;
  margin-right: 8px;
}
.comment-content {
  margin-top: 2px;
  color: #5b4a1b;
}
.no-data {
  color: #aaa;
  text-align: center;
  margin: 8px 0;
}
.history-item {
  cursor: pointer;
  transition: background-color 0.2s;
}
.history-item:hover {
  background-color: #f5ecd7;
  border-radius: 4px;
  padding-left: 8px;
}
</style> 