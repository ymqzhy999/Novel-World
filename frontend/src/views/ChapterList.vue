<template>
  <div class="chapter-list-container">
    <div class="chapter-list-title">章节列表</div>
    <ul class="chapter-list-ul">
      <li v-for="(chapter, idx) in chapters" :key="chapter.id">
        <span
          v-if="idx < chapters.length - 10"
          class="chapter-link"
          @click="goToContent(chapter.id)"
        >{{ chapter.title }}</span>
        <span v-else class="chapter-locked">{{ chapter.title }}（需付费解锁）</span>
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  data() { return { chapters: [] } },
  mounted() {
    const novelId = this.$route.params.novelId
    fetch(`/api/novel/${novelId}/chapters/`).then(res => res.json()).then(data => { this.chapters = data })
  },
  methods: {
    goToContent(chapterId) {
      this.$router.push(`/user-home/novel-list/${this.$route.params.novelId}/chapter/${chapterId}`)
    }
  }
}
</script>
<style scoped>
.chapter-list-container {
  max-width: 600px;
  margin: 30px auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px #eee;
  padding: 24px;
}
.chapter-list-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 18px;
  text-align: center;
}
.chapter-list-ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.chapter-list-ul li {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 16px;
  color: #333;
}
.chapter-list-ul li:last-child {
  border-bottom: none;
}
.chapter-link {
  color: #a67c00;
  cursor: pointer;
  text-decoration: underline;
}
.chapter-link:hover {
  color: #d4a017;
}
.chapter-locked {
  color: #aaa;
  font-style: italic;
}
</style> 