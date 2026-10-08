<template>
  <div>
    <!--注册用户卡片头部-->
    <div>
      <h2>用户注册</h2>
    </div>

    <!--用户注册部分-->
    <div>
      <form>
        邮箱号：<input type="text" v-model="email"><br>
        密码：<input type="password" v-model="password"><br>
        请再次输入密码：<input type="password" v-model="again_password"><br>
        用户名：<input type="text" v-model="nickname"><br>
        <!--必须输入所有信息并且两次输入密码一致才允许注册-->
        <button type="button" :disabled="((!email.trim())||(!password.trim())||(!again_password.trim())||(!nickname.trim())||(!(password==again_password)))"
                @click="registration">注册</button>
      </form>

    </div>
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

</style>