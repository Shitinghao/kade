<template>
  <div class="nav-box" style="border: 1px solid rgb(113, 118, 244) ;background: rgb(113, 118, 244);height: 50px;padding-top:5px;">
    <p class="nav-list">
    <div class="left">
      <!--<router-link class="nav-item" to="/home">首页</router-link>-->
      <router-link class="nav-item" to="/list">列表</router-link>
      <router-link class="nav-item" to="/nodeGraph">nodeGraph</router-link>
    </div>
    <div class="right">
      <!--<router-link class="nav-item" to="/login">登录</router-link>-->
      <!--<router-link class="nav-item" to="/reg">注册</router-link>-->
    </div>
    <div style="clear: both;"></div>
    </p>
  </div>
</template>

<script>
// 创建子组建，相对于路径对应的页面
  const api_host = "http://127.0.0.1:26551";
  var main_entity = "";
  export default {
    name: 'Nav',
    api_host,
    main_entity
  }
</script>

<style scoped>

</style>
