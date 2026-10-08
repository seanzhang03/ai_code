<template>
  <div class="chat-page">
    <!-- 左侧边栏：logo、新对话、历史记录、用户信息 -->
    <aside class="sidebar">
      <div class="sidebar-top">
        <div class="logo">RAG</div>
        <el-button type="primary" class="new-chat-btn" @click="createNewChat">
          <el-icon><Plus /></el-icon>
          <span>新对话</span>
        </el-button>
      </div>

      <div class="history-header">
        <span>历史记录</span>
      </div>

      <div class="history-list">
        <div
          class="history-item"
          v-for="item in historyList"
          :key="item.historyId"
          @click="selectHistory(item.historyId)"
        >
          <div class="history-info">
            <div class="history-question">{{ item.question }}</div>
            <div class="history-time">{{ item.createTime }}</div>
          </div>
          <!-- 阻止事件冒泡 -->
          <el-button class="history-delete" text size="small" @click.stop="deleteHistory(item.historyId)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>

      <div class="sidebar-bottom">
        <el-dropdown trigger="click" @command="handleUserCommand">
          <div class="user-info">
            <el-avatar :size="34" class="user-avatar">{{ nickname.charAt(0) }}</el-avatar>
            <span class="nickname">{{ nickname }}</span>
            <el-icon class="drop-arrow"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="admin" v-if="role==='admin'">管理员功能</el-dropdown-item>
              <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </aside>

    <!-- 右侧：对话主区域 -->
    <main class="chat-main">
      <header class="chat-header">
        <div class="chat-title">{{ currentTitle }}</div>
        <div class="chat-subtitle">{{ nickname }}与基于影视的RAG问答助手</div>
      </header>

      <!-- 消息区 -->
      <div class="message-box" ref="messageBox">
        <!-- 空状态 -->
        <div v-if="messages.length===0" class="empty-state">
          <div class="empty-logo">RAG</div>
          <div class="empty-hello">你好，{{ nickname }}</div>
          <div class="empty-desc">我是基于影视的RAG问答助手，可以基于知识库为你解答问题</div>
          <div class="suggest-list">
            <span class="suggest-chip" v-for="q in suggestQuestions" :key="q" @click="quickAsk(q)">{{ q }}</span>
          </div>
        </div>

        <!-- 对话记录 -->
        <div
          v-for="(item,index) in messages"
          :key="index"
          class="msg-row"
          :class="item.role==='assistant' ? 'is-assistant' : 'is-user'"
        >
          <div class="msg-name">{{ item.role === 'assistant' ? '基于影视的RAG问答助手' : nickname }}</div>
          <div class="msg-bubble">
            <span v-if="item.role==='user'">{{ item.content }}</span>
            <!-- 将 markdown 渲染成 html -->
            <div v-else class="markdown-body" v-html="$renderMarkdown(item.content)"></div>
          </div>
        </div>
      </div>

      <!-- 底部输入区 -->
      <div class="input-area">
        <textarea
          class="chat-textarea"
          v-model="question"
          rows="1"
          placeholder="向基于影视系统的RAG问答助手提问，enter发送，shift+enter换行"
          @keydown.enter.exact.prevent="handleEnter"
        ></textarea>
        <el-button type="primary" class="send-btn" :disabled="isButtonDisabled" @click="chat">
          <span v-show="!isLoading">发送</span>
          <span v-show="isLoading">加载中</span>
        </el-button>
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
}

//快速提问，基于建议的问题suggestQuestion来提问
function quickAsk(text){
  question.value=text
  chat()
}
</script>

<style scoped>
/* 整体布局：左栏 + 右主区域 */
.chat-page {
  display: flex;
  height: 100vh;
  width: 100%;
  text-align: left;
  overflow: hidden;
  color: #2b2f3a;
}

/* ===== 左侧边栏 ===== */
.sidebar {
  width: 280px;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-right: 1px solid #edf0f5;
}

.sidebar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 16px;
}

.sidebar .logo {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #a855f7, #6d5ef0);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.new-chat-btn {
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
}

.new-chat-btn:hover {
  opacity: 0.92;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
}

