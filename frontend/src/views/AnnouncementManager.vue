<template>
  <div>
    <h3>公告管理</h3>
    <button class="add-btn" @click="showAdd=true">发布新公告</button>

    <table class="announcement-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>内容</th>
          <th>发布时间</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in announcements" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.title }}</td>
          <td>{{ a.content.slice(0, 50) }}...</td>
          <td>{{ formatTime(a.published_at) }}</td>
          <td>{{ a.is_published ? '已发布' : '草稿' }}</td>
          <td>
            <button @click="editAnnouncement(a)">编辑</button>
            <button @click="deleteAnnouncement(a.id)">删除</button>
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
        <h4>{{ editData ? '编辑公告' : '发布公告' }}</h4>
        <form @submit.prevent="submitAnnouncement">
          <input v-model="form.title" placeholder="公告标题" required />
          <textarea v-model="form.content" placeholder="公告内容" required></textarea>
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.is_published" /> 是否立即发布
          </label>
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
  name: 'AnnouncementManager',
  data() {
    return {
      announcements: [],
      showAdd: false,
      editData: null,
      form: { title: '', content: '', is_published: true },
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
  mounted() {
    this.loadAnnouncements()
  },
  methods: {
    async loadAnnouncements() {
      const res = await fetch(`/api/manage/announcement/?page=${this.page}&page_size=${this.pageSize}`)
      const data = await res.json()
      this.announcements = data.results
      this.total = data.total
    },
    changePage(p) {
      this.page = p
      this.loadAnnouncements()
    },
    async submitAnnouncement() {
      const method = this.editData ? 'PUT' : 'POST'
      const body = this.editData ? { ...this.form, id: this.editData.id } : this.form
      const res = await fetch('/api/manage/announcement/', {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      const data = await res.json()
      if (data.id) {
        this.closeModal()
        this.loadAnnouncements()
      } else {
        alert('操作失败: ' + JSON.stringify(data))
      }
    },
    editAnnouncement(announcement) {
      this.editData = announcement
      this.form = { ...announcement }
      this.showAdd = false
    },
    async deleteAnnouncement(id) {
      if (!confirm('确定要删除该公告吗？')) return
      const res = await fetch('/api/manage/announcement/', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      })
      if (res.status === 204) {
        this.loadAnnouncements()
      } else {
        alert('删除失败')
      }
    },
    closeModal() {
      this.showAdd = false
      this.editData = null
      this.form = { title: '', content: '', is_published: true }
    },
    formatTime(t) {
      return t ? t.replace('T', ' ').slice(0, 16) : ''
    }
  }
}
</script>

<style scoped>
.add-btn {
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 6px;
  padding: 10px 24px;
  font-size: 16px;
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

.announcement-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  margin-top: 18px;
}
.announcement-table th, .announcement-table td {
  border: 1px solid #e0c97f;
  padding: 8px 12px;
  text-align: center;
}
.announcement-table th {
  background: #f5ecd7;
  color: #a67c00;
}
.announcement-table button {
  margin: 0 4px;
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  background: #e6c97a;
  color: #5b4a1b;
  cursor: pointer;
  transition: background 0.2s;
}
.announcement-table button:hover {
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

/* Modal Styles - Reuse from BookManager/UserManager if possible, for consistency */
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
  min-width: 400px;
  box-shadow: 0 2px 12px #e0c97f;
}
.modal-content input[type="text"], .modal-content textarea {
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
.checkbox-label {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: #5b4a1b;
  font-size: 15px;
}
.checkbox-label input[type="checkbox"] {
  margin-right: 8px;
  width: 16px;
  height: 16px;
}
</style> 