<template>
  <!--div是用来分区的-->
  <div>

    <!--登录卡片头部-->
    <div>
      <!--h2即二级标题-->
      <h2>用户登录</h2>
    </div>

      <!--Tab导航-->
      <div>
        <!--span是行内标签，用来包裹一小段文字和几个元素-->
        <span @click="activeLoginMethod ='captcha'">通过验证码登录</span><br>
        <span @click="activeLoginMethod ='email_password'">通过邮箱密码登录</span><br>
        <span @click="activeLoginMethod ='nickname_password'">通过用户名密码登录</span><br>
      </div>

    <!--通过邮箱验证码登录-->
    <div v-show="activeLoginMethod==='captcha'">  <!-- v-show函数用来显示或隐藏 -->
      <form>
        <!--还未点击发送允许用户输入邮箱号-->
        邮箱号：<input type="text" :disabled="isSend" v-model="email"><br>
        验证码：<input type="text" :disabled="!isSend" v-model="captcha"><br>
        <button type="button" :disabled="isSend" @click="sendCaptcha">发送验证码</button>
        <button type="button" :disabled="!isSend" @click="loginByEmailCaptcha">登录</button>
      </form>
    </div>


  <!--通过邮箱密码登录-->
  <div v-show="activeLoginMethod==='email_password'">  <!-- v-show函数用来显示或隐藏 -->
      <form>
        <!--还未点击发送允许用户输入邮箱号-->
        邮箱号：<input type="text"  v-model="email"><br>
        密码：<input type="password"  v-model="password"><br>
        <button type="button" :disabled="(!email.trim()) ||(!password.trim())" @click="loginByEmailPassword">登录</button>
      </form>
    </div>


  <!--通过用户名密码登录-->
  <div v-show="activeLoginMethod==='nickname_password'">  <!-- v-show函数用来显示或隐藏 -->
      <form>
        <!--还未点击发送允许用户输入邮箱号-->
        用户名：<input type="text"  v-model="nickname"><br>
        密码：<input type="password"  v-model="password"><br>
        <button type="button" :disabled="(!nickname.trim()) ||(!password.trim())" @click="loginByNicknamePassword">登录</button>
      </form>
    </div>
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

</style>