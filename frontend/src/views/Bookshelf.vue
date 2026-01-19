<template>
  <div class="bookshelf-container">
    <h2>我的书架</h2>
    <div v-if="books.length === 0" class="empty-bookshelf">
      <p>书架空空如也，快去收藏喜欢的小说吧！</p>
      <router-link to="/user-home/novel-list" class="browse-link">浏览小说</router-link>
    </div>
    <div v-else class="books-grid">
      <div v-for="book in books" :key="book.id" class="book-card" @click="goToNovel(book.novel_id)">
        <img :src="book.cover_url" :alt="book.title" class="book-cover" />
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">作者：{{ book.author }}</p>
          <p class="book-progress">已读：{{ book.read_chapters }}/{{ book.total_chapters }}章</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: []
    }
  },
  mounted() {
    this.loadBookshelf()
  },
  methods: {
    async loadBookshelf() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        if (!user.id) {
          this.books = []
          console.log('未登录或未获取到用户ID，书架为空。')
          return
        }
        console.log('User ID for bookshelf:', user.id);
        const res = await fetch(`/api/bookshelf/?user_id=${user.id}`)
        this.books = await res.json()
      } catch (e) {
        console.log('加载书架失败:', e)
        this.books = []
      }
    },
    goToNovel(novelId) {
      this.$router.push(`/user-home/novel-list/${novelId}`)
    }
  }
}
</script>

<style scoped>
.bookshelf-container {
  max-width: 800px;
  margin: 40px auto;
  background: #fffbe6;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 36px 32px 28px 32px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}

.bookshelf-container h2 {
  font-size: 24px;
  color: #a67c00;
  margin-bottom: 24px;
  text-align: center;
}

.empty-bookshelf {
  text-align: center;
  padding: 60px 20px;
}

.empty-bookshelf p {
  color: #888;
  font-size: 16px;
  margin-bottom: 20px;
}

.browse-link {
  display: inline-block;
  background: #e6c97a;
  color: #5b4a1b;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  transition: background 0.2s;
}

.browse-link:hover {
  background: #f5e6b2;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.book-card {
  background: #fdf6e3;
  border: 1px solid #e0c97f;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}

.book-card:hover {
  box-shadow: 0 4px 12px #d4a017;
  transform: translateY(-2px);
}

.book-cover {
  max-width: 100%;
  max-height: 120px;
  object-fit: contain;
  background: #fff;
  border-radius: 4px;
  margin-bottom: 12px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.book-title {
  font-size: 16px;
  color: #a67c00;
  margin-bottom: 8px;
  font-weight: bold;
}

.book-author {
  font-size: 14px;
  color: #888;
  margin-bottom: 6px;
}

.book-progress {
  font-size: 12px;
  color: #666;
}
</style> 