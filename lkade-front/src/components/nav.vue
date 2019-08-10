<template>
  <el-menu router default-active="/list" mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
    <el-menu-item disabled :unique-opened="true" style="opacity:1;width:200px;">
      <img :src="imgUrl" style="width: 100%;"/>
    </el-menu-item>

    <el-menu-item index="/list">数据表视图</el-menu-item>
    <el-menu-item index="/nodegraph">图谱视图</el-menu-item>
    <!--<router-link class="nav-item" to="/home">首页</router-link>-->
    <el-menu-item index="/logout" class="dock-right" @click="logout">退出登录</el-menu-item>
    <el-menu-item index="/admin" class="dock-right">admin</el-menu-item>

  </el-menu>
</template>

<script>
  import avatar from '@/assets/logo1.png'
  // 创建子组建，相对于路径对应的页面
  const api_host = process.env.VUE_APP_API_HOST;
  var main_entity = "";
  export default {
    name: 'Nav',
    data (){
      return{
        imgUrl: '../../static/logo1.png'
      }
    },
    api_host,
    main_entity,
    methods:{
      logout: function () {
        this.axios
          .get(this.api_host+'/login_exit')
          .then(function (response) {
            window.sessionStorage.removeItem('isLogin');
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    }
  }

</script>

<style scoped>
  .el-menu--horizontal > .el-menu-item.dock-right{
    float: right;
  }
</style>
