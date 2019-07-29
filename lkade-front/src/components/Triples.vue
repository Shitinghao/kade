<template>
  <div class="triples">
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="18">
        <el-input type="text" :name="searchStr" v-model="searchStr" placeholder="搜索" suffix-icon="el-icon-search" style="width:80%" ></el-input>
        <el-button @click="search_entity(null)">搜索</el-button>

        <div class="grid-content content_style">
          <el-table :data="entityData" style="width: 100%" :default-sort="{prop: 'eid', order: 'descending'}" center="True">
            <el-table-column label="Entity" sortable>
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end">
                  <a @click="search_entity(scope.row.eid)" class="buttonText">{{scope.row.ename}}</a>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="Operation" width="180">
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end" v-if="scope.row.eid !== ''">
                  <el-button type="danger" size="medium" @click="handleRemove(remove_entity, scope.row.id)">删除</el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <hr/>

       <div class="content_style">
         <div style="">
           <el-button type="info" @click="entDialogVisible=true" style="float: right;">新增实体</el-button>
           <el-dialog title="新增实体" :visible.sync="entDialogVisible" width="50%" :before-close="handleClose">
             <label for="" style="float: left;">name:</label>
             <el-input type="text" v-model="ent_inserts.ename" placeholder="请输入新增实体：name"></el-input>
             <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible=false">取 消</el-button>
            <el-button type="primary" @click="submitInsertTriple">确 定</el-button>
          </span>
           </el-dialog>
         </div>
         <div class="grid-content">
           <el-table :data="ment2entData" style="width: 100%" :default-sort="{prop: 'eid', order: 'descending'}" center="True">
             <el-table-column prop="mention" label="Mention" sortable>
             </el-table-column>
             <el-table-column label="Entity" sortable>
               <template slot-scope="scope">
                 <el-tooltip class="item" effect="dark" :content="scope.row.eid" placement="top-end">
                   <a @click="search_entity(scope.row.eid)" class="buttonText">{{scope.row.ename}}</a>
                 </el-tooltip>
               </template>
             </el-table-column>
             <el-table-column label="Operation" width="180">
               <template slot-scope="scope">
                 <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                   <el-button type="danger" size="medium" @click="handleRemove(remove_ment2ent, scope.row.id)">删除</el-button>
                 </el-tooltip>
               </template>
             </el-table-column>
           </el-table>
         </div>
       </div>

        <hr/>
       <div class="content_style">


        <div class="btn-group">
          <el-button type="info" @click="dialogVisible=true" style="float: right;">新增关系</el-button>

          <el-dialog title="新增关系" :visible.sync="dialogVisible" width="50%" :before-close="handleClose">
            <div class="input_style">
              <label for="" style="float: left;">Subject: </label>
              <el-input type="text" v-model="inserts.sid" placeholder="" :disabled="true"></el-input>
            </div>
            <div class="input_style">
              <label for="" style="float: left;"> Predicate:</label>
              <el-input type="text" v-model="inserts.p" placeholder=""></el-input>
            </div>
            <div class="input_style">
              <label for="" style="float: left;"> Object:</label>
              <el-input type="text" v-model="inserts.oid" placeholder=""></el-input>
            </div>
            <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible=false">取 消</el-button>
            <el-button type="primary" @click="submitInsertTriple">确 定</el-button>
          </span>
          </el-dialog>
        </div>


        <div class="grid-content">
          <el-table :data="tripleData" style="width: 100%" :default-sort="{prop: 'p', order: 'descending'}" center="True">
            <el-table-column prop="s" label="Subject" sortable>
            </el-table-column>
            <el-table-column prop="p" label="Predicate" sortable>
            </el-table-column>
            <el-table-column label="Object">
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.oid" placement="top-end" v-if="scope.row.oid !== ''">
                  <a @click="search_entity(scope.row.oid)" class="buttonText">{{scope.row.oname}}</a>
                </el-tooltip>
                <span v-if="scope.row.oid === ''">{{scope.row.oname}}</span>
              </template>
            </el-table-column>
            <el-table-column label="Operation" width="180">
              <template slot-scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                  <el-button type="danger" size="medium" @click="handleRemove(remove_triple, scope.row.id)">删除</el-button>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                  <el-button type="info" size="medium" @click="modify_triple(scope.row.id)">修改</el-button>
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
export default {
  name: 'Triples',
  data () {
    return {
      searchStr: '',
      entityData: [],
      tripleData: [],
      ment2entData: [],
      msgStr: '',
      nowsearchStr: '',
      dialogVisible: false,
      entDialogVisible: false,
      inserts: { sid: '', p: '', oid: '', old_tid: '' },
      ent_inserts: { ename: '' }
    }
  },
  methods: {
    search_entity(queryStr) {
      if (queryStr !== null) this.searchStr = queryStr;
      let _this = this;
      this.axios
        .get('http://127.0.0.1:26551/api/triples', {
          params: {
            entity: this.searchStr
          }
        })
        .then(function (response) {
          _this.tripleData = response.data.ret;
          if (response.data.ret.length > 0) {
            _this.inserts = { sid: response.data.ret[0].s, p: '', oid: '', old_tid: '' };
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      this.axios
        .get('http://127.0.0.1:26551/api/ment2ent', {
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
          });
        })
        .catch(function (error) { 
          console.log(error);
        });
      this.nowsearchStr = this.searchStr;
    },
    modify_triple(tid) {
      let thetriple = this.tripleData.filter(elem => (elem.id === tid));
      if (thetriple.length === 1) {
        this.inserts = {
          sid: thetriple[0].s,
          p: thetriple[0].p,
          oid: thetriple[0].oname,
          old_tid: tid
        }
      }
      this.dialogVisible = true;
    },
    remove_triple(tid) {
      let _this = this;
      this.axios
        .get('http://127.0.0.1:26551/api/removetriple', {
          params: {
            id: tid
          }
        })
        .then(function (response) {
          _this.msgStr = response.data.ret;
          _this.search_entity(_this.nowsearchStr);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    remove_ment2ent(tid) {
      let _this = this;
      this.axios
        .get('http://127.0.0.1:26551/api/removement2ent', {
          params: {
            id: tid
          }
        })
        .then(function (response) {
          _this.msgStr = response.data.ret;
          _this.search_entity(_this.nowsearchStr);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    remove_entity(tid) {
      let _this = this;
      this.axios
        .get('http://127.0.0.1:26551/api/removeentity', {
          params: {
            id: tid
          }
        })
        .then(function (response) {
          _this.msgStr = response.data.ret;
          _this.search_entity(_this.nowsearchStr);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleClose(done) {
      this.inserts.p = "";
      this.inserts.oid = "";
      this.inserts.old_tid = "";
      done();
    },
    handleRemove(func, fid) {
      this.$confirm('确认删除？')
        .then(_ => {
          func(fid);
        })
        .catch(_ => {});
    },
    submitInsertTriple() {
      this.dialogVisible = false;
      let _this = this;
      if (this.inserts.old_tid !== "") {
        this.remove_triple(this.inserts.old_tid);
        this.inserts.old_tid = "";
      }
      this.axios
        .get('http://127.0.0.1:26551/api/newtriple', {
          params: {
            sid: this.inserts.sid,
            p: this.inserts.p,
            oid: this.inserts.oid
          }
        })
        .then(function (response) {
          _this.msgStr = response.data.ret;
          _this.search_entity(_this.nowsearchStr);
          _this.inserts = { sid: '', p: '', oid: '', old_tid: '' };
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  },
  mounted() {
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
</style>
