<template>
  <div class="login-page">
    <el-card class="login-card" shadow="never">
      <!-- 卡片头部：logo + 标题 + 副标题 -->
      <template #header>
        <div class="login-header">
          <div class="logo">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <h2 class="login-title">用户登录</h2>
          <p class="login-subtitle">欢迎回来，请选择登录方式</p>
        </div>
      </template>

      <!-- Tab 导航：三种登录方式，绑定 activeLoginMethod -->
      <el-tabs v-model="activeLoginMethod" class="login-tabs" stretch>
        <!-- 通过邮箱验证码登录 -->
        <el-tab-pane label="验证码登录" name="captcha">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="邮箱号">
              <el-input v-model="email" :disabled="isSend" placeholder="请输入邮箱号" size="large" clearable>
                <template #prefix><el-icon><Message /></el-icon></template>
              </el-input>
            </el-form-item>
            <el-form-item label="验证码">
              <el-input v-model="captcha" :disabled="!isSend" placeholder="请输入验证码" size="large" clearable>
                <template #prefix><el-icon><Key /></el-icon></template>
                <template #append>
                  <el-button :disabled="isSend" @click="sendCaptcha">发送验证码</el-button>
                </template>
              </el-input>
            </el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :disabled="!isSend"
              @click="loginByEmailCaptcha"
            >登 录</el-button>
          </el-form>
        </el-tab-pane>

        <!-- 通过邮箱密码登录 -->
        <el-tab-pane label="邮箱密码" name="email_password">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="邮箱号">
              <el-input v-model="email" placeholder="请输入邮箱号" size="large" clearable>
                <template #prefix><el-icon><Message /></el-icon></template>
              </el-input>
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="password" type="password" placeholder="请输入密码" size="large" show-password>
                <template #prefix><el-icon><Lock /></el-icon></template>
              </el-input>
            </el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :disabled="(!email.trim()) || (!password.trim())"
              @click="loginByEmailPassword"
            >登 录</el-button>
          </el-form>
        </el-tab-pane>

        <!-- 通过用户名密码登录 -->
        <el-tab-pane label="用户名密码" name="nickname_password">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="用户名">
              <el-input v-model="nickname" placeholder="请输入用户名" size="large" clearable>
                <template #prefix><el-icon><User /></el-icon></template>
              </el-input>
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="password" type="password" placeholder="请输入密码" size="large" show-password>
                <template #prefix><el-icon><Lock /></el-icon></template>
              </el-input>
            </el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :disabled="(!nickname.trim()) || (!password.trim())"
              @click="loginByNicknamePassword"
            >登 录</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>


<script setup>
import {ref, getCurrentInstance, onMounted} from "vue"; //getCurrentInstance是用来获取当前实例
//请求服务器时，服务器ip端口协议都固定，只是后面路径不同，一旦服务器端口更改，页面上每一处代码都要修改，将这些抽取出来作为公共的全局配置
//全局配置写在main.js中，用getCurrentInstance调用
//onMounted有些东西不需要人为操作，让其自动执行

//导入路由
import {useRouter} from "vue-router"

//导入element-plus
import {ElMessage} from 'element-plus'

//定义路由对象
let router = useRouter()

//获取实例对象 -- 来访问全局配置的内容
let proxy = getCurrentInstance().proxy

//定义变量：邮箱、验证码、昵称、用户手动输入的密码
let email = ref("")
let captcha = ref("")
let nickname = ref("")
let password = ref("")

//是否可以发送，默认为不可发送，控制邮箱号、验证码、发送按钮、登录按钮的显示与隐藏
let isSend = ref(false)

//定义通过哪种方式来登录
let activeLoginMethod = ref("")


//定义发送验证码函数
function sendCaptcha(){
  isSend.value = !isSend.value
  proxy.$axios({
    url:"login/sendCaptcha",
    method:"get",  //设置请求方式
    params:{//get请求设置客户端给服务器的参数params，键值对格式，其中键要和服务器的一致
      email:email.value  //前面是后端的参数名，后面是前端的参数名，目的就是把前端的参数值传到后端去
    }
  }).then(res=>{//.then来得到服务器响应返回的数据，res就是接受响应的内容对象[形参]，等价于function a(res){}，调用一个函数之后，函数有返回值如何来处理这个返回值
    console.log(res)
    if(res.data.code===200) {
      alert("验证码已经发送！")
      ElMessage.success("验证码已发送，请查收")
      //把nickname存储在本地，用sessionStorage，临时来存储键值对数据
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
  }
    else{
      ElMessage.error(res.data.msg)
    }
      }
    )
}

