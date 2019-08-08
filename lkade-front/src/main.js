// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Element from 'element-ui'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueRouter from 'vue-router'
import $ from 'jquery'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

Vue.use(VueRouter)
Vue.use(Element)
Vue.use(ElementUI)

Vue.use(VueAxios, axios)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

router.beforeEach((to, from, next) => {
  if (window.sessionStorage.getItem('isLogin') === 'ok') {
    console.log(window.sessionStorage)
    if (to.path === '/') {
      next({path: '/list'})
    } else {
      next()
    }
  } else {
    if (to.path === '/') {
      next()
    } else {
      next({path: '/'})
    }
  }
})
