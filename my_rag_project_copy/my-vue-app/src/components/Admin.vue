<template>
  <div>
    <!--管理员卡片头部-->
    <div>
      <h2>管理员模块</h2>
    </div>

    <!--Tab导航-->
    <div>
      <span @click="activeAdminMethod='create'">创建用户</span><br>
      <span @click="activeAdminMethod='init'">初始用户密码</span><br>
      <span @click="activeAdminMethod='delete'">删除用户</span><br>
    </div>

    <!--创建用户-->
    <div v-show="activeAdminMethod==='create'">
      <form>
        邮箱号： <input type="text" v-model="email"><br>
        用户名： <input type="text" v-model="nickname"><br>
        <button type="button" :disabled="(!email.trim())||(!nickname.trim())" @click="createUsers">创建用户</button>
      </form>
    </div>

    <!--密码初始化-->
    <div v-show="activeAdminMethod==='init'">
      <form>
        用户名： <input type="text" v-model="nickname"><br>
        <button type="button" :disabled="!nickname.trim()" @click="initPassword">初始化该用户密码</button>
      </form>
    </div>

    <!--删除用户-->
    <div v-show="activeAdminMethod==='delete'">
      <form>
        用户名： <input type="text" v-model="nickname"><br>
        <button type="button" :disabled="!nickname.trim()" @click="deleteUsers">删除该用户</button>
      </form>
    </div>

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

</style>