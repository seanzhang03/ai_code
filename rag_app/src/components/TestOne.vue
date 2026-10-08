<script setup>
//导入响应式数据---用于定义变量
import {ref} from "vue"
//定义一个变量，类型为布尔类型，默认值为false
//let:javascript定义变量的标识符,ref是定义变量的函数，false变量的默认值
let isDisabled = ref(false);
//定义函数 ---规则---function 函数名称(形参){函数体}
function changeInput(){
  //js中的输出语句console.log(输出内容),输出结果在浏览器的console[控制台]中而不是在IDE工具中
  //在函数中想要访问定义的变量的值 -- 变量名称.value
  isDisabled.value = !isDisabled.value;
  console.log(isDisabled.value);
}
  //定义控制div显示与隐藏的变量
  let isShow = ref(true);

//定义登录函数
function sendEmail(){
  isCode.value = !isCode.value
  //js语法-DOM对象语法
  let email = document.getElementById("email").value
  console.log(email.value)
}

//定义控制验证码输入框是否可以输入的变量
let isCode=ref(true);

//定义验证码函数
function checkCode(){
  console.log("验证验证码")
  console.log(email.value,code.value)
  code.value="我变了"   //在这里通过code.value修改了双向绑定的验证码
}

//定义保存邮箱号、验证码的变量
let email =ref("")
let code =ref("")

//定义一个用户和ai问答的变量---是一个数组，数组里面的元素就是一个js对象
let messages = ref(
    [
      {role:"assistant",content:"你好，我是AI，你可以向我提供任何问题"},
      {role: 'user', content: '你叫什么名字？'},
      {role: 'assistant', content: '我叫ChatGPT，一个基于OpenAI的AI模型。'},
      {role: 'user', content: '你喜欢什么书？'},
      {role: 'assistant', content: '我非常喜欢《哈利波特》系列，以及《1984》和《安徒生童话》。'},
      {role: 'user', content: '你喜欢什么电影？'}
    ]
)

</script>




<template>
  <div>
    <!--表单 ，通常用于需要用户进行输入的时候-->
    <form>
        <!--一个输入框,类型为文本，即字符串-->
        账号:<input type="text" v-bind:disabled="isDisabled">
        <br>
      <!--
      //v-bind语法
      //语法解释 <标签 v-bind:属性名="变量[常量]"></标签>
      //标签：html中的标签名称
      //v-bind：指令名称，叫属性绑定指令
      //属性名：html中的标签中的属性
      //变量常量--定义在js中，常量就直接写
      //语法糖 <标签:属性名="变量[常量]"></标签>
      -->
        密码:<input type="password">
        <br>
       <!--点击按钮之后，需要去修改某个变量的值，通常情况下我们在函数中实现，即点击按钮之后就该去执行修改变量的值的函数，等价于python中调用函数
       这个过程叫事件绑定，完成事件绑定的事件名称非常多，比如click(单机事件)，dblclick
       在vue中，如果想要点击按钮或者其他标签时，去调用函数的执行，就需要使用语法指令--- v-on:事件名称=函数名称()
       语法糖：如果函数没有参数，就可以去掉函数名称的括号/v-on可以缩写为@---@事件名称=函数名称[我们使用的版本]
       -->
        <button type="button" @click="changeInput()">点我</button> <!--点击之后就会去执行changeInput()函数-->
    </form>
    <h1>控制内容显示与隐藏指令</h1>
    <!-- 控制内容与隐藏指令v-show
    指令语法：
    <标签 v-show = 布尔值></标签>
    通过布尔值来控制这个标签是否显示在页面上，true显示，false隐藏
    -->
    <div v-show = "isShow" style="border:1px solid red;width:100%">
    我显示了1
    </div>
    <div v-show = "!isShow" style="border:1px solid blue;width:100%">  <!--只显示1和2中的一个 -->
      我显示了2
    </div>
    <button type="button" @click="isShow=!isShow">点我2</button>

    <h1>双向绑定指令</h1>
    <!--双向绑定指令  v-model="变量名称"
    它可以使得html标签中的内容[一般是输入和选择]始终和绑定的变量是同一个值
    即输入内容变量=变量变化、变量变化=输入内容变量变化
    -->
    <form>
        邮箱号:<input type="text" v-bind:disabled="!isCode" id="email" v-model="email">  <!--disabled属性用来启用或者禁用某个属性，true为禁用false为非禁用 -->
        <br>
        验证码:<input type="text" :disabled="isCode " v-model="code">
        <br>
       <button type ="button" @click="sendEmail" v-show="isCode ">发送验证码</button>
      <button type ="button" @click="checkCode" v-show="!isCode">验证验证码</button>
    </form>
    <h1>循环指令</h1>
    <!--循环指令v-for，用法和for循环雷同
    语法格式 <标签 v-for=(每次得到的内容,index) in 变量对象变量名称)></标签>
    展示数据：在html中用表格，表格的基本组成
    <table>
      <tr>   表示表格的某一行
        <td></td>  表示表格的某一列
        <td></td>
      </tr>
    </table>
    -->
    <div>
      <table>
        <tr v-for="(item,index) in messages">  <!--item是每次遍历得到的对象，index是索引-->
       <!--在页面中取出js中定义的变量，v-for循环中的变量等，直接用{{变量名称}} {{}}差值表达式-->
          {{item.content}}
        </tr>
      </table>
    </div>
    <hr>  <!--水平线-->
    <div >
      <div v-for="(item,index) in messages">
          {{item.content}}
      </div>
    </div>

    </div>
</template>

<style scoped>

</style>


