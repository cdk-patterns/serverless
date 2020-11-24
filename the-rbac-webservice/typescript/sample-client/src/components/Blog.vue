<template>
<!-- It would be neat to alternate the content of this blog based on the user jwt roles attr -->
  <div class="hello">
    <h1>Nice Login...</h1>
    <p>User Logged in: Placeholder</p>
    <h3>Mini Blog Idea</h3>
    <p>
      <label>What would you call your Blog?</label><br/> 
      <input
        type="text"
        id="title"
        class="form-control"
        v-model="formData.blog.title"
      />
      <br />
      <label>What would it be about?</label><br/>
      <input
        type="text"
        id="outline"
        class="form-control"
        v-model="formData.blog.outline"
      />
    </p>
    <p>
      <button @click="saveBlog">Record My Awesome Blog Thoughts..</button>
    </p>
  </div>
</template>

<script>
import API from "@aws-amplify/api";

export default {
  name: "HitsCounter",
  data() {
    return {
      apiName: "blogApi",
      userName: "",
      blogs: [],
      formData: {
        blog: {
          title: "enter here",
          outline: "enter here",
        },
      },
    };
  },
  methods: {
    getBlogs: async function () {
      try {
        const response = await API.get(this.apiName, "/blogs");
        this.blogs = response[0].blogs;
      } catch (err) {
        console.log(err);
      }
    },
    saveBlog: async function () {
      try {
        alert("Wow I love this idea");
        const response = await API.put(this.apiName, "/blogs", {
          body: {
              title: this.formData.blog.title,
              outline: this.formData.blog.outline,
          },
        });
        this.blogs = response[0].blogs;
      } catch (err) {
        console.log(err);
      }
    },
  },
  created() {
    this.getBlogs();
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
