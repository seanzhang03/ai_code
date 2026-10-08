<template>
 <div>
   <!--用户修改密码卡片头部-->
   <div>
     <h2>用户修改密码</h2>
   </div>

   <!--tab导航-->
   <div>
     <span @click="activePasswordMethod='captcha'">通过邮箱验证码修改</span><br>
     <span @click="activePasswordMethod='password'">通过旧密码修改</span>
   </div>

   <!--通过邮箱验证码修改-->
   <div v-show="activePasswordMethod==='captcha'">
     <form>
       邮箱号：<input type="text" :disabled="isSend" v-model="email"><br>
       验证码：<input type="text" :disabled="!isSend" v-model="captcha"><br>
       新密码：<input type="password" :disabled="!isSend" v-model="new_password"><br>
       <button type="button" :disabled="isSend" @click="sendCaptcha">发送验证码</button>
       <button type="button" :disabled="(!isSend)||(!email.trim())||(!captcha.trim())||(!new_password.trim())" @click="changePasswordCaptcha">修改密码</button>
     </form>
   </div>

   <!--通过邮箱旧密码修改-->
   <div v-show="activePasswordMethod==='password'">
     <form>
       邮箱号：<input type="text"  v-model="email"><br>
       旧密码：<input type="password"  v-model="old_password"><br>
       新密码：<input type="password"  v-model="new_password"><br>
       <button type="button" :disabled="(!email.trim())||(!old_password.trim())||(!new_password.trim())" @click="changePasswordPassword">修改密码</button>
     </form>
   </div>
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

</style>