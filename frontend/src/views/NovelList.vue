<template>
  <div>
    <div class="novel-search-bar">
      <input v-model="search" placeholder="搜索小说或作者" @input="doSearch" />
    </div>
    <div class="novel-grid">
      <div class="novel-card" v-for="novel in novels" :key="novel.id">
        <img
          :src="novel.cover_url"
          :alt="novel.title"
          class="novel-cover"
          @click="goToChapters(novel.id)"
        />
        <div class="novel-info">
          <h3 @click="goToChapters(novel.id)" class="novel-title">{{ novel.title }}</h3>
          <p class="novel-author">作者：{{ novel.author }}</p>
          <p class="novel-desc">{{ novel.description.slice(0, 40) }}...</p>
        </div>
      </div>
    </div>
    <div v-if="novels.length === 0">暂无数据</div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      novels: [],
      allNovels: [],
      search: ''
    }
  },
  mounted() {
    fetch('/api/novels/')
      .then(res => res.json())
      .then(data => {
        this.novels = data
        this.allNovels = data
      })
  },
  methods: {
    goToChapters(novelId) {
      this.$router.push(`/user-home/novel-list/${novelId}`)
    },
    doSearch() {
      const kw = this.search.trim().toLowerCase()
      if (!kw) {
        this.novels = this.allNovels
      } else {
        this.novels = this.allNovels.filter(novel =>
          novel.title.toLowerCase().includes(kw) ||
          (novel.author && novel.author.toLowerCase().includes(kw))
        )
      }
    }
  }
}
</script>
<style scoped>
.novel-search-bar {
  width: 100%;
  max-width: 400px;
  margin: 0 auto 18px auto;
  display: flex;
  justify-content: center;
}
.novel-search-bar input {
  width: 100%;
  padding: 8px 14px;
  border: 1px solid #e0c97f;
  border-radius: 6px;
  font-size: 16px;
  background: #fdf6e3;
  outline: none;
}
.novel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 28px 18px;
  justify-content: center;
  padding: 24px 0 0 0;
  max-width: 1100px;
  margin: 0 auto;
}
.novel-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px #eee;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.2s;
  cursor: pointer;
  min-height: 280px;
}
.novel-card:hover {
  box-shadow: 0 4px 16px #ccc;
}
.novel-cover {
  width: 120px;
  height: 160px;
  object-fit: cover;
  margin-top: 10px;
  border-radius: 4px;
}
.novel-info {
  padding: 10px 8px 10px 8px;
  width: 100%;
  text-align: center;
}
.novel-title {
  font-size: 16px;
  margin: 6px 0 4px 0;
  color: #333;
  cursor: pointer;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.novel-author {
  font-size: 13px;
  color: #888;
  margin-bottom: 2px;
}
.novel-desc {
  font-size: 12px;
  color: #666;
  height: 32px;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 