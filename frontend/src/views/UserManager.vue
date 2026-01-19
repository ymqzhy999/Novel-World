<template>
  <div>
    <h3>用户管理</h3>
    <table class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>邮箱</th>
          <th>余额</th>
          <th>身份</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.balance }}</td>
          <td>{{ u.role === 'admin' ? '管理员' : '普通用户' }}</td>
          <td>{{ u.is_active == false ? '已禁用' : '正常' }}</td>
          <td>
            <button @click="toggleUser(u)">{{ u.is_active == false ? '启用' : '禁用' }}</button>
            <button @click="deleteUser(u.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button :disabled="page===1" @click="changePage(page-1)">上一页</button>
      <span>第{{ page }}/{{ totalPages }}页</span>
      <button :disabled="page===totalPages" @click="changePage(page+1)">下一页</button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'UserManager',
  data() {
    return {
      users: [],
      page: 1,
      pageSize: 10,
      total: 0
    }
  },
  computed: {
    totalPages() {
      return Math.max(1, Math.ceil(this.total / this.pageSize))
    }
  },
  mounted() { this.loadUsers() },
  methods: {
    async loadUsers() {
      const res = await fetch(`/api/manage/user/?page=${this.page}&page_size=${this.pageSize}`)
      const data = await res.json()
      this.users = data.results
      this.total = data.total
    },
    changePage(p) {
      this.page = p
      this.loadUsers()
    },
    async toggleUser(user) {
      await fetch('/api/manage/user/', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: user.id, disabled: user.is_active })
      })
      this.loadUsers()
    },
    async deleteUser(id) {
      if (!confirm('确定要删除该用户吗？')) return
      await fetch('/api/manage/user/', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      })
      this.loadUsers()
    }
  }
}
</script>
<style scoped>
.user-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  margin-top: 18px;
}
.user-table th, .user-table td {
  border: 1px solid #e0c97f;
  padding: 8px 12px;
  text-align: center;
}
.user-table th {
  background: #f5ecd7;
  color: #a67c00;
}
.user-table button {
  margin: 0 4px;
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  background: #e6c97a;
  color: #5b4a1b;
  cursor: pointer;
  transition: background 0.2s;
}
.user-table button:hover {
  background: #d4a017;
  color: #fff;
}
.pagination {
  margin: 18px 0;
  text-align: center;
}
.pagination button {
  margin: 0 8px;
  padding: 4px 14px;
  border: none;
  border-radius: 4px;
  background: #e6c97a;
  color: #5b4a1b;
  cursor: pointer;
  transition: background 0.2s;
}
.pagination button:disabled {
  background: #f5ecd7;
  color: #aaa;
  cursor: not-allowed;
}
</style> 