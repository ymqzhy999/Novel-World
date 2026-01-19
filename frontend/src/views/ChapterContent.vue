<template>
  <div class="chapter-content-container">
    <div class="chapter-title">
      {{ chapter.title }}
      <button class="collect-btn" @click="toggleBookshelf">
        {{ isCollected ? '已收藏' : '收藏' }}
      </button>
    </div>
    <div class="chapter-body" v-html="chapter.content"></div>
    <div class="chapter-nav">
      <button @click="goPrev" :disabled="!hasPrev">上一章</button>
      <button @click="goNext" :disabled="!hasNext">下一章</button>
    </div>
    <CommentSection :novel-id="$route.params.novelId" />
  </div>
</template>

<script>
import CommentSection from '../components/CommentSection.vue'

export default {
  components: {
    CommentSection
  },
  data() {
    return {
      chapter: {},
      chapters: [],
      chapterIdx: 0,
      isCollected: false
    }
  },
  async mounted() {
    const novelId = this.$route.params.novelId
    const chapterId = parseInt(this.$route.params.chapterId)
    // 获取所有章节
    const res = await fetch(`/api/novel/${novelId}/chapters/`)
    this.chapters = await res.json()
    this.chapterIdx = this.chapters.findIndex(c => c.id === chapterId)
    this.chapter = this.chapters[this.chapterIdx] || {}
    // 记录历史浏览
    this.addHistory(novelId)
    // 检查是否已收藏
    await this.checkBookshelf()
  },
  computed: {
    hasPrev() {
      return this.chapterIdx > 0
    },
    hasNext() {
      return this.chapterIdx < this.chapters.length - 1
    }
  },
  methods: {
    async addHistory(novelId) {
      try {
        const userObj = JSON.parse(localStorage.getItem('user') || '{}')
        const userId = userObj.id
        await fetch('/api/history/add/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, keyword: novelId })
        })
      } catch (e) {
        console.log('记录历史失败:', e)
      }
    },
    goPrev() {
      if (this.hasPrev) {
        const prevId = this.chapters[this.chapterIdx - 1].id
        this.$router.push(`/user-home/novel-list/${this.$route.params.novelId}/chapter/${prevId}`)
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    goNext() {
      if (this.hasNext) {
        const nextId = this.chapters[this.chapterIdx + 1].id
        this.$router.push(`/user-home/novel-list/${this.$route.params.novelId}/chapter/${nextId}`)
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    async checkBookshelf() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      if (!user.id) return
      const res = await fetch(`/api/bookshelf/check/?user_id=${user.id}&novel_id=${this.$route.params.novelId}`)
      const data = await res.json()
      this.isCollected = data.collected
    },
    async toggleBookshelf() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      if (!user.id) {
        alert('请先登录')
        return
      }
      const url = this.isCollected ? '/api/bookshelf/remove/' : '/api/bookshelf/add/'
      await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id, novel_id: this.$route.params.novelId })
      })
      this.isCollected = !this.isCollected
    }
  },
  watch: {
    '$route.params.chapterId': {
      immediate: true,
      handler(newVal) {
        if (this.chapters.length) {
          this.chapterIdx = this.chapters.findIndex(c => c.id === parseInt(newVal))
          this.chapter = this.chapters[this.chapterIdx] || {}
          window.scrollTo({ top: 0, behavior: 'smooth' })
        }
      }
    }
  }
}
</script>

<style scoped>
.chapter-content-container {
  max-width: 700px;
  margin: 40px auto;
  background: #fdf6e3;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 36px 28px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
  color: #5b4a1b;
  min-height: 500px;
}
.chapter-title {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 32px;
  text-align: center;
  letter-spacing: 2px;
  color: #a67c00;
  text-shadow: 1px 1px 0 #fffbe6;
}
.collect-btn {
  margin-left: 18px;
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 4px;
  padding: 4px 16px;
  cursor: pointer;
  font-size: 15px;
}
.collect-btn:hover {
  background: #d4a017;
  color: #fff;
}
.chapter-body {
  font-size: 1.18em;
  line-height: 2.2;
  text-indent: 2em;
  word-break: break-all;
  min-height: 400px;
}
.chapter-nav {
  margin-top: 40px;
  text-align: center;
}
.chapter-nav button {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 5px;
  padding: 8px 24px;
  margin: 0 16px;
  font-size: 1em;
  cursor: pointer;
  transition: background 0.2s;
}
.chapter-nav button:disabled {
  background: #f5e6b2;
  color: #b3a16c;
  cursor: not-allowed;
}
.chapter-nav button:hover:not(:disabled) {
  background: #f5e6b2;
}
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
}
.comment-form {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.comment-form textarea {
  width: 100%;
  min-height: 60px;
  border: 1px solid #e0c97f;
  border-radius: 5px;
  padding: 8px;
  font-size: 15px;
  background: #fffbe6;
  margin-bottom: 8px;
  resize: vertical;
}
.comment-form button {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 5px;
  padding: 6px 18px;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s;
}
.comment-form button:hover {
  background: #f5e6b2;
}
.comment-success {
  color: #2e7d32;
  background: #e6ffe6;
  border: 1px solid #b2dfdb;
  border-radius: 5px;
  padding: 6px 18px;
  margin-top: 10px;
  text-align: center;
  font-size: 15px;
}
</style>
