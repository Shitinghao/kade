<template>
  <el-menu router="true"  default-active="/list" mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
    <el-menu-item disabled="true" >此处放数眼logo</el-menu-item>
    <el-menu-item index="/list">数据表视图</el-menu-item>
    <el-menu-item index="/nodegraph">图谱视图</el-menu-item>
    <!--<router-link class="nav-item" to="/home">首页</router-link>-->
    <el-menu-item index="/logout" class="dock-right">退出登录</el-menu-item>
    <el-menu-item index="/admin" class="dock-right">admin</el-menu-item>

  </el-menu>
</template>

<script>
  // 创建子组建，相对于路径对应的页面
  const api_host = "http://127.0.0.1:26551";
  //const api_host = "";
  var main_entity = "";
  export default {
    name: 'Nav',
    api_host,
    main_entity
  }

</script>

<style   scoped>
  .el-menu--horizontal > .el-menu-item.dock-right{
    float: right;
  }
</style>
