<template>
  <div class="stats-panel-container">
    <h3>数据统计</h3>

    <div class="stats-card">
      <h4>充值数据统计</h4>
      <p>总充值金额：<span class="highlight">{{ rechargeStats.total_recharge_amount ? rechargeStats.total_recharge_amount.toFixed(2) : '0.00' }} 书币</span></p>
      <p>充值用户数：<span class="highlight">{{ rechargeStats.recharge_users_count || 0 }} 人</span></p>

      <h5>充值金额排行 (Top 10)</h5>
      <ul v-if="rechargeStats.top_recharge_users && rechargeStats.top_recharge_users.length">
        <li v-for="(user, index) in rechargeStats.top_recharge_users" :key="index">
          {{ user.username }}: {{ user.total_recharge.toFixed(2) }} 书币
        </li>
      </ul>
      <p v-else>暂无充值排行数据。</p>
    </div>

    <div class="stats-card">
      <h4>小说收藏统计</h4>
      <p>总收藏数量：<span class="highlight">{{ novelCollectionStats.total_collections || 0 }} 本</span></p>

      <h5>小说收藏数排行 (Top 10)</h5>
      <ul v-if="novelCollectionStats.top_collected_novels && novelCollectionStats.top_collected_novels.length">
        <li v-for="(novel, index) in novelCollectionStats.top_collected_novels" :key="index">
          《{{ novel.title }}》: {{ novel.collection_count }} 次收藏
        </li>
      </ul>
      <p v-else>暂无收藏排行数据。</p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'StatsPanel',
  data() {
    return {
      rechargeStats: {},
      novelCollectionStats: {}
    }
  },
  async mounted() {
    await this.loadRechargeStats()
    await this.loadNovelCollectionStats()
  },
  methods: {
    async loadRechargeStats() {
      try {
        const res = await fetch('/api/stats/recharge/')
        this.rechargeStats = await res.json()
      } catch (e) {
        console.error('加载充值统计数据失败:', e)
      }
    },
    async loadNovelCollectionStats() {
      try {
        const res = await fetch('/api/stats/novel-collections/')
        this.novelCollectionStats = await res.json()
      } catch (e) {
        console.error('加载小说收藏统计数据失败:', e)
      }
    }
  }
}
</script>

<style scoped>
.stats-panel-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
  color: #5b4a1b;
}

h3 {
  font-size: 24px;
  color: #a67c00;
  margin-bottom: 24px;
  text-align: center;
}

.stats-card {
  background: #fdf6e3;
  border: 1px solid #e0c97f;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(224, 201, 127, 0.5);
  padding: 25px;
  margin-bottom: 30px;
}

.stats-card h4 {
  font-size: 20px;
  color: #a67c00;
  margin-bottom: 15px;
  border-bottom: 2px solid #e0c97f;
  padding-bottom: 8px;
}

.stats-card h5 {
  font-size: 17px;
  color: #d4a017;
  margin-top: 20px;
  margin-bottom: 10px;
}

.stats-card p {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 8px;
}

.stats-card ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.stats-card li {
  font-size: 15px;
  padding: 6px 0;
  border-bottom: 1px dashed #f0e6c2;
}

.stats-card li:last-child {
  border-bottom: none;
}

.highlight {
  font-weight: bold;
  color: #d4a017;
}
</style> 