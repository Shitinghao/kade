<template>
  <div class="hello">
    <nav></nav>
    <h1>{{ msg }}</h1>
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
      msg: 'Welcome to Kade'
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
</style>
