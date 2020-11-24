<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Please <button @click="login">click here</button> to login..
    </p>
  </div>
</template>

<script>
import Auth from '@aws-amplify/auth';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
    login: function(){
      Auth.federatedSignIn({ provider: 'Auth0'});
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
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
