<template>
  <div>
    <!--左侧功能：展示历史记录以及新建一个对话-->
    <!--顶部logo和新建对话-->
    <div>
      <div>RAG</div>
      <button @click="createNewChat">新对话</button>
    </div>

    <!--历史记录标题-->
    <div>
      <span>历史记录</span>
    </div>

    <!--一个完整窗口的全部上下文记录-->
    <div v-for="item in historyList" :key="item.historyId" @click="selectHistory(item.historyId)">
      <!--各窗口记录-->
      <div>
        <div>{{item.question}}</div>
        <div>{{item.createTime}}</div>
      </div>
      <!--阻止事件冒泡-->
      <button @click.stop="deleteHistory(item.historyId)">删除</button>
    </div>

    <!--底部，当前用户的信息-->
    <div>
      <div>
        <span>{{nickname}}</span>
        <select @change = 'handleUserCommand($event.target.value)'>
          <option></option>
          <option value="admin" v-if="role==='admin'">管理员功能</option>
          <option value="changePassword">修改密码</option>
          <option value="logout">退出登录</option>
        </select>
      </div>
    </div>

    <!----------------------右侧,即对话主区域----------------------->
    <main>
      <!--顶部标题栏-->
      <header>
        <div>{{currentTitle}}</div>
        <div>{{nickname}}与基于影视的RAG问答助手</div>
      </header>

      <!--消息区-->
      <div ref ="messageBox"> <!--让js代码能直接获取并操作这个DOM元素-->
        <div v-if="messages.length===0">  <!-- v-if根据条件选择性渲染-->
          <div>RAG</div>
          <div>你好,{{nickname}}</div>
          <div>我是基于影视的RAG问答助手，可以基于知识库为你解答问题</div>
          <div>
            <span v-for="q in suggestQuestions" :key="q" @click="quickAsk(q)">{{q}}</span>
          </div>
        </div>
        <!--一个窗口的全部对话记录-->
        <div v-for="(item,index) in messages" :key="index">
          <div>
            <div>{{item.role ==='assistant'?'基于影视的RAG问答助手':nickname}}</div> <!--基于不同角色展示不同信息，若是user展示nickname，否则展示前面的信息-->
            <div>
              <!-- v-if v- else-->
              <span v-if="item.role==='user'">{{item.content}}}</span>  <!--如果role是user则展示其中的内容-->
              <div v-else v-html="$renderMarkdown(item.content)"></div>  <!--将markdown文档加载成html字符-->
            </div>
          </div>
        </div>
      </div>

      <!--底部输入区-->
      <div>
        <textarea
            v-model="question",
            rows="1"
            placeholder="向基于影视系统的RAG问答助手提问，enter发送，shift+enter换行"
            @keydown.enter.exact.prevent="handleEnter"
        ></textarea><!-- textarea多行输入-->
        <button :isdisabled="isButtonDisabled" @click="chat">
          <span v-show="!isLoading">发送</span>
          <span v-show="isLoading">加载中</span>
        </button>
      </div>

    </main>



  </div>
</template>

<script setup>
import {ref, watch,computed,getCurrentInstance, onMounted,nextTick} from "vue";
import { ElMessage } from 'element-plus'
//代理对象
let proxy = getCurrentInstance().proxy

//导入路由
import {useRouter} from "vue-router"

//控制发送按钮是否可以使用的布尔值
let isButtonDisabled = ref(true)

//用户输入的问题
let question = ref("")

//用户名
let nickname = ref("")

//路由对象，用于登录跳转功能
let router = useRouter()

//监听用户输入的问题
watch(question,(newQuestion)=>{ //question后面跟的是回调函数，当用户输入、删除内容导致question变化，回调函数自动执行，并将新值newQuestion传进去
  console.log(newQuestion)
  //判定输入栏是否输入了东西
  //若有输入且不为空串，则允许点击发送按钮,否则不允许
  if(newQuestion.length>0 && newQuestion.trim()){
    isButtonDisabled.value = false
  }
  else{
    isButtonDisabled.value = true
  }
})


//存储聊天记录的数组，将对话结果保存下来，显示在页面上
let messages = ref([])

//控制loading按钮
let isLoading = ref(false)

//全局对话保存的history_id(默认为0)
let globalHistoryId = ref(0)

//空状态下的快捷提问建议
const suggestQuestions = [
    "推荐几部高分电影",
    "热门电影",
    "新上映的电影"
]

//左侧对话窗口记录
let historyList= ref([])

//定义角色
let role = ref("")
role.value = sessionStorage.getItem("role")

//退出登录跳转函数
function log_out_router(){
  setTimeout(()=>{router.push("/login")},1000)
}
//修改密码跳转函数
function change_password_router(){
  setTimeout(()=>{router.push("/password")},1000)
}

