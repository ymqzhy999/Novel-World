# 小说阅读平台

一个基于Django后端和Vue3前端的现代化小说阅读平台，提供完整的小说阅读、用户管理、评论互动等功能。

## 功能特性

### 用户功能
- ✅ 用户注册/登录（邮箱格式验证）
- ✅ 账号信息管理
- ✅ 历史浏览记录
- ✅ 个人评论管理
- ✅ 书架收藏（界面已实现）
- ✅ 充值中心（界面已实现）
- ✅ 消息通知（界面已实现）

### 小说功能
- ✅ 小说列表展示（宫格布局）
- ✅ 小说搜索（按标题/作者）
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

## 数据库模型

### 主要表结构
- **User** - 用户表
- **Novel** - 小说表
- **Chapter** - 章节表
- **Comment** - 评论表
- **SearchHistory** - 搜索历史表
- **Bookshelf** - 书架表
- **RechargeRecord** - 充值记录表
- **PaidReadingRecord** - 付费阅读记录表

## 开发说明

### 添加新功能
1. 在`app01/models.py`中定义数据模型
2. 在`app01/views.py`中实现API逻辑
3. 在`app01/urls.py`中注册路由
4. 在前端`src/views/`中创建页面
5. 在`src/router/index.js`中添加路由

### 样式规范
- 主色调：#a67c00（温暖米黄）
- 背景色：#fffbe6（浅米黄）
- 强调色：#d4a017（金黄色）
- 字体：楷体优先，serif备用

### 代码规范
- 后端：遵循Django最佳实践
- 前端：使用Vue 3 Composition API
- 命名：使用驼峰命名法
- 注释：关键功能添加中文注释

## 部署说明

### 生产环境部署
1. 配置生产数据库
2. 设置环境变量
3. 收集静态文件
4. 配置Web服务器（Nginx）
5. 使用Gunicorn运行Django
6. 构建前端生产版本

### 环境变量
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@localhost/novel_platform
ALLOWED_HOSTS=your-domain.com
```
修改了 NovelListView 的 get 方法：
现在，在获取小说列表之前，它会尝试从 Redis 缓存中读取数据。
如果缓存中有数据，它会直接返回缓存的数据，并且会在后端打印 "从 Redis 缓存中获取小说列表"。
如果缓存中没有数据，它会从数据库中查询小说列表，然后将查询到的数据存入 Redis 缓存，并设置 60 秒的过期时间，同时会在后端打印 "将小说列表存入 Redis 缓存"