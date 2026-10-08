<script setup>
  import {ref,getCurrentInstance} from "vue";
  //控制输入框是否可以输入的变量
  let isCode = ref(true);

  //接受邮箱号和验证码的变量
  let email = ref("1607259232@qq.com")
  let code = ref("")

  //获取当前实例对象，通过实例对象访问到main.js中的$axios
  let proxy =getCurrentInstance().proxy
  console.log(getCurrentInstance())

  //定义发送验证码函数
  function sendEmail(){
    let sendEmail = email.value //获取到用户输入的邮箱号
    //通过封装的axios请求访问服务器定义的发送验证码接口
    proxy.$axios({ //{}写的就是访问服务器接口的信息：比如请求地址[自动拼接http://localhost:8000/]、请求方式[默认get]、请求承诺书
      url:"users/sendEmail",//请求地址
      method:"get",  //请求方式
      params:{  //请求参数
        email:sendEmail,  //参数的key必须和服务器接口的形参一致
      },
    }).then(res=>{ //请求成功的回调函数 ---即请求服务器接口成功后执行这个代码
      //这个代码本质上就是一个函数，只是用了函数的简化写法[箭头函数]
      //res就是函数的形参,=>固定写法，{}内的内容就是函数体
      //res=>{] 等价于function a(res){]
      //res中的data属性就是我们自己在服务器中定义的返回值
      let code = res.data.code
      let msg = res.data.msg
      //逻辑判断处理 '==='表示全等，即数据类型和值都相等
      if(code===200){
        //修改isCode的值
        alert(msg)
      }
      else{
        alert(msg)
      }
    })
    console.log(proxy)
  }

  //定义验证码函数
  function checkCode(){
    let checkCode={ //把输入的邮箱号和验证码封装成一个js对象
      email:email.value,
      code:code.value
    }
    //json.stringify将js对象转为json
    //json.parse(json)将json转为js对象
    //axios中使用post请求，设置参数时用data属性，比如data:JSON.stringify(checkCode)
    JSON.stringify(checkCode)

  }
  //同源策略：要求计算机中A服务访问B服务，必须满足协议、ip、端口都相同
  //对我们服务器、客户端前后端分离项目而言，无法满足端口相同，就违背了同源策略的规定，要想实现访问，就要进行跨域配置[都在服务端解决 ]
</script>




<template>
  <div>
     <form>
        邮箱号:<input type="text" v-bind:disabled="!isCode" id="email" v-model="email">  <!--disabled属性用来启用或者禁用某个属性，true为禁用false为非禁用 -->
        <br>
        验证码:<input type="text" :disabled="isCode " v-model="code">
        <br>
       <button type ="button" @click="sendEmail" v-show="isCode ">发送验证码</button>
      <button type ="button" @click="checkCode" v-show="!isCode">验证验证码</button>
    </form>
  </div>
</template>

<style scoped>

</style>