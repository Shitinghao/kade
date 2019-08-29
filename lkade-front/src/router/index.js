import Vue from 'vue'
import Router from 'vue-router'
import Triples from '@/components/Triples'
import login from '@/components/login'
import reg from '@/components/reg'
import nodeGraph from '@/components/nodeGraph'
import Schema from '@/components/Schema'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/kg/kade/login',
      name: 'login',
      meta: {
        isLogin: false,
        keepAlive: false
      },
      component: login
    },
    {
      path: '/kg/kade/',
      redirect: '/kg/kade/login'
    },
    {
      path: '/kg/kade/list',
      name: 'triples',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: Triples
    },
    {
      path: '/kg/kade/nodeGraph',
      name: 'nodeGraph',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: nodeGraph
    },
    {
      path: '/kg/kade/schema',
      name: 'Schema',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: Schema
    },
    {
      path: '/kg/kade/reg',
      name: 'reg',
      meta: {
        isLogin: false,
        keepAlive: false
      },
      component: reg
    },
    {
      path: '/kg/kade/logout',
      redirect: '/kg/kade/login'
    },
    {
      path: '/kg/kade/admin',
      redirect: '/kg/kade/list'
    }

  ]
})