.history-header {
  padding: 8px 16px;
  font-size: 13px;
  color: #9aa0ae;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.history-item:hover {
  background: #f5f4fb;
}

.history-info {
  flex: 1;
  min-width: 0;
}

.history-question {
  font-size: 14px;
  color: #3a4152;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 12px;
  color: #a6acba;
  margin-top: 2px;
}

.history-delete {
  color: #b3b9c6;
  padding: 4px;
}

.history-item:hover .history-delete {
  color: #e5484d;
}

.sidebar-bottom {
  padding: 14px 16px;
  border-top: 1px solid #edf0f5;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 4px;
}

.user-avatar {
  background: linear-gradient(135deg, #a855f7, #6d5ef0);
  color: #fff;
  font-weight: 600;
}

.nickname {
  flex: 1;
  font-size: 14px;
  color: #3a4152;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drop-arrow {
  color: #9aa0ae;
}

/* ===== 右侧主区域 ===== */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #f6f7fb;
}

.chat-header {
  padding: 14px 24px;
  background: #ffffff;
  border-bottom: 1px solid #edf0f5;
}

.chat-title {
  font-size: 17px;
  font-weight: 600;
  color: #1f2333;
}

.chat-subtitle {
  font-size: 13px;
  color: #9aa0ae;
  margin-top: 3px;
}

/* 消息区：可滚动 */
.message-box {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* 空状态 */
.empty-state {
  max-width: 560px;
  margin: 12vh auto 0;
  text-align: center;
}

.empty-logo {
  width: 64px;
  height: 64px;
  margin: 0 auto 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  font-size: 26px;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  box-shadow: 0 12px 24px -10px rgba(124, 92, 252, 0.6);
}

.empty-hello {
  font-size: 22px;
  font-weight: 600;
  color: #1f2333;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #8a8fa3;
  margin-bottom: 24px;
}

.suggest-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.suggest-chip {
  padding: 8px 16px;
  font-size: 14px;
  color: #6d5ef0;
  background: #f1eefe;
  border: 1px solid #e4dcfb;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggest-chip:hover {
  color: #fff;
  background: linear-gradient(135deg, #a855f7, #6d5ef0);
  border-color: transparent;
}

/* 单条消息 */
.msg-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 18px;
}

.msg-row.is-user {
  align-items: flex-end;
}

.msg-row.is-assistant {
  align-items: flex-start;
}

.msg-name {
  font-size: 12px;
  color: #9aa0ae;
  margin-bottom: 6px;
  padding: 0 4px;
}

.msg-bubble {
  max-width: 72%;
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 15px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.is-user .msg-bubble {
  color: #fff;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  border-bottom-right-radius: 4px;
}

.is-assistant .msg-bubble {
  color: #2b2f3a;
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px -4px rgba(30, 34, 60, 0.08);
}

/* markdown 内容 */
.markdown-body :deep(pre) {
  background: #f4f3ec;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 13px;
}

.markdown-body :deep(code) {
  background: #f4f3ec;
  padding: 2px 6px;
  border-radius: 5px;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 13px;
}

.markdown-body :deep(pre code) {
  background: transparent;
  padding: 0;
}

/* 底部输入区 */
.input-area {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  padding: 16px 24px;
  background: #ffffff;
  border-top: 1px solid #edf0f5;
}

.chat-textarea {
  flex: 1;
  resize: none;
  padding: 12px 16px;
  font-size: 15px;
  line-height: 1.5;
  font-family: inherit;
  color: #2b2f3a;
  border: 1px solid #e2e6ef;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  min-height: 46px;
  max-height: 160px;
  box-sizing: border-box;
}

.chat-textarea:focus {
  border-color: #7c5cfc;
  box-shadow: 0 0 0 3px rgba(124, 92, 252, 0.12);
}

.send-btn {
  height: 46px;
  padding: 0 24px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  background: linear-gradient(135deg, #a855f7 0%, #6d5ef0 100%);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.send-btn:not(.is-disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px -10px rgba(124, 92, 252, 0.65);
}

/* 小屏适配 */
@media (max-width: 768px) {
  .sidebar {
    width: 220px;
    min-width: 220px;
  }
  .msg-bubble {
    max-width: 88%;
  }
}
</style>
