<img width="1246" height="628" alt="1f8ec88c24f55db33e603dd4be8023e0" src="https://github.com/user-attachments/assets/5e2df5d8-13c5-40a5-97fb-723b8142af69" /># 小说阅读平台

一个基于Django后端和Vue3前端的现代化小说阅读平台，提供完整的小说阅读、用户管理、评论互动等功能。

## 功能特性

### 用户功能
- ✅ 用户注册/登录（邮箱格式验证）
- ✅ 账号信息管理
- ✅ 历史浏览记录
- ✅ 个人评论管理
- ✅ 书架收藏
- ✅ 充值中心
- ✅ 消息通知

### 小说功能
- ✅ 小说列表展示
- ✅ 小说搜索
- ✅ 章节列表浏览
- ✅ 章节内容阅读
- ✅ 上下章切换
- ✅ 评论互动系统

### 技术特性
- 🎨 温暖米黄色调UI设计
- 📱 响应式布局，支持移动端
- 🔄 前后端数据实时同步
- 💾 自动历史浏览记录
- 💬 实时评论系统

## 技术栈

### 后端
- **Django 4.2+** - Web框架
- **Django REST Framework** - API开发
- **MySQL** - 数据库
- **PyMySQL** - MySQL驱动

### 前端
- **Vue 3** - 前端框架
- **Vite** - 构建工具
- **Vue Router** - 路由管理
- **原生CSS** - 样式设计

## 项目结构

```
django_project/
├── backend/                 # Django后端
│   ├── app01/              # 主应用
│   │   ├── models.py       # 数据模型
│   │   ├── views.py        # API视图
│   │   ├── urls.py         # 路由配置
│   │   └── serializers.py  # 序列化器
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # Vue前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面
│   │   ├── router/         # 路由
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 安装运行

### 1. 环境准备
确保已安装：
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置数据库
# 在settings.py中修改数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'novel_platform',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 创建数据库
mysql -u root -p
CREATE DATABASE novel_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 迁移数据库
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动后端服务
python manage.py runserver
```

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用
- 前端地址：http://localhost:5173
- 后端API：http://localhost:8000

## API接口

### 用户相关
- `POST /api/user/register/` - 用户注册
- `POST /api/user/login/` - 用户登录
- `GET /api/user/info/` - 获取用户信息
- `GET /api/user/{id}/comments/` - 获取用户评论
- `GET /api/user/{id}/history/` - 获取历史浏览

### 小说相关
- `GET /api/novels/` - 获取小说列表
- `GET /api/novel/{id}/chapters/` - 获取章节列表
- `GET /api/novel/{id}/comments/` - 获取小说评论
- `POST /api/novel/{id}/comments/` - 发表评论

### 历史记录
- `POST /api/history/add/` - 添加历史浏览


### 主要表结构
- **User** - 用户表
- **Novel** - 小说表
- **Chapter** - 章节表
- **Comment** - 评论表
- **SearchHistory** - 搜索历史表
- **Bookshelf** - 书架表
- **RechargeRecord** - 充值记录表
- **PaidReadingRecord** - 付费阅读记录表


系统采用了 Redis 对小说列表接口进行了 60 秒的缓存策略，有效减轻数据库压力。 充值流程采用 申请 -> 审核 机制，保障资金安全。 评论系统支持多级回复展示。  如果没有redis服务，可以去app01/views.py注释redis连接
数据来源说明：本系统所有小说数据均通过 get_novel.py 脚本对公开的小说平台进行合法采集。采集过程严格遵循相关平台的 robots.txt 协议，仅用于展示开发技术及后端逻辑实现。

<img width="1161" height="624" alt="40a0291cb7c8fbc056cd28f66e831638" src="https://github.com/user-attachments/assets/e1d58578-a37f-4f19-8949-54c0f493909b" />




