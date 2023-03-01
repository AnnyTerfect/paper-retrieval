import Vue from 'vue'
import VueRouter from 'vue-router'
import ViewPaper from '../views/ViewPaper.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ViewPaper',
    component: ViewPaper
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
