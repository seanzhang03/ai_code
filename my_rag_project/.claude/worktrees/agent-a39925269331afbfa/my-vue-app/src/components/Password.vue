<template>
  <div class="password-page">
    <el-card class="password-card" shadow="never">
      <!-- 卡片头部：logo + 标题 + 副标题 -->
      <template #header>
        <div class="password-header">
          <div class="logo">
            <el-icon><Lock /></el-icon>
          </div>
          <h2 class="password-title">修改密码</h2>
          <p class="password-subtitle">通过验证码或旧密码重置密码</p>
        </div>
      </template>

      <!-- Tab 导航：两种修改方式，绑定 activePasswordMethod -->
      <el-tabs v-model="activePasswordMethod" class="password-tabs" stretch>
        <!-- 通过邮箱验证码修改 -->
        <el-tab-pane label="验证码修改" name="captcha">
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

            <el-form-item label="新密码">
              <el-input v-model="new_password" type="password" :disabled="!isSend" placeholder="请输入新密码" size="large" show-password>
                <template #prefix><el-icon><Lock /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              class="password-btn"
              :disabled="(!isSend)||(!email.trim())||(!captcha.trim())||(!new_password.trim())"
              @click="changePasswordCaptcha"
            >修改密码</el-button>
          </el-form>
        </el-tab-pane>

        <!-- 通过旧密码修改 -->
        <el-tab-pane label="旧密码修改" name="password">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="邮箱号">
              <el-input v-model="email" placeholder="请输入邮箱号" size="large" clearable>
                <template #prefix><el-icon><Message /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-form-item label="旧密码">
              <el-input v-model="old_password" type="password" placeholder="请输入旧密码" size="large" show-password>
                <template #prefix><el-icon><Lock /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-form-item label="新密码">
              <el-input v-model="new_password" type="password" placeholder="请输入新密码" size="large" show-password>
                <template #prefix><el-icon><Lock /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              class="password-btn"
              :disabled="(!email.trim())||(!old_password.trim())||(!new_password.trim())"
              @click="changePasswordPassword"
            >修改密码</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";
//导入路由
import {useRouter} from "vue-router"

//实例
let proxy = getCurrentInstance().proxy

//定义路由对象
let router = useRouter()

//定义修改密码的方式
let activePasswordMethod = ref("")

//
let isSend = ref(false)

//定义邮箱、旧密码、新密码、验证码
let email=ref("")
let old_password=ref("")
let new_password=ref("")
let captcha = ref("")


//定义发送验证码函数
function sendCaptcha(){
  isSend.value = !isSend.value
  proxy.$axios({
    url:"password/sendCaptcha",
    method:"get",
    params:{
      email:email.value
    }
  }).then(res=>{
    if(res.data.code===200){
      alert("验证码已经发送，请查收")
      sessionStorage.setItem("nickname",res.data.data.nickname)
      sessionStorage.setItem("usersId",res.data.data.usersId)
    }
    else {
      alert(res.data.msg)
    }
  })
}

//通过旧密码修改新密码
function changePasswordPassword(){
  proxy.$axios({
    url:"password/changePasswordPassword",
    method:"post",
    data:JSON.stringify({
      email:email.value,
      old_password:old_password.value,
      new_password:new_password.value
    })
  }).then(res=>{
    if(res.data.code===200){
      alert("密码修改成功！下面跳转到登录页面！请重新登录")
      email.value=""
      old_password.value=""
      new_password.value=""
      setTimeout(()=>{router.push("/login")},1000)
    }
    else {
      alert(res.data.msg)
    }
  })
}

//通过验证码修改密码
function changePasswordCaptcha() {
  proxy.$axios({
    url: "password/changePasswordCaptcha",
    method: "post",
    data: JSON.stringify({
      email: email.value,
      captcha: captcha.value,
      new_password: new_password.value
    })
  }).then(res => {
    if(res.data.code===200){
      alert("密码修改成功！下面跳转到登录页面！请重新登录")
      email.value = ""
      captcha.value = ""
      new_password.value = ""
      setTimeout(()=>{router.push("/login")},1000)
    }
    else {
      alert(res.data.msg)
    }
  })
}
</script>

<style scoped>
.password-page {
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

.password-card {
  width: 420px;
  max-width: 100%;
  border: none;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 20px 45px -18px rgba(103, 78, 178, 0.35);
}

.password-card :deep(.el-card__header) {
  border-bottom: none;
  padding: 28px 24px 0;
}

.password-card :deep(.el-card__body) {
  padding: 12px 24px 28px;
}

/* 卡片头部 */
.password-header {
  text-align: center;
}

.password-header .logo {
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

.password-title {
  margin: 0;
  font-size: 22px;
  letter-spacing: 0.5px;
  color: #1f2333;
}

.password-subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8fa3;
}

/* Tab 激活态 */
.password-tabs :deep(.el-tabs__item) {
  font-size: 15px;
  color: #6b7280;
}

.password-tabs :deep(.el-tabs__item.is-active) {
  color: #7c5cfc;
  font-weight: 600;
}

.password-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #a855f7, #6d5ef0);
  height: 3px;
  border-radius: 3px;
}

.password-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: #f0eef5;
}

/* 表单间距与标签 */
.password-tabs :deep(.el-form-item) {
  margin-bottom: 18px;
}

.password-tabs :deep(.el-form-item__label) {
  color: #4b5164;
  font-weight: 500;
  padding-bottom: 6px;
}

/* 输入框圆角与聚焦态 */
.password-tabs :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.password-tabs :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #7c5cfc inset;
}

/* 验证码右侧「发送验证码」按钮 */
.password-tabs :deep(.el-input-group__append) {
  border-radius: 0 10px 10px 0;
  background: #fbfaff;
}

.password-tabs :deep(.el-input-group__append .el-button) {
  color: #7c5cfc;
  font-weight: 500;
}

/* 修改密码按钮 */
.password-btn {
  width: 100%;
  margin-top: 4px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.password-btn:not(.is-disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 22px -10px rgba(124, 92, 252, 0.65);
}

/* 小屏适配 */
@media (max-width: 480px) {
  .password-card {
    width: 100%;
  }
  .password-title {
    font-size: 20px;
  }
}
</style>
