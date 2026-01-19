<template>
  <div class="comment-section">
    <h3>评论区</h3>
    <div v-if="comments.length === 0" class="no-comment">暂无评论</div>
    <div v-for="c in comments" :key="c.id" class="comment-item">
      <span class="comment-user">{{ c.user_name }}</span>
      <span class="comment-time">{{ formatTime(c.created_at) }}</span>
      <div class="comment-content">{{ c.content }}</div>
      <button class="reply-btn" @click="replyTo(c)">回复</button>
      <div v-if="c.replies && c.replies.length" class="reply-list">
        <div v-for="r in c.replies" :key="r.id" class="reply-item">
          <span class="comment-user">{{ r.user_name }}</span>
          <span class="comment-time">{{ formatTime(r.created_at) }}</span>
          <div class="comment-content">{{ r.content }}</div>
          <button class="reply-btn" @click="replyTo(r)">回复</button>
        </div>
      </div>
    </div>
    <form class="comment-form" @submit.prevent="submitComment">
      <textarea v-model="commentInput" :placeholder="replyToComment ? '回复 @' + replyToComment.user_name : '写下你的评论...'" required></textarea>
      <button type="submit">{{ replyToComment ? '回复' : '发表评论' }}</button>
      <button v-if="replyToComment" type="button" @click="cancelReply" class="cancel-reply">取消回复</button>
    </form>
    <div v-if="showSuccess" class="comment-success">评论成功！</div>
  </div>
</template>

<script>
export default {
  name: 'CommentSection',
  props: {
    novelId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      comments: [],
      commentInput: '',
      showSuccess: false,
      replyToComment: null
    }
  },
  mounted() {
    this.loadComments()
  },
  methods: {
    async loadComments() {
      try {
        const res = await fetch(`/api/novel/${this.novelId}/comments/`)
        this.comments = await res.json()
      } catch (e) {
        console.log('加载评论失败:', e)
      }
    },
    replyTo(comment) {
      this.replyToComment = comment
      this.commentInput = ''
    },
    cancelReply() {
      this.replyToComment = null
      this.commentInput = ''
    },
    async submitComment() {
      const user = localStorage.getItem('user')
      if (!user) {
        alert('请先登录')
        return
      }
      try {
        const userRes = await fetch('/api/user/info/')
        const userInfo = await userRes.json()
        const body = {
          user_id: userInfo.id,
          content: this.commentInput,
          parent: this.replyToComment ? this.replyToComment.id : null
        }
        const res = await fetch(`/api/novel/${this.novelId}/comments/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        })
        const data = await res.json()
        if (data.success) {
          this.commentInput = ''
          this.replyToComment = null
          this.showSuccess = true
          this.loadComments()
          setTimeout(() => { this.showSuccess = false }, 1200)
        }
      } catch (e) {
        console.log('发表评论失败:', e)
      }
    },
    formatTime(t) {
      return t ? t.replace('T', ' ').slice(0, 19) : ''
    }
  }
}
</script>

<style scoped>
.comment-section {
  margin-top: 48px;
  background: #fdf6e3;
  border-radius: 8px;
  box-shadow: 0 2px 8px #e0c97f;
  padding: 24px 18px 18px 18px;
}

.comment-section h3 {
  font-size: 20px;
  color: #a67c00;
  margin-bottom: 18px;
}

.no-comment {
  color: #aaa;
  text-align: center;
  margin-bottom: 12px;
}

.comment-item {
  border-bottom: 1px solid #f0e6c2;
  padding: 10px 0 6px 0;
}

.reply-list {
  margin-left: 32px;
  margin-top: 6px;
  border-left: 2px solid #f0e6c2;
  padding-left: 12px;
}

.reply-item {
  margin-bottom: 8px;
}

.reply-btn {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 4px;
  padding: 2px 10px;
  font-size: 13px;
  margin-left: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.reply-btn:hover {
  background: #d4a017;
  color: #fff;
}

.cancel-reply {
  margin-left: 12px;
  background: #eee;
  color: #a67c00;
  border: none;
  border-radius: 4px;
  padding: 2px 10px;
  font-size: 13px;
  cursor: pointer;
}

.comment-user {
  color: #d4a017;
  font-weight: bold;
  margin-right: 12px;
}

.comment-time {
  color: #b3a16c;
  font-size: 13px;
}

.comment-content {
  margin-top: 4px;
  font-size: 15px;
  color: #5b4a1b;
  line-height: 1.5;
}

.comment-form {
  margin-top: 20px;
}

.comment-form textarea {
  width: 100%;
  min-height: 80px;
  padding: 12px;
  border: 1px solid #e0c97f;
  border-radius: 5px;
  font-size: 14px;
  background: #fffbe6;
  resize: vertical;
  margin-bottom: 12px;
}

.comment-form button {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 5px;
  padding: 8px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.comment-form button:hover {
  background: #f5e6b2;
}

.comment-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 5px;
  padding: 8px 12px;
  text-align: center;
  margin-top: 12px;
  font-size: 14px;
}
</style> 