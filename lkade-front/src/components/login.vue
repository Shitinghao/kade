<template>
  <div>
    <h1>登录</h1>
    <!--<div class="login">-->
    <el-container>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="12" :offset="6">
              <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" style="margin-left: -70px;">
                <el-form-item label="用户名" prop="name">
                  <el-input v-model.number="ruleForm.name"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pass">
                  <el-input type="password" v-model="ruleForm.pass" autocomplete="off" @keyup.enter.native="submitForm('ruleForm')"></el-input>
                </el-form-item>
                <!--<el-form-item label="确认密码" prop="checkPass">-->
                  <!--<el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>-->
                <!--</el-form-item>-->

                <el-form-item>
                  <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                  <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
              </el-form>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    <div style="position: absolute;width: 100%;height: 100%;background:#FFFFFF;top: 0;z-index: -10"></div>
    <!--</div>-->
  </div>

</template>

<script>
  import global from './nav.vue'
  import qs from 'Qs'
  import md5 from 'js-md5';
export default {
  name: 'login',
  data () {
    var checkName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('用户名不能为空'))
      } else {
        callback()
      }
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        pass: '',
        checkPass: '',
        name: ''
      },
      rules: {
        pass: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        name: [
          { validator: checkName, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm: function (formName) {
      let _this = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.axios
            .post(global.api_host + '/login_check', qs.stringify({
               user: this.ruleForm.name,
               passwd: md5(this.ruleForm.pass+'salt123')
              })
            )
            .then(function (response) {
              console.log(response);
              var ses = window.sessionStorage;
              if (response.data.status === 'ok') {
                ses.setItem('isLogin', 'ok');
                ses.setItem('uname', response.data.uname);
                _this.$router.push({ path: '/kg/kade/list' })

              } else {
                _this.$message.error("登陆失败")
                var ses = window.sessionStorage;
                ses.setItem('isLogin', 'fail');
              }

            })
            .catch(function (error) {
              console.log(error);
            });
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  },
  mounted() {
  }

}
</script>

<style scoped>
  .input{

  }

</style>
