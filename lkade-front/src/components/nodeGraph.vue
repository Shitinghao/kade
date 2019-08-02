<template>
  <div>
    <h1>this is nodeGraph</h1>
    <!--检索实体-->
    <el-input type="text" placeholder="搜索" suffix-icon="el-icon-search" style="width:80%" @keyup.enter.native="search_entity(null)"></el-input>
    <el-button @click="search_entity(null)">搜索</el-button>
    <!--内容展示区-->
    <el-container>
      <el-main>
        <el-row :gutter="20" style="border: 1px solid red;">
          <!--图形控件区-->
          <div style="border: 1px solid black;">
            <el-button type="text" @click="table = true">实体详情</el-button>
          </div>
          <!--graph-->
          <div class="left_graph" ref="left_graph">
          </div>
        </el-row>
      </el-main>
    </el-container>

    <el-drawer
      title="我嵌套了表格!"
      :visible.sync="table"
      direction="rtl"
      size="50%">
      <el-table :data="gridData">
        <el-table-column property="date" label="日期" width="150"></el-table-column>
        <el-table-column property="name" label="姓名" width="200"></el-table-column>
        <el-table-column property="address" label="地址"></el-table-column>
      </el-table>
    </el-drawer>

  </div>

</template>

<script>
  // import 'd3/d3.min'
    export default {
        name: "nodeGraph",
      data() {
        return {
          table: false,
          dialog: false,
          loading: false,
          gridData: [{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-03',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }],
          formLabelWidth: '80px',
          url1:'',
          url2:''
          
        };

      },
      methods: {
        handleClose(done) {
          this.$confirm('确定要提交表单吗？')
            .then(_ => {
              this.loading = true;
              setTimeout(() => {
                this.loading = false;
                done();
              }, 2000);
            })
            .catch(_ => {});
        }
      }

    }

</script>

<style scoped>

</style>
