<template>
  <div class="messages-container">
    <h2>消息通知</h2>
    
    <div class="message-tabs">
      <span 
        :class="['tab-item', { active: activeTab === 'announcement' }]"
        @click="activeTab = 'announcement'"
      >
        系统公告
      </span>
      <span 
        :class="['tab-item', { active: activeTab === 'recharge' }]"
        @click="activeTab = 'recharge'"
      >
        充值消息
      </span>
      <span 
        :class="['tab-item', { active: activeTab === 'comment' }]"
        @click="activeTab = 'comment'"
      >
        评论回复
      </span>
    </div>

    <div class="message-list">
      <div v-if="currentMessages.length === 0" class="empty-messages">
        <p>暂无{{ getTabName() }}消息</p>
      </div>
      
      <div 
        v-for="message in currentMessages" 
        :key="message.id"
        :class="['message-item', { unread: !message.read }]"
        @click="markAsRead(message.id)"
      >
        <div class="message-header">
          <span class="message-title">{{ message.title }}</span>
          <span class="message-time">{{ formatTime(message.created_at) }}</span>
        </div>
        <div class="message-content">{{ message.content }}</div>
        <div v-if="message.link" class="message-link">
          <router-link :to="message.link">查看详情</router-link>
        </div>
      </div>
    </div>

    <div class="message-actions">
      <button @click="markAllAsRead" class="action-btn">全部标记为已读</button>
      <button @click="clearReadMessages" class="action-btn">清空已读消息</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'announcement',
      messages: {
        announcement: [],
        recharge: [],
        comment: []
      }
    }
  },
  computed: {
    currentMessages() {
      return this.messages[this.activeTab] || []
    }
  },
  async mounted() {
    // 动态加载系统公告
    try {
      const announcementRes = await fetch('/api/announcements/')
      this.messages.announcement = await announcementRes.json()
    } catch (e) {
      console.error('加载系统公告失败:', e)
    }

    // 动态加载充值消息
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (user.id) {
      try {
        const rechargeRes = await fetch(`/api/user/${user.id}/recharge-messages/`)
        this.messages.recharge = await rechargeRes.json()
      } catch (e) {
        console.error('加载充值消息失败:', e)
      }
      // 动态加载评论回复消息
      try {
        const commentReplyRes = await fetch(`/api/user/${user.id}/comment-replies/`)
        this.messages.comment = await commentReplyRes.json()
      } catch (e) {
        console.error('加载评论回复消息失败:', e)
      }
    }
  },
  methods: {
    getTabName() {
      const names = {
        announcement: '公告',
        recharge: '充值',
        comment: '评论'
      }
      return names[this.activeTab] || ''
    },
    formatTime(timeStr) {
      if (!timeStr) return ''
      const date = new Date(timeStr)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      if (diff < 2592000000) return `${Math.floor(diff / 86400000)}天前`
      
      return date.toLocaleDateString()
    },
    markAsRead(messageId) {
      // 标记已读逻辑，需要后端支持，目前前端模拟
      const message = this.currentMessages.find(m => m.id === messageId)
      if (message) {
        message.read = true
      }
    },
    markAllAsRead() {
      this.currentMessages.forEach(message => {
        message.read = true
      })
    },
    clearReadMessages() {
      const tab = this.activeTab
      this.messages[tab] = this.messages[tab].filter(message => !message.read)
    }
  }
}
</script>

<style scoped>
.messages-container {
  max-width: 700px;
  margin: 40px auto;
  background: #fffbe6;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 36px 32px 28px 32px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}

.messages-container h2 {
  font-size: 24px;
  color: #a67c00;
  margin-bottom: 24px;
  text-align: center;
}

.message-tabs {
  display: flex;
  border-bottom: 2px solid #e0c97f;
  margin-bottom: 24px;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 12px;
  cursor: pointer;
  color: #a67c00;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tab-item:hover {
  background: #f5ecd7;
}

.tab-item.active {
  color: #d4a017;
  border-bottom-color: #d4a017;
  background: #fdf6e3;
}

.empty-messages {
  text-align: center;
  padding: 60px 20px;
  color: #888;
}

.message-item {
  background: #fdf6e3;
  border: 1px solid #e0c97f;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.message-item:hover {
  box-shadow: 0 2px 8px #d4a017;
}

.message-item.unread {
  border-left: 4px solid #d4a017;
  background: #f5ecd7;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.message-title {
  font-weight: bold;
  color: #a67c00;
  font-size: 16px;
}

.message-time {
  color: #888;
  font-size: 14px;
}

.message-content {
  color: #5b4a1b;
  line-height: 1.5;
  margin-bottom: 8px;
}

.message-link {
  text-align: right;
}

.message-link a {
  color: #d4a017;
  text-decoration: none;
  font-size: 14px;
}

.message-link a:hover {
  text-decoration: underline;
}

.message-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  justify-content: center;
}

.action-btn {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.action-btn:hover {
  background: #f5e6b2;
}
</style> 