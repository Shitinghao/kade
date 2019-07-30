<template>
  <div id="app" style="margin-top: 0;">
    <!--<header-tab></header-tab>-->
    <!--<h2>{{msg}}</h2>-->
    <div class="nav-box" style="border: 1px solid #F56C6C ;background: #F56C6C;">
      <p class="nav-list">
        <div class="left">
          <router-link class="nav-item" to="/">首页</router-link>
          <router-link class="nav-item" to="/list">列表</router-link>
          <router-link class="nav-item" to="/nodeGraph">nodeGraph</router-link>
        </div>
        <div class="right">
          <router-link class="nav-item" to="/login">登录</router-link>
          <router-link class="nav-item" to="/reg">注册</router-link>
        </div>
        <div style="clear: both;"></div>
      </p>
    </div>
    <div>
      <router-view></router-view>
    </div>
    <!--<router-view />-->
    <!--<Triples></Triples>-->


  </div>
</template>

<script>
// import Triples from './components/Triples.vue'

// import

export default {
  name: 'App',
  // components: {
  //   Triples,
  // }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
  .left{
    float: left;margin-left:100px;
  }
  .right{
    float: right;margin-right:100px;
  }
  .nav-item{
    color: white;
    text-decoration: none;
  }
</style>
