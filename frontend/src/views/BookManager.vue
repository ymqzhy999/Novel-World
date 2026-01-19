<template>
  <div>
    <h3>书籍管理</h3>
    <button class="add-btn" @click="showAdd=true">添加新书籍</button>
    <table class="novel-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>作者</th>
          <th>分类</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="n in novels" :key="n.id">
          <td>{{ n.id }}</td>
          <td>{{ n.title }}</td>
          <td>{{ n.author }}</td>
          <td>{{ n.category }}</td>
          <td>
            <button @click="editNovel(n)">编辑</button>
            <button @click="deleteNovel(n.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button :disabled="page===1" @click="changePage(page-1)">上一页</button>
      <span>第{{ page }}/{{ totalPages }}页</span>
      <button :disabled="page===totalPages" @click="changePage(page+1)">下一页</button>
    </div>
    <!-- 添加/编辑弹窗 -->
    <div v-if="showAdd || editData" class="modal">
      <div class="modal-content">
        <h4>{{ editData ? '编辑书籍' : '添加书籍' }}</h4>
        <form @submit.prevent="submitNovel">
          <input v-model="form.title" placeholder="标题" required />
          <input v-model="form.author" placeholder="作者" required />
          <input v-model="form.category" placeholder="分类" />
          <input v-model="form.cover_url" placeholder="封面URL" />
          <textarea v-model="form.description" placeholder="简介"></textarea>
          <textarea v-model="form.content" placeholder="内容"></textarea>
          <div class="modal-actions">
            <button type="submit">保存</button>
            <button type="button" @click="closeModal">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'BookManager',
  data() {
    return {
      novels: [],
      showAdd: false,
      editData: null,
      form: { title: '', author: '', category: '', cover_url: '', description: '', content: '' },
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
  mounted() { this.loadNovels() },
  methods: {
    async loadNovels() {
      const res = await fetch(`/api/manage/novel/?page=${this.page}&page_size=${this.pageSize}`)
      const data = await res.json()
      this.novels = data.results
      this.total = data.total
    },
    changePage(p) {
      this.page = p
      this.loadNovels()
    },
    async submitNovel() {
      const method = this.editData ? 'PUT' : 'POST'
      const body = this.editData ? { ...this.form, id: this.editData.id } : this.form
      const res = await fetch('/api/manage/novel/', {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      const data = await res.json()
      this.closeModal()
      this.loadNovels()
    },
    editNovel(novel) {
      this.editData = novel
      this.form = { ...novel }
      this.showAdd = false
    },
    async deleteNovel(id) {
      if (!confirm('确定要删除这本书吗？')) return
      await fetch('/api/manage/novel/', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      })
      this.loadNovels()
    },
    closeModal() {
      this.showAdd = false
      this.editData = null
      this.form = { title: '', author: '', category: '', cover_url: '', description: '', content: '' }
    }
  }
}
</script>
<style scoped>
.novel-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  margin-top: 18px;
}
.novel-table th, .novel-table td {
  border: 1px solid #e0c97f;
  padding: 8px 12px;
  text-align: center;
}
.novel-table th {
  background: #f5ecd7;
  color: #a67c00;
}
.novel-table button {
  margin: 0 4px;
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  background: #e6c97a;
  color: #5b4a1b;
  cursor: pointer;
  transition: background 0.2s;
}
.novel-table button:hover {
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
.modal {
  position: fixed;
  left: 0; top: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: #fffbe6;
  border-radius: 8px;
  padding: 32px 24px;
  min-width: 350px;
  box-shadow: 0 2px 12px #e0c97f;
}
.modal-content input, .modal-content textarea {
  width: 100%;
  margin-bottom: 12px;
  padding: 8px;
  border: 1px solid #e0c97f;
  border-radius: 4px;
  font-size: 15px;
  background: #fdf6e3;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.add-btn {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 6px;
  padding: 12px 32px;
  font-size: 17px;
  font-weight: bold;
  margin-bottom: 18px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  box-shadow: 0 2px 8px #e0c97f;
}
.add-btn:hover {
  background: #d4a017;
  color: #fff;
}
</style> 