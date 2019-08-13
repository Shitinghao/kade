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
    },
    {
      path: '/list',
      name: 'triples',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: Triples
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
      path: '/schema',
      name: 'Schema',
      meta: {
        keepAlive: true,
        isLogin: true
      },
      component: Schema
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
      path: '/logout',
      redirect: 'login'
    },
    {
      path: '/admin',
      redirect: 'list'
    }

  ]
})
