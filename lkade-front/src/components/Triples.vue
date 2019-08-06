<template>
  <div class="triples">
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="18">
        <el-input type="text" :name="searchStr" v-model="searchStr" placeholder="搜索" suffix-icon="el-icon-search" style="width:80%" @keyup.enter.native="search_entity(null)"></el-input>
        <el-button @click="search_entity(null, null)">搜索</el-button>

        <div class="grid-content content_style">
          <div style="">
            <el-button type="info" @click="entDialogVisible=true" class="addBtn_style">新增实体</el-button>
            <el-dialog title="新增实体" :visible.sync="entDialogVisible" width="50%" :before-close="handleClose">
              <label for="" style="float: left;">name:</label>
              <el-input type="text" v-model="ent_inserts.ename" placeholder="请输入新增实体的名称"></el-input>
              <span slot="footer" class="dialog-footer">
                <el-button @click="entDialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="submitNewEntity">确 定</el-button>
              </span>
            </el-dialog>
            <el-dialog title="删除实体" :visible.sync="entDelDialogVisible" width="50%">
              <span>将要删除实体 {{ent_dels.eid}} , 以下关系也将被同步删除：</span>
              <el-table :data="delEntData" style="width: 100%" center="True">
                <el-table-column prop="s" label="Subject"></el-table-column>
                <el-table-column prop="p" label="Preidcate"></el-table-column>
                <el-table-column prop="o" label="Object"></el-table-column>
              </el-table>
              <span slot="footer" class="dialog-footer">
                <el-button @click="entDelDialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="remove_entity(ent_dels.eid)">确 定</el-button>
              </span>
            </el-dialog>
          </div>
          <el-table :data="entityData" style="width: 100%" :default-sort="{prop: 'eid', order: 'descending'}" center="True">
            <el-table-column label="Entity" sortable>
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end">
                  <a @click="search_entity(scope.row.ename, scope.row.eid)" class="buttonText">{{scope.row.ename}}</a>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="Operation" width="180">
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end" v-if="scope.row.eid !== ''">
                  <el-button type="danger" size="medium" @click="showRemoveEntDialog(scope.row.eid)">删除</el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>

        </div>
        <hr/>
        <div class="content_style">
          <div style="clear: both"></div>
          <hr class="hr_style" />
          <div class="grid-content">
            <el-table :data="ment2entData" style="width: 100%" :default-sort="{prop: 'eid', order: 'descending'}" center="True">
              <el-table-column prop="mention" label="Mention" sortable>
              </el-table-column>
              <el-table-column label="Entity" sortable>
                <template slot-scope="scope">
                  <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end">
                    <a @click="search_entity(scope.row.ename, scope.row.eid)" class="buttonText">{{scope.row.ename}}</a>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="Operation" width="180">
                <template slot-scope="scope">
                  <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                    <el-button type="danger" size="medium" @click="handleRemove(remove_ment2ent, scope.row.id)">删除</el-button>
                  </el-tooltip>
                  <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end" v-if="scope.row.id === ''">
                    <el-button type="info" size="medium" @click="showNewM2EDialog(scope.row)">新增别名</el-button>
                  </el-tooltip>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <el-dialog title="新增别名" :visible.sync="m2eDialogVisible" width="50%" :before-close="handleClose">
            <label for="" style="float: left;"> Entity:</label>
            <el-input type="text" v-model="m2e_inserts.ename" placeholder="" :disabled="true" v-if="m2e_inserts.eid !== m2e_inserts.ename"></el-input>
            <el-input type="text" v-model="m2e_inserts.eid" placeholder="" :disabled="true"></el-input>
            <label for="" style="float: left;"> Mention:</label>
            <el-input type="text" v-model="m2e_inserts.mention" placeholder="请输入新的别名"></el-input>
            <span slot="footer" class="dialog-footer">
              <el-button @click="m2eDialogVisible=false">取 消</el-button>
              <el-button type="primary" @click="submitNewM2E">确 定</el-button>
            </span>
          </el-dialog>
        </div>

        <hr/>
       <div class="content_style">


        <div class="btn-group" style="float: right;">
          <el-button type="info" @click="dialogVisible=true" class="addBtn_style">新增关系</el-button>
          <el-dialog title="新增关系" :visible.sync="dialogVisible" width="50%" :before-close="handleClose">
            <div class="input_style">
              <label for="" style="float: left;">Subject: </label>
              <el-input type="text" v-model="inserts.sname" placeholder="" :disabled="true"></el-input>
              <el-input type="text" v-model="inserts.sid" placeholder="" :disabled="true"  v-if="inserts.sid !== inserts.sname"></el-input>
            </div>
            <div class="input_style">
              <label for="" style="float: left;"> Predicate:</label>
              <el-input type="text" v-model="inserts.p" placeholder=""></el-input>
            </div>
            <div class="input_style">
              <label for="" style="float: left;"> Object:</label>
              <el-input type="text" v-model="inserts.oname" placeholder="" v-on:input="objectSuggestion(true)"></el-input>
            </div>
            <div class="input_style">
              <label for="" style="float: left;"> 实体ID:</label>
                <el-select v-model="inserts.oid" placeholder="实体id" @change="objectSelectEnt($event)" style="width: 100%;">
                  <el-option v-for="item in inserts.options" :key="item.value"
                             :label="item.label" :value="item.value" style="width: 100%">
                  </el-option>
                </el-select>
            </div>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible=false">取 消</el-button>
              <el-button type="primary" @click="submitNewTriple">确 定</el-button>
            </span>
          </el-dialog>
        </div>
        <div style="clear: both"></div>
         <hr class="hr_style"/>
        <div class="grid-content">
          <el-table :data="tripleData" style="width: 100%" :default-sort="{prop: 'p', order: 'descending'}" center="True">
            <el-table-column prop="sname" label="Subject" sortable>
            </el-table-column>
            <el-table-column prop="p" label="Predicate" sortable>
            </el-table-column>
            <el-table-column label="Object">
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.oid" placement="top-end" v-if="scope.row.oid !== ''">
                  <a @click="search_entity(scope.row.oname, scope.row.oid)" class="buttonText">{{scope.row.oname}}</a>
                </el-tooltip>
                <span v-if="scope.row.oid === ''">{{scope.row.oname}}</span>
              </template>
            </el-table-column>
            <el-table-column label="Operation" width="180">
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                  <el-button type="danger" size="medium" @click="handleRemove(remove_triple, scope.row)">删除</el-button>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                  <el-button type="info" size="medium" @click="modify_triple(scope.row)">修改</el-button>
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
export default {
  name: 'Triples',
  data () {
    return {
      api_host: global.api_host,
      searchStr: '',
      entityData: [],
      tripleData: [],
      ment2entData: [],
      delEntData: [],
      nowsearchStr: '',
      dialogVisible: false,
      entDialogVisible: false,
      m2eDialogVisible: false,
      entDelDialogVisible: false,
      ent_dels: { eid: '' },
      inserts: { sid: '', sname:'', p: '', oid: '', oname: '', old_titem: '' },
      ent_inserts: { ename: '' },
      m2e_inserts: { mention: '', eid: '' }
    }
  },
  methods: {
    search_entity(ename, eid) {
      let queryStr = null;
      if (ename != null) {
        queryStr = ename;
        if (eid != null && eid !== ename) {
          queryStr = ename + "<id:" + eid + ">"
        }
      }
      console.log("queryStr:" + queryStr);
      if (queryStr != null && queryStr !== "") this.searchStr = queryStr;
      let _this = this;
      this.axios
        .get(this.api_host+'/api/triples', {
          params: {
            entity: this.searchStr
          }
        })
        .then(function (response) {
          _this.tripleData = response.data.ret;
        })
        .catch(function (error) {
          console.log(error);
        });
      this.axios
        .get(this.api_host+'/api/ment2ent', {
          params: {
            q: this.searchStr
          }
        })
        .then(function (response) {
          _this.ment2entData = response.data.ret;
          let ents = response.data.ret.filter(x => (x.isent));
          _this.entityData = [];
          ents.forEach(function (x) {
            _this.entityData.push({
              eid: x.eid,
              ename: x.ename
            });
            global.main_entity = x.ename;
            _this.inserts = { sid: x.eid, sname: x.ename, p: '', oid: '', old_titem: '' }
          });
        })
        .catch(function (error) {
          console.log(error);
        });
      this.nowsearchStr = this.searchStr;
    },
    modify_triple(titem) {
      let thetriple = this.tripleData.filter(elem => (elem.id === titem.id));
      if (thetriple.length === 1) {
        this.inserts = {
          sid: thetriple[0].s,
          sname: thetriple[0].sname,
          p: thetriple[0].p,
          oid: thetriple[0].oid,
          oname: thetriple[0].oname,
          old_titem: titem
        }
      }
      if (this.inserts.oid !== "") this.objectSuggestion(false);
      this.dialogVisible = true;
    },
    showNewM2EDialog(item) {
      this.m2e_inserts.eid = item.eid;
      this.m2e_inserts.ename = item.ename;
      this.m2eDialogVisible = true;
    },

    simple_remove(_this, url, pparams) {
      this.axios
        .get(url, {
          params: pparams
        })
        .then(function (response) {
          _this.search_entity(_this.nowsearchStr);
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    remove_triple(item) {
      console.log(item);
      this.simple_remove(this, this.api_host+'/api/remove_triple', {
        id: item.id,
        oid: item.oid
      });
    },

    remove_ment2ent(tid) {
      this.simple_remove(this, this.api_host+'/api/remove_ment2ent', {
            id: tid
          });
    },

    remove_entity(tid) {
      let _this = this;
      this.axios
        .get(this.api_host+'/api/remove_entity', {
          params: {
            id: tid
          }
        })
        .then(function (response) {
          _this.search_entity(_this.nowsearchStr);
          _this.entDelDialogVisible = false;
          _this.ent_dels.eid = "";
        })
        .catch(function (error) {
          console.log(error);
        });
    },


    showRemoveEntDialog(eid) {
      let _this = this;
      this.ent_dels.eid = eid;
      this.axios
        .get(this.api_host+'/api/info_remove_entity', {
          params: {
            id: eid
          }
        })
        .then(function (response) {
          _this.delEntData = response.data.ret;
          _this.entDelDialogVisible = true;
        })
        .catch(function (error) {
          console.log(error);
        });
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


    submitNewTriple() {
      let _this = this;
      console.log(this.inserts);
      this.checkAndSubmit(this, this.api_host+'/api/new_triple', {
          sid: this.inserts.sid,
          p: this.inserts.p,
          oid: this.inserts.oid,
          oname: this.inserts.oname,
          old_titem: this.inserts.old_titem
        },
        function (response, _this) {
          if (_this.inserts.old_titem !== "") {
            _this.remove_triple(_this.inserts.old_titem);
            _this.inserts.old_titem = "";
          }
          _this.search_entity(_this.nowsearchStr);
          _this.inserts = { sid: '', sname: '', p: '', oid: '', old_titem: '' };
          _this.dialogVisible = false;
        },
        function (response, _this) {
          _this.$message.error(response.data.msg);
        }
      );
    },

    submitNewEntity() {
      let _this = this;
      this.checkAndSubmit(this, this.api_host+'/api/new_entity', {
            name: this.ent_inserts.ename
        },
        function (response, _this) {
          _this.search_entity(_this.ent_inserts.ename, response.data.eid);
          _this.ent_inserts.ename = "";
          _this.entDialogVisible = false;
        },
        function (response, _this) {
          _this.$message.error(response.data.msg);
        }
      )
    },

    checkAndSubmit(_this, url, pparams, succ_func, fail_func) {
      pparams["precheck"] = 1
      _this.axios
        .get(url, {
          params: pparams
        })
        .then(function (response) {
          if (response.data.status !== "ok") {
            fail_func(response, _this)
          } else {
            delete pparams["precheck"];
            _this.axios
              .get(url, {
                params: pparams
              })
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


    submitNewM2E() {
      this.checkAndSubmit(this, this.api_host+'/api/new_ment2ent', {
            mention: this.m2e_inserts.mention,
            eid: this.m2e_inserts.eid
        },
        function (response, _this) {
          _this.search_entity(_this.nowsearchStr);
          _this.m2e_inserts.mention = "";
          _this.m2eDialogVisible = false;
        },
        function (response, _this) {
          _this.$message.error(response.data.msg);
        }
      )
    },

    objectSelectEnt(obj_ename) {
      this.inserts.oname = obj_ename;
    },

    objectSuggestion(update_oid) {
      let _this = this;
      this.axios
        .get(this.api_host+'/api/ment2ent', {
          params: {
            q: this.inserts.oname,
            no_other_m: 1
          }
        })
        .then(function (response) {
          let ents = response.data.ret;
          let new_inserts = JSON.parse(JSON.stringify(_this.inserts)); //deepcopy
          new_inserts.options = [];
          ents.forEach(function (x) {
            let xlabel = x.ename;
            if (x.eid !== x.ename) xlabel += "<id:" + x.eid + ">"
            new_inserts.options.push({
              label: xlabel,
              value: xlabel
            });
          });
          new_inserts.options.push({
              label: '<不链接实体>',
              value: ''
          });
          if (update_oid) new_inserts.oid = "";
          _this.inserts = new_inserts;
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  },
  mounted() {
    if (this.searchStr === "") {
      this.search_entity(global.main_entity, null);
    }
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
    background-color:#F56C6C;
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
