import Vue from 'vue'
import App from './views/App.vue'
import Logout from './views/Logout.vue'
import Admin from './views/Admin.vue'
import NotFound from './views/NotFound.vue'
import Amplify from 'aws-amplify';
import '@aws-amplify/ui-vue';
//import aws_exports from './aws-exports';
import dev_cfg from './dev-cfg.js';

Amplify.configure(dev_cfg.awsConfig);

Vue.config.productionTip = false

/*new Vue({
  render: h => h(App),
}).$mount('#app')
*/

const routes = {
  '/': App,
  '/callback': Admin, // How can I lock down this route to an authenticated session?
  '/logout': Logout,
  '/error': NotFound
}

new Vue({
  el: '#app',
  data: {
    currentRoute: window.location.pathname
  },
  computed: {
    ViewComponent () {
      return routes[this.currentRoute] || NotFound
    }
  },
  render (h) { return h(this.ViewComponent) }
})
