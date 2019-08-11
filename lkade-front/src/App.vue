<template>
  <div id="app" style="margin-top: 0;">
    <!--<header-tab></header-tab>-->
    <!--<img src="./assets/logo1.png">-->
    <!--<h2>{{msg}}</h2>-->
     <div v-if="$route.meta.keepAlive">
       <Nav></Nav>
       <router-view />
     </div>
       <router-view v-if="!$route.meta.keepAlive"/>

    <!--<Triples></Triples>-->

  </div>
</template>

<script>
import Nav from './components/nav.vue'

// import

export default {
  name: 'App',
  components: {
    Nav,
  }
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
