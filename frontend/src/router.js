import Vue from 'vue'
import Router from 'vue-router'
// import PromptView from './views/PromptView.vue'
import RAG from './views/RAG.vue'
// import LLMs from './views/LLMs.vue'
import LoginView from './views/LoginView.vue'
import AboutView from './views/AboutView.vue'
import NotFoundPage from './components/NotFoundPage.vue'
// import KB from './views/KB.vue'
import FileUploadView from './views/FileUploadView.vue'
import { clearAuthToken, isLoggedIn } from './utils/auth'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    // {
    //   path: '/',
    //   name: 'llms',
    //   component: LLMs
    // },
    {
      path: '/rag',
      name: 'rag',
      component: RAG
    },
    // {
    //   path: '/kb',
    //   name: 'kb',
    //   component: KB
    // },
    // {
    //   path: '/prompt',
    //   name: 'prompt',
    //   component: PromptView
    // },
    {
      path: '/upload',
      name: 'upload',
      component: FileUploadView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        allowAnonymous: true
      }
    },
    {
      path: '/logout',
      name: 'Logout',
      beforeEnter(to, from, next) {
        clearAuthToken()
        next('/login')
      },
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '*',
      component: NotFoundPage
    }
  ]
})


router.beforeEach((to, from, next) => {
  
  
  if (to.name == 'login' && isLoggedIn()) {
    console.log('redirecting to /rag')
    next({ path: '/rag' })
  }
  else if (!to.meta.allowAnonymous && !isLoggedIn()) {
   
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }
  else {
    console.log('router next()')
    next()
  }
})

export default router