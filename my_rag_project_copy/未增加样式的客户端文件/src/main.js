import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
//注册router
import router from "./router"
const app = createApp(App)
app.use(router)

//全局配置axios请求
import axios from "axios"  //导入axios包
axios.defaults.baseURL = "http://localhost:8000/" //服务器请求路径公共部分，即后端接口，将前端对接到后端
axios.defaults.headers.post['Content-Type'] = 'application/json' //post请求发送json数据给服务器
axios.defaults.headers.put['Content-Type'] = 'application/json'  //put请求发送json数据给服务器
app.config.globalProperties.$axios = axios //挂载axios，使用$axios替代原生axios，全局变量名字$axios 值为axios

//注册elment-plus
import ElementPlus from 'element-plus'

// 注册md格式解析
// Markdown 配置
import { marked } from 'marked'
import DOMPurify from 'dompurify'

//  Markdown 配置
marked.setOptions({
  breaks: true,    // 支持换行
  gfm: true,       // GitHub 风格
  smartLists: true,
  smartypants: false
})

// Markdown 正则处理
function normalizeMarkdown(text) {
  return text
    .replace(/(#{1,6} )/g, '\n$1')
    .replace(/- /g, '\n- ')
}

// 全局 markdown 渲染方法
function renderMarkdown(text) {
  if (!text) return ''
  const rawHtml = marked.parse(normalizeMarkdown(text))
  return DOMPurify.sanitize(rawHtml)
}
app.config.globalProperties.$renderMarkdown = renderMarkdown

app.mount('#app')