//邮箱验证码登录函数
function loginByEmailCaptcha(){
  proxy.$axios({
    url:"login/loginByEmailCaptcha",
    method:"post",
    data:JSON.stringify({  //stringify将JS对象转换为JSON
      email:email.value,
      captcha:captcha.value,
    }),
  }).then(res=>{
    if(res.data.code ===200){
      alert("登录成功！")
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("token",res.data.token)
      //过多少毫秒执行一次函数，跳转到聊天页面
      setTimeout(()=>{router.push("/chat")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}

//邮箱密码登录函数
function loginByEmailPassword(){
  proxy.$axios({
    url:"login/loginByEmailPassword",
    method:"post",
    data:JSON.stringify({  //stringify将JS对象转换为JSON
      email:email.value,
      password:password.value,
    }),
  }).then(res=>{
    if(res.data.code ===200){
      alert("登录成功！")
      //临时存储
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("token",res.data.token)
      //过多少毫秒执行一次函数，跳转到聊天页面
      setTimeout(()=>{router.push("/chat")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}

//用户名密码登录函数
function loginByNicknamePassword(){
  proxy.$axios({
    url:"login/loginByNicknamePassword",
    method:"post",
    data:JSON.stringify({  //stringify将JS对象转换为JSON
      nickname:nickname.value,
      password:password.value,
    }),
  }).then(res=>{
    if(res.data.code ===200){
      //临时存储
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
      sessionStorage.setItem("role",res.data.data.role)
      sessionStorage.setItem("token",res.data.token)
      alert("登录成功！")
      //过多少毫秒执行一次函数，跳转到聊天页面
      setTimeout(()=>{router.push("/chat")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}

</script>

<style scoped>
.login-page {
  min-height: 100svh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  box-sizing: border-box;
  background:
    radial-gradient(circle at 12% 18%, rgba(170, 59, 255, 0.14), transparent 42%),
    radial-gradient(circle at 88% 82%, rgba(86, 114, 255, 0.14), transparent 42%),
    linear-gradient(160deg, #f5f6ff 0%, #fbf5ff 48%, #eef2fb 100%);
}

.login-card {
  width: 420px;
  max-width: 100%;
  border: none;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 20px 45px -18px rgba(103, 78, 178, 0.35);
}

.login-card :deep(.el-card__header) {
  border-bottom: none;
  padding: 28px 24px 0;
}

.login-card :deep(.el-card__body) {
  padding: 12px 24px 28px;
}

/* 卡片头部 */
.login-header {
  text-align: center;
}

.login-header .logo {
  width: 56px;
  height: 56px;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  font-size: 30px;
  color: #fff;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  box-shadow: 0 10px 20px -8px rgba(124, 92, 252, 0.6);
}

.login-title {
  margin: 0;
  font-size: 22px;
  letter-spacing: 0.5px;
  color: #1f2333;
}

.login-subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8fa3;
}

/* Tab 激活态 */
.login-tabs :deep(.el-tabs__item) {
  font-size: 15px;
  color: #6b7280;
}

.login-tabs :deep(.el-tabs__item.is-active) {
  color: #7c5cfc;
  font-weight: 600;
}

.login-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #a855f7, #6d5ef0);
  height: 3px;
  border-radius: 3px;
}

.login-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: #f0eef5;
}

/* 表单间距与标签 */
.login-tabs :deep(.el-form-item) {
  margin-bottom: 18px;
}

.login-tabs :deep(.el-form-item__label) {
  color: #4b5164;
  font-weight: 500;
  padding-bottom: 6px;
}

/* 输入框圆角与聚焦态 */
.login-tabs :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.login-tabs :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #7c5cfc inset;
}

/* 验证码右侧「发送验证码」按钮 */
.login-tabs :deep(.el-input-group__append) {
  border-radius: 0 10px 10px 0;
  background: #fbfaff;
}

.login-tabs :deep(.el-input-group__append .el-button) {
  color: #7c5cfc;
  font-weight: 500;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  margin-top: 4px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.login-btn:not(.is-disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 22px -10px rgba(124, 92, 252, 0.65);
}

/* 小屏适配 */
@media (max-width: 480px) {
  .login-card {
    width: 100%;
  }
  .login-title {
    font-size: 20px;
  }
}
</style>
