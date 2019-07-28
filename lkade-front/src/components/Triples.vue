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
            <el-table-column prop="oper" label="Operation" width="180">
            </el-table-column>
          </el-table>
        </div>

        <hr/>

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
            <el-table-column prop="oper" label="Operation" width="180">
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
      ment2entData: []
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
