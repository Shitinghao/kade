import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import list from '@/components/list'
import login from '@/components/login'
import nodeGraph from '@/components/nodeGraph'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/',
      name: 'HelloWorld',
      // meta:{
      //   requireAuth:true
      // },
      component: HelloWorld

    },
    {
      path: '/list',
      name: 'App',
      component: list
    },
    {
      path: '/nodeGraph',
      name: 'nodeGraph',
      component: nodeGraph
    }
  ]
})
