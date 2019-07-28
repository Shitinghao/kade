<template>
  <div class="ment2ent">
    
  </div>
</template>

<script>
export default {
  name: 'Ment2Ent',
  data () {
    return {
      tripleData: []
    }
   },
  mounted() {
    this.axios
      .get('http://127.0.0.1:26551/api/ment2ent?q=%E5%A4%8D%E6%97%A6')
      .then(response => (this.tripleData = response.data.ret))
      .catch(function (error) { 
        console.log(error);
      });
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
