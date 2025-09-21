import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false

//These values are replaces during amplify setup
axios.defaults.baseURL = "https://6qm0yrcpf0.execute-api.us-east-1.amazonaws.com/prod"
Vue.prototype.$UserPoolId = 'us-east-1_m2riVcmx2'
Vue.prototype.$ClientId = '6cpukv1nuc591iloervot1irii'

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

new Vue({
router,
  render: h => h(App),

}).$mount('#app')
