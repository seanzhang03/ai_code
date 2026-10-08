<template>
  <div class="register-page">
    <el-card class="register-card" shadow="never">
      <!-- 卡片头部：logo + 标题 + 副标题 -->
      <template #header>
        <div class="register-header">
          <div class="logo">
            <el-icon><UserFilled /></el-icon>
          </div>
          <h2 class="register-title">用户注册</h2>
          <p class="register-subtitle">创建账号，开启对话之旅</p>
        </div>
      </template>

      <!-- 注册表单：邮箱 / 密码 / 确认密码 / 用户名 -->
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

        <el-form-item label="确认密码">
          <el-input v-model="again_password" type="password" placeholder="请再次输入密码" size="large" show-password>
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>

        <el-form-item label="用户名">
          <el-input v-model="nickname" placeholder="请输入用户名" size="large" clearable>
            <template #prefix><el-icon><User /></el-icon></template>
          </el-input>
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="register-btn"
          :disabled="((!email.trim())||(!password.trim())||(!again_password.trim())||(!nickname.trim())||(!(password==again_password)))"
          @click="registration"
        >注 册</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";

//导入路由
import {useRouter} from "vue-router"

//定义注册需要的邮箱、密码和用户名
let email = ref("")
let password = ref("")
let nickname = ref("")

//定义第二次输入的密码，两次密码一致才允许注册
let again_password = ref("")

//获取实例对象
let proxy =getCurrentInstance().proxy

//定义路由对象
let router = useRouter()

function registration(){
  proxy.$axios({
    url:"registration/registration",
    method:"post",
    data:JSON.stringify({
      email:email.value,
      password:password.value,
      nickname:nickname.value
    }),
  }).then(res=>{
    if (res.data.code === 200){
      alert("注册成功!")
      //跳转到登录页面
      setTimeout(()=>{router.push("/login")},1000)
    }
    else{
      alert(res.data.msg)
    }
  })
}
</script>

<style scoped>
.register-page {
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

.register-card {
  width: 420px;
  max-width: 100%;
  border: none;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 20px 45px -18px rgba(103, 78, 178, 0.35);
}

.register-card :deep(.el-card__header) {
  border-bottom: none;
  padding: 28px 24px 0;
}

.register-card :deep(.el-card__body) {
  padding: 12px 24px 28px;
}

/* 卡片头部 */
.register-header {
  text-align: center;
}

.register-header .logo {
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

.register-title {
  margin: 0;
  font-size: 22px;
  letter-spacing: 0.5px;
  color: #1f2333;
}

.register-subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8fa3;
}

/* 表单间距与标签 */
:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__label) {
  color: #4b5164;
  font-weight: 500;
  padding-bottom: 6px;
}

/* 输入框圆角与聚焦态 */
:deep(.el-input__wrapper) {
  border-radius: 10px;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #7c5cfc inset;
}

/* 注册按钮 */
.register-btn {
  width: 100%;
  margin-top: 4px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.register-btn:not(.is-disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 22px -10px rgba(124, 92, 252, 0.65);
}

/* 小屏适配 */
@media (max-width: 480px) {
  .register-card {
    width: 100%;
  }
  .register-title {
    font-size: 20px;
  }
}
</style>
