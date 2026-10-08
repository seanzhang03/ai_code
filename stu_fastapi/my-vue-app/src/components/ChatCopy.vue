
<template>
  <div>
    <div v-for="(item,index) in messages" :key="index">
      {{item.content}}
    </div>
    <form>
      <input type="text" placeholder="向sz提问" v-model="question"/>
      <el-button type="primary" @click="chat" :disabled="isButtonDisabled" v-loading="isLoading">
        <el-icon ><search /></el-icon>
      </el-button>
    </form>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted,watch} from "vue";
import {ElMessage} from "element-plus";
//axios请求：一次性得到所有的结果，这种实现出来的问答就不和日常使用的网页问答相同
//流式输出：为我们的大模型输出一点内容后，马上返回给客户端，客户端马上展示到页面上
//实现流式输出的方式：
//js支持的fetch请求：客户端代码复杂，规定服务器流式输出的数据就是数据内容就可以了
//sse请求：客户端的代码相对简单一些，规定服务器流式输出的内容必须满足data:内容\n\n格式，这个只能发送get请求，没办法设置请求头信息(请求头中可设置登录的凭证信息)

//用户输入的问题
let question = ref("")

//控制发送按钮是否可以使用的布尔值
let isButtonDisabled = ref(true)

//监听用户输入的问题
watch(question,(newQuestion)=>{
  console.log(newQuestion)
  //判定是否输入了内容
  if(newQuestion.length>0 && newQuestion.trim()){
    isButtonDisabled.value = false
  }
  else{
    isButtonDisabled.value = true
  }
})

//存储聊天记录的数组，将对话结果保存下来，显示在页面上
let messages = ref([
  {role:"user",content:"你好"},
  {role:"assistant",content:"你好，有什么我可以帮忙的吗？"}
])

//控制按钮状态loading
let isLoading = ref(false)

//聊天
function chat(){
  isLoading = true  //显示loading
  let myQuestion = question.value.trim() //把用户输入的问题赋值给myQuestion trim函数去除空格
  console.log(myQuestion)
  question.value = ""  //清空用户输入的问题
  //由于用户的问题在右边显示，ai的回复在左边显示，我们提前通过角色来控制样式
  //添加用户的问题到messages中、模拟ai的回复到messages中
  messages.value.push({role:"user",content:myQuestion})
  messages.value.push({role:"assistant",content:"ai努力回复中~~~~"})
  //通过sse请求，把用户的问题发送给服务器，实时接收服务器的流式输出数据
  //构造sse请求 -- 参数
  let params =new URLSearchParams({question:myQuestion})  //告诉服务器有个变量question对应的值为myQuestion
  //创建sse请求 -- 对象 --- 参数就是服务器请求地址 + 客户端给服务器的参数+get请求
  let sse =new EventSource("http://localhost:8000/chat/chat?"+params)  //"users/chat?"这么写要调用封装好的axios，这里明确告诉访问地址
  //sse请求监听服务器返回的结果
  //拼接结果的变量
  let s = ""
  sse.onmessage = (event)=>{
    let content = JSON.parse(event.data).content //parse函数将json数据转换为js对象
    console.log(content)
    if(content==="[DONE]"){//结束
      //关闭连接
      sse.close()
      console.log("SSE连接已关闭")
      isLoading.value = false //隐藏loading
      //结束
      return
    }
    //拼接结果s+=content
    s+=content
    //修改messages中最后一个元素中content属性的值
    messages.value[messages.value.length-1].content = s
    //当消息接收完成后，需要关闭sse连接，否则会一直监听，服务器的数据就会重复输出
  }
  //sse请求监听服务器返回的错误
  sse.onerror = (event)=>{
    console.log("接收到错误",event)
    isLoading.value = false
  }
  //sse连接的时候打印
  sse.onopen = (event) =>{
    console.log("接收到连接",event)
  }
}
</script>


<style scoped>
</style>