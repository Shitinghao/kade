<template>
  <div class="schemas">
    <h1 style="margin: 60px 0;">Schema管理</h1>
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="18">
        <hr />
        <div class="content_style">
          <div class="btn-group" style="float: right;">
            <el-button type="info" @click="showNewSchemaDialog" class="addBtn_style">新增限制</el-button>
            <el-dialog title="新增限制" :visible.sync="newSchemaDialogVisible" width="50%" :before-close="handleClose">
              <div class="input_style">
                <label for="" style="float: left;">Cond_p</label>
                <el-input type="text" v-model="schema_inserts.cond_p" placeholder=""></el-input>
              </div>
              <div class="input_style">
                <label for="" style="float: left;">Op_type:</label>
                <el-select v-model="schema_inserts.op_type" placeholder="请选择" style="width: 100%">
                  <el-option v-for="item in op_type_options"
                             :key="item.value"
                             :label="item.label"
                             :value="item.value">
                  </el-option>
                </el-select>
              </div>
              <div class="input_style">
                <label for="" style="float: left;">Limit_o_type:</label>
                <el-select v-model="schema_inserts.limit_o_type" placeholder="请选择" style="width: 100%">
                  <el-option v-for="item in limit_o_type_options"
                             :key="item.value"
                             :label="item.label"
                             :value="item.value">
                  </el-option>
                </el-select>
              </div>
              <div class="input_style">
                <label for="" style="float: left;">Limit_o:</label>
                <el-input type="text" v-model="schema_inserts.limit_o" placeholder=""></el-input>
              </div>
              <span slot="footer" class="dialog-footer">
                <el-button @click="newSchemaDialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="submitNewSchema">确 定</el-button>
              </span>
            </el-dialog>
          </div>
          <div style="clear: both"></div>
          <hr class="hr_style" />
          <div class="grid-content">
            <el-table :data="schemaData" style="width: 100%" :default-sort="{prop: 'cond_p', order: 'descending'}" center="True">
              <el-table-column prop="cond_p" label="Cond_p" sortable>
              </el-table-column>
              <el-table-column prop="op_type" label="Op_type" sortable>
              </el-table-column>
              <el-table-column prop="limit_o_type" label="Limit_o_type" sortable>
              </el-table-column>
              <el-table-column prop="limit_o" label="Limit_o" sortable>
              </el-table-column>
              <el-table-column label="Operation" width="180">
                <template slot-scope="scope">
                  <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                    <el-button type="danger" size="medium" @click="handleRemove(remove_schema, scope.row.id)">删除</el-button>
                  </el-tooltip>
                  <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                    <el-button type="info" size="medium" @click="modify_schema(scope.row)">修改</el-button>
                  </el-tooltip>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import global from './nav.vue'
import qs from 'Qs'
export default {
  name: 'Schema',
  data () {
    return {
      api_host: global.api_host,
      newSchemaDialogVisible: false,
      schemaData: [],
      schema_inserts: { cond_p: '', op_type: 'and', limit_o_type: 'equal', limit_o: '', old_tid: '' },

      op_type_options: [{ value: 'and', label: 'and' }, { value: 'or', label: 'or' }],
      limit_o_type_options: [{value: 'regex', label: 'regex'}, {value: 'equal', label: 'equal'}, {value: 'eval', label: 'eval'}]
    }
  },
  methods: {
    list_schema() {
      let _this = this;
      this.axios
        .post(this.api_host + '/api/schemas', qs.stringify({}))
        .then(function (response) {
          if (response.data.status !== "ok") {
            _this.$message.error(response.data.msg);
          } else
            _this.schemaData = response.data.ret;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    modify_schema(titem) {
      let thetriple = this.schemaData.filter(elem => (elem.id === titem.id));
      if (thetriple.length === 1) {
        this.schema_inserts = {
          cond_p: thetriple[0].cond_p,
          op_type: thetriple[0].op_type,
          limit_o_type: thetriple[0].limit_o_type,
          limit_o: thetriple[0].limit_o,
          old_tid: titem.id
        }
      }
      this.newSchemaDialogVisible = true;
    },

    simple_remove(_this, url, pparams) {
      this.axios
        .post(url, qs.stringify(pparams))
        .then(function (response) {
          _this.list_schema();
        })
        .catch(function (error) {
          console.log(error);
        });
    },


    remove_schema(tid) {
      this.simple_remove(this, this.api_host+'/api/remove_schema', {
            id: tid
          });
    },

    showNewSchemaDialog() {
      this.schema_inserts = { cond_p: '', op_type: 'and', limit_o_type: 'equal', limit_o: '', old_tid: ''},
      this.newSchemaDialogVisible = true;
    },

    handleClose(done) {
      done();
    },
    handleRemove(func, fid) {
      this.$confirm('确认删除？')
        .then(_ => {
          func(fid);
        })
        .catch(_ => {});
    },
    submitNewSchema() {
      let _this = this;
      console.log(this.schema_inserts);
      this.checkAndSubmit(this, this.api_host + '/api/new_schema', {
          cond_p: this.schema_inserts.cond_p,
          op_type: this.schema_inserts.op_type,
          limit_o_type: this.schema_inserts.limit_o_type,
          limit_o: this.schema_inserts.limit_o,
          old_tid: this.schema_inserts.old_tid
        },
        function (response, _this) {
          if (_this.schema_inserts.old_tid !== "") {
            _this.remove_schema(_this.schema_inserts.old_tid);
            _this.schema_inserts.old_tid = "";
          }
          _this.list_schema();
          _this.inserts = { cond_p: '', op_type: '', limit_o_type: '', limit_o: '', old_tid: ''}
          _this.newSchemaDialogVisible = false;
        },
        function (response, _this) {
          _this.$message.error(response.data.msg);
        }
      );
    },


    checkAndSubmit(_this, url, pparams, succ_func, fail_func) {
      pparams["precheck"] = 1
      _this.axios
        .post(url, qs.stringify(pparams))
        .then(function (response) {
          if (response.data.status !== "ok") {
            fail_func(response, _this)
          } else {
            delete pparams["precheck"];
            _this.axios
              .post(url, qs.stringify(pparams))
              .then(response => succ_func(response, _this))
              .catch(function (error) {
                console.log(error);
              });
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

  },
  mounted() {
    this.list_schema();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
  .content_style{
    box-shadow: 0 0 3px lightgrey;margin: 30px 0;padding: 20px;
  }
  .input_style{
    margin: 10px;
  }
  /*table hr*/
  .hr_style{
    border:0;
    /*background-color:#F56C6C;*/
    background-color: #ffd04b;
    height:1px;
  }
  .addBtn_style{
    float: right;
    margin-bottom: 10px;
  }
.el-select .el-input .el-select__caret{
  margin-top: 10px;
}
</style>
