import {createApp}   from "vue";
import './style.css'
import App from './App.vue'


//创建对象
const app = createApp(App)

//注册路由对象
import router from './router'
app.use(router)  //给vue应用安装插件或功能扩展


//axios 全局配置
//客户端如何请求服务器得到服务器返回的数据
//我们使用 axios 库来实现，axios 库封装了 http 请求，可以用于快速的实现客户端向服务器发送请求且得到服务器的响应数据
//axis 使用步骤：
//
// 第一步：安装
//
// 第二步：全局配置【意义：少写一些重复性代码，比如服务器接口访问的公共路径部分、post请求设置请求体application/json部分】
import axios from "axios"  //导入axios包
axios.defaults.baseURL = "http://localhost:8080" //服务器请求路径公告部分
axios.defaults.headers.post['Content-Type'] = 'application/json' //post请求发送json数据给服务器
axios.defaults.headers.put['Content-Type'] = 'application/json'  //put请求发送json数据给服务器
app.config.globalProperties.$axios = axios //挂载axios，使用$axios替代原生axios
app.mount('#app')