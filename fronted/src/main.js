import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online! ! !
 */
import axios from './config/http.js'

import { mockXHR } from '../mock'
if (process.env.NODE_ENV === 'production') {
  mockXHR()
}

// set ElementUI lang to EN
Vue.use(ElementUI, { locale })

//  this.$http 引用axios
Vue.prototype.$axios = axios

Vue.config.productionTip = false

//  创建websocket连接  用来接收服务端推送的实时异常地点数据
// function connectSocket(host)
// {
//     window.webSocket = new WebSocket(host);
//     /*建立连接*/
//     webSocket.onopen = evt => {
//       console.log("webSocket连接成功");
//       let data = {type: 'bind'};
//       let json = JSON.stringify(data);
//       webSocket.send(json);
//     };
//     /*连接关闭*/
//     webSocket.onclose = evt => {
//       console.log("webSocket连接关闭");
//     };
//     /*接收服务器推送消息*/
//     webSocket.onmessage = evt => {
//       let data = JSON.parse(evt.data);
//       console.log(data)
//     };
//     /*连接发生错误时*/
//     webSocket.onerror = (evt,e) => {
//       console.log(evt);
//     }
// }
//
// Vue.prototype.$connectSocket= connectSocket("ws://localhost:8080/realtime");


new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
