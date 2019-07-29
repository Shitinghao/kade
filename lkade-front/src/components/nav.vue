<!--<template>-->
    <div id="app">
      <nav class="navbar navbar-inverse">
        <div class="container">
          <div class="coolapse navbar-coolapse">
            <ul class="nav navbar-nav">
              <li>
                <a v-link="{path:'/home'}">Home</a>
              </li>
              <li>
                <a v-link="{path:'/list'}">List</a>
              </li>
              <li>
                <a v-link="{path:'/nodeGraph'}">NodeGraph</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <!--路由组建template插入的位置-->
      <div class="container">
        <router-vue></router-vue>
      </div>
    </div>
<!--</template>-->

<script>
    // 创建子组建，相对于路径对应的页面
    // export default {
    //     name: "nav"
    // }

    var Home = Vue.extend({
      template:'<h1>this is home page</h1>'
    });
    //创建跟组建
    var App = vue.extend({})
//  创建路由实例
    var router = new VueRouter()
    router.map({
      '/home':{
        component:Home
      },
      '/list':{
        component: {
          template: '<h1>this is list</h1>'
        }
      }

    })
  router.start(App,'#app')
</script>

<style scoped>

</style>
