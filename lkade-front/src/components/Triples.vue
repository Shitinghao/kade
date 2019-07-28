<template>
  <div class="triples">
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="18">
        <el-input type="text" :name="searchStr" v-model="searchStr" placeholder="搜索" suffix-icon="el-icon-search"></el-input>
        <el-button @click="search_entity(null)">搜索</el-button>

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

        <hr />

        <el-button type="info" @click="dialogVisible=true">新增关系</el-button>

        <el-dialog title="新增关系" :visible.sync="dialogVisible" width="50%">
          Subject: <el-input type="text" v-model="inserts.sid" placeholder=""></el-input>
          Predicate: <el-input type="text" v-model="inserts.p" placeholder=""></el-input>
          Object: <el-input type="text" v-model="inserts.oid" placeholder=""></el-input>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible=false">取 消</el-button>
            <el-button type="primary" @click="submitInsertTriple">确 定</el-button>
          </span>
        </el-dialog>

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
                  <el-button type="danger"  size="medium" @click="handleRemove(remove_triple, scope.row.id)">删除</el-button>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" :content="scope.row.id" placement="top-end" v-if="scope.row.id !== ''">
                  <el-button type="info" size="medium" @click="modify_triple(scope.row.id)">修改</el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
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
      tripleData: [],
      ment2entData: [],
      msgStr: '',
      nowsearchStr: '',
      dialogVisible: false,
      inserts: {sid: '', p: '', oid: '', old_tid: ''}
    }
  },
  methods: {
    search_entity(queryStr) {
      if (queryStr !== null) this.searchStr = queryStr;
      this.axios
        .get('http://127.0.0.1:26551/api/triples', {
          params: {
            entity: this.searchStr
          }
        })
        .then(response => (this.tripleData = response.data.ret))
        .catch(function (error) {
          console.log(error);
        });
      this.axios
        .get('http://127.0.0.1:26551/api/ment2ent', {
          params: {
            q: this.searchStr
          }
        })
        .then(response => (this.ment2entData = response.data.ret))
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
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
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
</style>
