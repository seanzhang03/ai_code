<template>
  <!-- 使用 flex 布局让表单在页面中居中 -->
  <div class="login-container">
    <!-- 使用 el-card 作为登录卡片容器，增加阴影和圆角 -->
    <el-card class="login-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>用户登录</span>
        </div>
      </template>

      <!-- 使用 el-form 替代原生 form，增加 label-position 控制标签位置 -->
      <el-form label-position="top" @submit.prevent>
        <!-- 邮箱输入框 -->
        <el-form-item label="邮箱号">
          <el-input
            v-model="email"
            placeholder="请输入邮箱地址"
            :disabled="isSend"
            clearable
          />
        </el-form-item>

        <!-- 验证码输入框 -->
        <el-form-item label="验证码">
          <el-input
            v-model="captcha"
            placeholder="请输入验证码"
            :disabled="!isSend"
            clearable
          />
        </el-form-item>

        <!-- 按钮组：使用 flex 布局让两个按钮并排或上下排列 -->
        <div class="login-actions">
          <el-button
            type="primary"
            :disabled="isSend"
            @click="sendCaptcha"
            class="action-btn"
          >
            发送验证码
          </el-button>
          <el-button
            type="success"
            :disabled="!isSend"
            @click="login"
            class="action-btn"
          >
            登录
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";//getCurrentInstance获取当前实例
//请求服务器时，服务器的ip端口协议都是固定的，只是后面的路径不一样，一旦服务器端口发生更改，页面上每一处代码都要更改，将这些抽取出来成为一个公共的全局配置
//全局配置写在main.js里面，用getCurrentInstance来调用
//onMounted有些东西不需要人为操作，让其自动执行

//导入路由
import {useRouter} from "vue-router";

//导入element plus
import {ElMessage} from 'element-plus'

//定义路由对象
let router = new useRouter()

//获取实例对象--用来访问全局配置的内容
let proxy = getCurrentInstance().proxy

//定义一个变量控制邮箱号、验证码、发送按钮、登录按钮的显示与隐藏
let isSend = ref(false)

//定义两个变量：邮箱号、验证码
let email = ref("")
let captcha = ref("")

//发送验证码
function sendCaptcha(){
    isSend.value=!isSend.value //必须要加.value，直接访问这个对象访问不到其值

    proxy.$axios({ //使用全局配置的axios，客户端去访问服务器里面的数据
      url:"users/sendCaptcha",  //服务器里的url地址，访问的接口地址，默认拼接
      method:"get", //设置请求方式，默认get
      params:{  //get请求设置客户端给服务器的参数parms，键值对格式，其中键和服务器的要一致
        email:email.value,
      }
    }).then(res =>{  //.then来得到服务器响应返回的数据，res就是接受响应的内容对象[形参]，等价于function a(res){}，调用一个函数之后，函数有返回值，如何来处理这个返回值
      //let data =res.data
      console.log(res)
      if (res.data.code === 200){
        ElMessage.success("验证码已发送，请查收")
        //把nickname存储在本地存储中，用sessionStorage,临时存储键值对的数据
        sessionStorage.setItem("nickname",res.data.data.nickname)  //setItem存值，getItem取值，将后面的值赋给前面这个键对应的值
        sessionStorage.setItem("usersId",res.data.data.usersId)
        //返回的是一个data对象，里面含有code、msg和data三个变量，其中data包含的是返回的昵称
      }
      else{
        ElMessage.error(res.data.msg)  //失败返回对应响应码
      }

    })
}

//登录函数
function login(){ //传2个参数给服务器:email、code
  proxy.$axios({ //发送请求
    url:"users/login", //服务器里面没写url
    method:"post",  //post请求方式，发送的json数据
    data: JSON.stringify({  //JSON.stringify将JS对象转换为为JSON
      email:email.value,
      captcha:captcha.value,
    }),          //post请求设置json参数需要data属性
  }).then (res=>{ //处理请求结果
    if(res.data.code === 200){
      alert("登录成功！")
      //过多少毫秒执行一次函数,跳转到聊天页面
      setTimeout(()=>{router.push("/chat") },1000) //参数为执行的函数和等待时间

    }
    else{
      alert(res.data.msg)
    }
  })

}
</script>

<style scoped>
/* 页面整体背景与居中布局 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5; /* 浅灰色背景 */
}

/* 登录卡片样式 */
.login-card {
  width: 400px;
  border-radius: 8px;
}

/* 卡片头部样式 */
.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

/* 按钮组布局 */
.login-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

/* 按钮宽度均分 */
.action-btn {
  flex: 1;
  margin-right: 10px;
}

.action-btn:last-child {
  margin-right: 0;
}
</style>