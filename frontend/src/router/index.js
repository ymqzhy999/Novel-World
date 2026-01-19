import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/LoginRegister.vue'
import UserHome from '../views/UserHome.vue'
import AccountInfo from '../views/AccountInfo.vue'
import NovelList from '../views/NovelList.vue'
import ChapterList from '../views/ChapterList.vue'
import ChapterContent from '../views/ChapterContent.vue'
import LoginRegister from '../views/LoginRegister.vue'
import Bookshelf from '../views/Bookshelf.vue'
import Recharge from '../views/Recharge.vue'
import Messages from '../views/Messages.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginRegister },
  { path: '/user-home', component: UserHome, children: [
    { path: 'account-info', component: AccountInfo },
    { path: 'novel-list', component: NovelList },
    { path: 'novel-list/:novelId', component: ChapterList, props: true },
    { path: 'bookshelf', component: Bookshelf },
    { path: 'recharge', component: Recharge },
    { path: 'messages', component: Messages },
  ]},
  { path: '/user-home/novel-list/:novelId/chapter/:chapterId', component: ChapterContent, props: true },
  { path: '/admin', component: AdminDashboard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 