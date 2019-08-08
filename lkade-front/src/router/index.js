import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import list from '@/components/list'
import login from '@/components/login'
import reg from '@/components/reg'
import nodeGraph from '@/components/nodeGraph'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      meta: {
        isLogin: false,
        keepAlive: false
      },
      component: login
    },
    {
      path: '/',
      redirect: 'login'
      // name: 'HelloWorld',
      // meta: {
      //   requireAuth: true
      // },
      // component: HelloWorld

    },
    {
      path: '/list',
      name: 'HelloWorld',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: HelloWorld
    },
    {
      path: '/nodeGraph',
      name: 'nodeGraph',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: nodeGraph
    },
    {
      path: '/reg',
      name: 'reg',
      meta: {
        isLogin: false,
        keepAlive: false
      },
      component: reg
    },
    {
      path: '/list',
      name: 'list',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: list
    },
    {
      path:'/logout',
      redirect: 'login'
    },
    {
      path:'/admin',
      redirect: 'list'
    }

  ]
})

