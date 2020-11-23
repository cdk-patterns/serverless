<template>
  <div class="hello">
    <h1>Nice Login...</h1>
    <h2>Our Hit Counter</h2>
    <p>
      Here is the current value for the number of <br />
      <b>Hits stored in our DynamoDB [{{ hitsCount }}]</b>
    </p>
    <p>
      <button @click="getHits">Increase Hits</button>
    </p>
  </div>
</template>

<script>
import API from "@aws-amplify/api";

export default {
  name: "HitsCounter",
  data() {
    return {
      hitsCount: 0,
      apiName: "hitsapi",
    };
  },
  methods: {
    getHits: async function () {
      try {
        const response = await API.get(this.apiName, "/hits");
        this.HitsCounter = response[0].hits;
      } catch (err) {
        console.log(err);
      }
    },
  },
  created() {
    this.getHits();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: circle;
  padding: 0;
}
li {
  padding-left: 16px;
}
li:before {
  content: "•"; /* Insert content that looks like bullets */
  padding-right: 8px;
  color: blue; /* Or a color you prefer */
}
a {
  color: #42b983;
}
</style>
