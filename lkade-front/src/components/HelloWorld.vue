<template>
  <div class="hello">
    <nav></nav>
    <h1 style="margin: 60px 0;">{{ msg }}</h1>
    <!--<h2>Essential Links</h2>-->
    <Triples></Triples>
  </div>
</template>

<script>
import Triples from './Triples.vue'
export default {
  name: 'HelloWorld',
  components: {
    Triples
  },
  data () {
    return {
      msg: '数据表视图'
    }
  },
  created(){
    console.log($);
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
