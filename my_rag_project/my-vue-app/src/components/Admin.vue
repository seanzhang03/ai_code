<template>
  <div class="admin-page">
    <el-card class="admin-card" shadow="never">
      <!-- 卡片头部：标题 + 副标题 -->
      <template #header>
        <div class="admin-header">
          <div class="logo">
            <el-icon><Promotion /></el-icon>
          </div>
          <h2 class="admin-title">管理员模块</h2>
          <p class="admin-subtitle">用户管理功能</p>
        </div>
      </template>

      <!-- Tab 导航：三种操作，绑定 activeAdminMethod -->
      <el-tabs v-model="activeAdminMethod" class="admin-tabs" stretch>
        <!-- 创建用户 -->
        <el-tab-pane label="创建用户" name="create">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="邮箱号">
              <el-input v-model="email" placeholder="请输入邮箱号" size="large" clearable>
                <template #prefix><el-icon><Message /></el-icon></template>
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
              class="admin-btn"
              :disabled="(!email.trim())||(!nickname.trim())"
              @click="createUsers"
            >创建用户</el-button>
          </el-form>
        </el-tab-pane>

        <!-- 初始化密码 -->
        <el-tab-pane label="初始化密码" name="init">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="用户名">
              <el-input v-model="nickname" placeholder="请输入用户名" size="large" clearable>
                <template #prefix><el-icon><User /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              class="admin-btn"
              :disabled="!nickname.trim()"
              @click="initPassword"
            >初始化该用户密码</el-button>
          </el-form>
        </el-tab-pane>

        <!-- 删除用户 -->
        <el-tab-pane label="删除用户" name="delete">
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="用户名">
              <el-input v-model="nickname" placeholder="请输入用户名" size="large" clearable>
                <template #prefix><el-icon><User /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-button
              type="danger"
              size="large"
              class="admin-btn"
              :disabled="!nickname.trim()"
              @click="deleteUsers"
            >删除该用户</el-button>
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

//定义管理员进行什么操作
let activeAdminMethod = ref("")

//定义邮箱和用户名、token
let email = ref("")
let nickname = ref("")
let token = ref("")
token.value = sessionStorage.getItem("token")

//实例
let proxy = getCurrentInstance().proxy

//定义路由对象
let router = useRouter()

function createUsers(){
  proxy.$axios({
    url:"admin/createUsers",
    method:"post",
    //headers携带token
    headers: {
      "Authorization": `Bearer ${token.value}`
    },
    data:JSON.stringify({
      email:email.value,
      nickname:nickname.value
    }),
  }).then(res=>{
    if(res.data.code===200){
      alert("创建用户成功！即将跳转回管理员界面！")
      nickname.value = ""
      setTimeout(()=>{router.push("/admin")},1000)
    }
    else{
      alert(res.data.msg)
      nickname.value = ""
    }
  })
}

function initPassword(){
  proxy.$axios({
    url:"admin/initPassword",
    method:"post",
    headers: {
      "Authorization": `Bearer ${token.value}`
    },
    data:JSON.stringify({
      nickname:nickname.value
    }),
  }).then(res=>{
    if(res.data.code===200){
      alert("重置用户密码成功！初始密码为:123456。即将跳转回管理员界面！")
      nickname.value = ""
      setTimeout(()=>{router.push("/admin")},1000)
    }
    else{
      alert(res.data.msg)
      nickname.value = ""
    }
  })
}

function deleteUsers(){
  proxy.$axios({
    url:"admin/deleteUsers",
    method:"post",
    headers: {
      "Authorization": `Bearer ${token.value}`
    },
    data:JSON.stringify({
      nickname:nickname.value
    }),
  }).then(res=>{
    if(res.data.code===200){
      alert("删除用户成功！即将跳转回管理员界面！")
      nickname.value = ""
      setTimeout(()=>{router.push("/admin")},1000)
    }
    else{
      alert(res.data.msg)
      nickname.value = ""
    }
  })
}

</script>

<style scoped>
.admin-page {
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

.admin-card {
  width: 420px;
  max-width: 100%;
  border: none;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 20px 45px -18px rgba(103, 78, 178, 0.35);
}

.admin-card :deep(.el-card__header) {
  border-bottom: none;
  padding: 28px 24px 0;
}

.admin-card :deep(.el-card__body) {
  padding: 12px 24px 28px;
}

/* 卡片头部 */
.admin-header {
  text-align: center;
}

.admin-header .logo {
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

.admin-title {
  margin: 0;
  font-size: 22px;
  letter-spacing: 0.5px;
  color: #1f2333;
}

.admin-subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8fa3;
}

/* Tab 激活态 */
.admin-tabs :deep(.el-tabs__item) {
  font-size: 15px;
  color: #6b7280;
}

.admin-tabs :deep(.el-tabs__item.is-active) {
  color: #7c5cfc;
  font-weight: 600;
}

.admin-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #a855f7, #6d5ef0);
  height: 3px;
  border-radius: 3px;
}

.admin-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: #f0eef5;
}

/* 表单间距与标签 */
.admin-tabs :deep(.el-form-item) {
  margin-bottom: 18px;
}

.admin-tabs :deep(.el-form-item__label) {
  color: #4b5164;
  font-weight: 500;
  padding-bottom: 6px;
}

/* 输入框圆角与聚焦态 */
.admin-tabs :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.admin-tabs :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #7c5cfc inset;
}

/* 管理员按钮 */
.admin-btn {
  width: 100%;
  margin-top: 4px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  letter-spacing: 2px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.admin-btn:not(.is-disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 22px -10px rgba(124, 92, 252, 0.65);
}

/* 创建用户按钮：主色 */
.admin-btn[type="primary"] {
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
}

/* 删除用户按钮：危险色 */
.admin-btn[type="danger"] {
  background: linear-gradient(135deg, #e5484d 0%, #c42b2c 100%);
}

.admin-btn[type="danger"]:not(.is-disabled):hover {
  box-shadow: 0 12px 22px -10px rgba(229, 72, 77, 0.65);
}

/* 小屏适配 */
@media (max-width: 480px) {
  .admin-card {
    width: 100%;
  }
  .admin-title {
    font-size: 20px;
  }
}
</style>
