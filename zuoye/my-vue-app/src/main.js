import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')


import axios from "axios"  //导入axios包
axios.defaults.baseURL = "http://localhost:8080" //服务器请求路径公告部分
axios.defaults.headers.post['Content-Type'] = 'application/json' //post请求发送json数据给服务器
axios.defaults.headers.put['Content-Type'] = 'application/json'  //put请求发送json数据给服务器
app.config.globalProperties.$axios = axios //挂载axios，使用$axios替代原生axios
app.mount('#app')