<template>
  <div>
    <h3>充值审核</h3>
    <table class="recharge-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户</th>
          <th>金额</th>
          <th>时间</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in records" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.username }}</td>
          <td>{{ r.amount }}</td>
          <td>{{ formatTime(r.recharge_time) }}</td>
          <td>{{ statusText(r.status) }}</td>
          <td>
            <button v-if="r.status==='pending'" @click="approve(r.id, true)">通过</button>
            <button v-if="r.status==='pending'" @click="approve(r.id, false)">拒绝</button>
            <span v-else>--</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
export default {
  name: 'RechargeManager',
  data() {
    return { records: [] }
  },
  mounted() { this.loadRecords() },
  methods: {
    async loadRecords() {
      const res = await fetch('/api/recharge/records/')
      this.records = await res.json()
    },
    async approve(id, approve) {
      const res = await fetch('/api/recharge/approve/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recharge_id: id, approve })
      })
      const data = await res.json()
      if (data.success) {
        this.loadRecords()
      } else {
        alert(data.msg || '操作失败')
      }
    },
    formatTime(t) {
      return t ? t.replace('T', ' ').slice(0, 19) : ''
    },
    statusText(s) {
      if (s==='pending') return '待审核'
      if (s==='approved') return '已通过'
      if (s==='rejected') return '已拒绝'
      return s
    }
  }
}
</script>
<style scoped>
.recharge-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  margin-top: 18px;
}
.recharge-table th, .recharge-table td {
  border: 1px solid #e0c97f;
  padding: 8px 12px;
  text-align: center;
}
.recharge-table th {
  background: #f5ecd7;
  color: #a67c00;
}
.recharge-table button {
  margin: 0 4px;
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  background: #e6c97a;
  color: #5b4a1b;
  cursor: pointer;
  transition: background 0.2s;
}
.recharge-table button:hover {
  background: #d4a017;
  color: #fff;
}
</style> 