//管理员功能跳转函数
function admin_router(){
  setTimeout(()=>{router.push("/admin")},1000)
}
//聊天
function chat(){
  let myQuestion = question.value.trim() //把用户输入的问题赋值给myQuestion
  console.log(myQuestion)
  question.value = ""  //清空用户输入的问题
  //考虑到用户的问题在右侧显示，ai的回复在左侧显示，通过角色来控制样式
  //添加用户的问题到messages中、模拟ai的回复到messages中
  messages.value.push({role:"user",content:myQuestion})
  messages.value.push({role:"assistant",content:"ai努力回复中~~"})
  //通过sse请求,把用户的问题发送给服务器，实时接收服务器的流式输出数据
  //构造sse请求  ---参数  构造一个URL查询字符串参数对象
  let params = new URLSearchParams({question:myQuestion,historyId:globalHistoryId.value}) //告诉服务器这个变量question对应的值为myQuestion
  //构造sse请求 --- 对象：其参数为服务器请求地址 + 客户端给服务器的参数+get请求
  let sse = new EventSource("http://localhost:8000/chat/chat?"+params) //"users/chat?"这么写要调用封装好的axios，这里明确告诉访问地址
  //sse请求监听服务器返回的结果
  //拼接结果的变量
  let s = ""
  sse.onmessage=(event)=>{
    let content = JSON.parse(event.data).content //parse函数将json数据转为js对象
    console.log(content)
    if (content === "[DONE]"){ //结束
      //关闭连接
      sse.close()
      console.log("SSE连接已经关闭")
      //保存对话结果
      saveChatResult(myQuestion,s)
      isLoading.value = false //隐藏loading
      //结束
      return
    }
    //拼接结果
    s+= content
    //修改messages中最后一个元素中content属性的值
    messages.value[messages.value.length-1].content =s
  }
  //sse请求监听服务器返回的错误
  sse.onerror = (event) => {
    console.log("SSE请求错误",event)
    isLoading.value = false  //接收到错误隐藏loading
  }
  //sse连接时打印
  sse.onopen=()=>{
    console.log("建立SSE连接")
  }
}



//当前对话标题,动态显示聊天窗口顶部的标题
const currentTitle = computed(()=>{
  //cur是一个bool值，若找到了就返回true
  const cur = historyList.value.find(h=>h.id===globalHistoryId.value); //查找id等于选中会话globalHistoryId的那条
  //true返回之前的历史记录的标题，否则返回新的对话
  return cur?cur.title:'新的对话';
})

//消息区DOM，自动滚动到底部(流式输出保持跟随)
let messageBox = ref(null)

//监听消息变化，自动滚动到底部(流式输出保持跟随)
watch(messages,()=>{
  nextTick(()=>{
    if(messageBox.value){
      messageBox.value.scrollTop = messageBox.value.scrollHeight //scrollHeight元素内容总高度，scrollTop当前向上滚动的像素
    }
  })
},{deep:true}) //deep:true表示流式输出也能跟着滚动


//点击左侧窗口记录进入一个完整的窗口，显示其上下文历史
function selectHistory(historyId){
  globalHistoryId.value = historyId
  proxy.$axios({
    url:"history/queryHistoryList/"+historyId,  //这里直接把参数通过url传递了
    method:"get"
  }).then(res=>{
    messages.value = res.data.data
  })
}

//保存对话结果 --- 需要user_id,question,answer,parent_id等
function saveChatResult(question,answer){
  let params = {
    userId:sessionStorage.getItem("usersId"),
    question:question,
    answer:answer,
    parentId:globalHistoryId.value,
  }
  proxy.$axios({
    url:"history/saveChatResult",
    method:"post",
    data:JSON.stringify(params)
  }).then(res=>{
    if(globalHistoryId.value === 0) {
      //新对话---继续对话不需要做任何处理
      globalHistoryId.value = res.data.data  //后端将新对话存入到数据库中，并返回在数据库中的history_id
      //重新加载历史记录菜单
      queryHistoryMenu()
      }
  })
}

//加载历史对话菜单，即左侧窗口记录
function queryHistoryMenu(){
  proxy.$axios({
    url:"history/queryHistoryMenu/"+sessionStorage.getItem("usersId"),
    method:"get",
  }).then(res=>{
    historyList.value=res.data.data
  })
}

//键盘enter键进行消息的发送(shift+enter为换行)
function handleEnter(){
  if(!isButtonDisabled.value) {//即有内容的时候可以调用chat方法
    chat()
  }
}

//新建对话
function createNewChat(){
  globalHistoryId.value = 0 //重置新对话的根对话id
  messages.value=[]  //清空messages数组的内容
}

  //加载页面后执行，加载页面后挂载历史记录菜单
onMounted(()=>{
  nickname.value = sessionStorage.getItem("nickname")||"undefined"
  queryHistoryMenu()
  })

//用户菜单命令处理
function handleUserCommand(command){
  switch(command){
    case "admin":
      ElMessage.info("即将跳转到管理员功能页面~")
      admin_router()
      break
    case "changePassword":
      ElMessage.info("即将跳转到修改密码功能页面~")
        change_password_router()
      break
    case "logout":
      ElMessage.info("即将退出登录~")
      log_out_router()
      break
  }
}//TODO:后续对接前端，根据command跳转到对应页面

//快速提问，基于建议的问题suggestQuestion来提问
function quickAsk(text){
  question.value=text
  chat()
}
</script>

<style scoped>

</style>