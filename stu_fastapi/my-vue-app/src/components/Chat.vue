<template>
    <div class="chat-wrapper">
        <!-- ============ 左侧：历史记录 + 用户信息 ============ -->


        <aside class="chat-sidebar">
            <!-- 顶部 Logo 与新建对话 -->
            <div class="sidebar-header">
                <div class="logo-badge">
                    <span class="logo-dot"></span>
                    RAG
                </div>
                <el-button
                        type="primary"
                        class="new-chat-btn"
                        @click="createNewChat"
                >
                    <el-icon>
                        <Plus/>
                    </el-icon>
                    <span>新对话</span>
                </el-button>
            </div>

            <!-- 历史记录标题 -->
            <div class="history-title">
                <span>历史记录</span>
                <el-icon class="history-title-icon">
                    <Clock/>
                </el-icon>
            </div>

            <!-- 历史记录列表 -->
            <el-scrollbar class="history-scroll">
                <div class="history-list">
                    <div
                            v-for="item in historyList"
                            :key="item.historyId"
                            class="history-item"
                            :class="{ active: item.usersId === globalHistoryId }"
                            @click="selectHistory(item.historyId)"
                    >
                        <el-icon class="history-item-icon">
                            <ChatDotRound/>
                        </el-icon>
                        <div class="history-item-body">
                            <div class="history-item-title">{{ item.question }}</div>
                            <div class="history-item-time">{{ item.createTime }}</div>
                        </div>
                        <el-popconfirm
                                title="确定删除这条历史记录吗？"
                                width="220"
                                confirm-button-text="删除"
                                cancel-button-text="取消"
                                @confirm="deleteHistory(item.historyId)"
                        >
                            <template #reference>
                                <el-icon class="history-item-delete" @click.stop>
                                    <Delete/>
                                </el-icon>
                            </template>
                        </el-popconfirm>
                    </div>
                </div>
            </el-scrollbar>

            <!-- 底部：当前用户信息 -->
            <div class="sidebar-user">
                <el-dropdown trigger="click" @command="handleUserCommand">
                    <div class="user-info">
                        <el-avatar :size="38" class="user-avatar">{{ nickname }}</el-avatar>
                        <el-icon class="user-arrow">
                            <ArrowDown/>
                        </el-icon>
                    </div>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="profile">
                                <el-icon>
                                    <User/>
                                </el-icon>
                                个人中心
                            </el-dropdown-item>
                            <el-dropdown-item command="settings">
                                <el-icon>
                                    <Setting/>
                                </el-icon>
                                设置
                            </el-dropdown-item>
                            <el-dropdown-item command="logout" divided>
                                <el-icon>
                                    <SwitchButton/>
                                </el-icon>
                                退出登录
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </aside>

        <!-- ============ 右侧：对话主区域 ============ -->
        <main class="chat-main">
            <!-- 顶部标题栏 -->
            <header class="chat-header">
                <div class="chat-header-title">{{ currentTitle }}</div>
                <div class="chat-header-sub">
                    {{ nickname }} 与 RAG 助手
                </div>
            </header>

            <!-- 消息区 -->
            <div class="chat-messages" ref="messageBox">
                <!-- 空状态：欢迎引导 -->
                <div v-if="messages.length === 0" class="empty-state">
                    <div class="empty-logo">RAG</div>
                    <div class="empty-title">你好，{{ nickname }} 👋</div>
                    <div class="empty-desc">我是 RAG 检索增强问答助手，可以基于知识库为你解答问题</div>
                    <div class="empty-suggests">
                        <span
                                v-for="q in suggestQuestions"
                                :key="q"
                                class="suggest-chip"
                                @click="quickAsk(q)"
                        >{{ q }}</span>
                    </div>
                </div>

                <!-- 消息列表 -->
                <div
                        v-for="(item, index) in messages"
                        :key="index"
                        class="message-row"
                        :class="item.role"
                >
                    <el-avatar :size="34" class="message-avatar" :class="item.role">
                        {{ item.role === 'assistant' ? 'AI' : nickname }}
                    </el-avatar>
                    <div class="message-body">
                        <div class="message-role">{{ item.role === 'assistant' ? 'RAG 助手' : nickname }}</div>
                        <div
                                class="message-bubble"
                                :class="item.role"
                        >
                            <span v-if="item.role === 'user'">{{ item.content }}</span>
                            <div v-else class="markdown-body" v-html="$renderMarkdown(item.content)"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 底部输入区 -->
            <div class="chat-input-area">
                <el-input
                        v-model="question"
                        type="textarea"
                        :rows="1"
                        resize="none"
                        :autosize="{ minRows: 1, maxRows: 5 }"
                        placeholder="向 cc 提问，Enter 发送，Shift + Enter 换行"
                        class="chat-input"
                        @keydown.enter.exact.prevent="handleEnter"
                />
                <el-button
                        type="primary"
                        class="send-btn"
                        :disabled="isButtonDisabled"
                        v-loading="isLoading"
                        @click="chat"
                >
                    <el-icon v-if="!isLoading">
                        <Promotion/>
                    </el-icon>
                </el-button>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, getCurrentInstance,onMounted } from "vue";
import { ElMessage } from "element-plus";
import {useRouter} from "vue-router"
import {  Delete } from "@element-plus/icons-vue";
// 其余图标已在 main.js 中全局注册，模板内可直接使用（如 <Plus />、<Promotion /> 等）

// =====================================================================
// 以下为「已实现」的核心聊天逻辑，保持不变
// =====================================================================

//代理对象
let proxy = getCurrentInstance().proxy

// 用户输入的问题
let question = ref("")

// 控制发送按钮是否可以使用的布尔值
let isButtonDisabled = ref(true)

// 监听用户输入的问题
watch(question, (newQuestion) => { //question后面跟的是回调函数，当用户输入、删除内容导致question变化，回调函数自动执行，并将新值newQuestion传进去
  // 判定是否输入了内容
  if (newQuestion.length > 0 && newQuestion.trim()) {
    isButtonDisabled.value = false
  } else {
    isButtonDisabled.value = true
  }
})

// 存储聊天记录的数组，将对话结果保存下来，显示在页面上
let messages = ref([])

// 控制按钮状态loading
let isLoading = ref(false)

// 聊天
function chat() {
  isLoading.value = true  // 显示loading
  let myQuestion = question.value.trim() // 把用户输入的问题赋值给myQuestion trim函数去除空格
  question.value = ""  // 清空用户输入的问题
  // 由于用户的问题在右++边显示，ai的回复在左边显示，我们提前通过角色来控制样式
  // 添加用户的问题到messages中、模拟ai的回复到messages中
  messages.value.push({ role: "user", content: myQuestion })
  messages.value.push({ role: "assistant", content: "ai努力回复中~~~~" })
  // 通过sse请求，把用户的问题发送给服务器，实时接收服务器的流式输出数据
  // 构造sse请求 -- 参数
  let params = new URLSearchParams({ question: myQuestion ,historyId:globalHistoryId .value})  // 告诉服务器有个变量question对应的值为myQuestion
  // 创建sse请求 -- 对象 --- 参数就是服务器请求地址 + 客户端给服务器的参数+get请求
  let sse = new EventSource("http://localhost:8000/chat/chat?" + params)  // "users/chat?"这么写要调用封装好的axios，这里明确告诉访问地址
  // sse请求监听服务器返回的结果
  // 拼接结果的变量
  let s = ""
  sse.onmessage = (event) => {
    let content = JSON.parse(event.data).content // parse函数将json数据转换为js对象
    console.log(content)
    if (content === "[DONE]") { // 结束
      // 关闭连接
      sse.close()
      console.log("SSE连接已关闭")
      //保存对话结果
      saveChatResult(myQuestion,s)
      isLoading.value = false // 隐藏loading
      // 结束
      return
    }
    // 拼接结果s+=content
    s += content
    // 修改messages中最后一个元素中content属性的值
    messages.value[messages.value.length - 1].content = s
    // 当消息接收完成后，需要关闭sse连接，否则会一直监听，服务器的数据就会重复输出
  }
  // sse请求监听服务器返回的错误
  sse.onerror = (event) => {
    console.log("接收到错误", event)
    isLoading.value = false  //隐藏loading
    //保存对话结果
  }
  // sse连接的时候打印
  sse.onopen = (event) => {
    console.log("接收到连接", event)
  }
}

// =====================================================================
// 以下为「新增」的美化/交互相关状态与函数（仅定义 + 模拟数据，不含真实实现）
// =====================================================================

// 获取当前组件实例（如需访问 $axios / $renderMarkdown 等全局属性）
//路由对象，用于退出登录跳转等后续功能
let router = new useRouter()

//当前登录用户信息(昵称从登录页写入的sessionStorage读取，其余为模拟数据)
let nickname = ref("")

//历史记录模拟数据(每条含对应的模拟聊天内容，用来演示"点击后展示数据内容")
let historyList = ref([])


//当前对话标题
const currentTitle = computed(()=>{
  const cur = historyList.value.find(h=>h.id===globalHistoryId.value)
  return cur?cur.title:'新的对话'
})

//空状态下的快捷提问建议
const suggestQuestions = [
    "什么是RAG",
    "如何优化向量检索",
    "SSE流式输出原理"
]

//消息区DOM，用于自动滚动到底部（流式输出时保持跟随）
let messageBox = ref(null)

//监听消息变化，自动滚动到底部(流式输出时保持跟随)
watch(messages,()=>{
  nextTick(()=>{
    if(messageBox.value){
      messageBox.value.scrollTop = messageBox.value.scrollHeight //scrollHeight元素内容总高度，scrollTop当前向上滚动的像素
    }
  })
},{deep:true})  //deep:true表示流式输出也能跟着滚动

//全局对话保存的history_id(默认值为0)
let globalHistoryId=ref(0)


//点击某条历史记录
function selectHistory(historyId){
  globalHistoryId.value = historyId
  proxy.$axios({
    url:"history/queryHistoryList/"+historyId,
    method:"get"
  }).then(res=>{
    messages.value = res. data.data
  })
}

//保存对话结果---需要参数user_id,question,answer,parent_id
function saveChatResult(question,answer){
  let params = {
    usersId:sessionStorage.getItem("usersId"),
    question:question,
    answer:answer,
    parentId:globalHistoryId.value,
  }
  proxy.$axios({
    url:"history/saveChatResult",
    method:"post",
    data:JSON.stringify(params)
  }).then(res=>{  //返回的数据就是新增对话记录的id
    if(globalHistoryId.value===0){
      //新对话---继续对话不需要做任何处理
      globalHistoryId.value =res.data.data
      //重新加载历史记录菜单
      queryHistoryMenu()
    }
  })
}

//新建对话
function createNewChat(){
  globalHistoryId.value = 0 //重置新对话的parentId=0
  messages.value=[]  //清空messages数组中的内容
}

//删除历史记录
  function deleteHistory(historyId){

}

//键盘enter发送(shift+enter换行)
function handleEnter(){
  if(!isButtonDisabled.value){
    chat()
  }
}

//快捷提问：填入问题并发送
function quickAsk(text){
  question.value = text
  chat()
  //TODO:后续可扩展为直接跳转到新会话再发送
}

//用户菜单命令处理
function handleUserCommand(command){
  switch(command){
    case "profile":
      ElMessage.info("个人中心功能开发中")
      break
    case "settings":
      ElMessage.info("设置功能开发中")
      break
    case "logout":
      logout()
      break
  }
}//TODO:后续对接前端，根据command跳转到对应页面

//退出登录
function logout(){
  sessionStorage.removeItem("nickname")
  ElMessage.success("已退出登录")
  router.push("/login")
  //TODO:后续对接后端，清理登录态(token)后再跳转登录页
}

//加载历史对话菜单
function queryHistoryMenu(){
  proxy.$axios({
    url:'history/queryHistoryMenu/'+sessionStorage.getItem("usersId"),
    method:"get"
  }).then(res=>{
    historyList.value=res.data.data
  })
}

//加载页面后执行
onMounted(()=>{
  nickname.value = sessionStorage.getItem("nickname") ||"undefined"
  queryHistoryMenu()
})
</script>



<style scoped>
/* ============ 主题色变量 ============ */
.chat-wrapper {
    --el-color-primary: #5b6ef0;
    --el-color-primary-light-3: #7d8bf4;
    --el-color-primary-light-5: #9aa6f7;
    --el-color-primary-light-7: #bcc3fa;
    --el-color-primary-light-8: #cdd2fb;
    --el-color-primary-light-9: #eef0ff;
    --el-color-primary-dark-2: #4a5bda;
}

/* ============ 整体布局 ============ */
.chat-wrapper {
    display: flex;
    height: 100vh;
    width: 100%;
    overflow: hidden;
    background: #f4f5fb;
    font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
    color: #1f2330;
}

/* ============ 左侧边栏 ============ */
.chat-sidebar {
    display: flex;
    flex-direction: column;
    width: 280px;
    flex-shrink: 0;
    background: #ffffff;
    border-right: 1px solid #eceef5;
    box-shadow: 2px 0 12px rgba(31, 35, 48, 0.03);
}

.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 16px 14px;
}

.logo-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #5b6ef0;
}

.logo-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: linear-gradient(135deg, #5b6ef0, #a351c9);
    box-shadow: 0 0 0 3px rgba(91, 110, 240, 0.18);
}

.new-chat-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 8px 12px;
    border-radius: 10px;
    background-image: linear-gradient(135deg, #5b6ef0 0%, #8a4fd0 100%);
    border: none;
    font-weight: 600;
}

.new-chat-btn:hover {
    background-image: linear-gradient(135deg, #4a5bda 0%, #7a42c2 100%);
}

.history-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 18px;
    font-size: 13px;
    color: #a0a4b0;
    letter-spacing: 1px;
}

.history-title-icon {
    font-size: 14px;
}

.history-scroll {
    flex: 1;
    padding: 0 10px;
}

.history-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-bottom: 8px;
}

.history-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 12px;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.2s ease;
    position: relative;
}

.history-item:hover {
    background: #f5f6ff;
}

.history-item.active {
    background: linear-gradient(135deg, #eef0ff, #f3ecff);
}

.history-item.active .history-item-icon {
    color: #5b6ef0;
}

.history-item-icon {
    font-size: 18px;
    color: #b0b4c2;
    flex-shrink: 0;
}

.history-item-body {
    flex: 1;
    min-width: 0;
}

.history-item-title {
    font-size: 14px;
    color: #33384a;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.history-item.active .history-item-title {
    color: #4a5bda;
    font-weight: 600;
}

.history-item-time {
    font-size: 12px;
    color: #b4b8c4;
    margin-top: 3px;
}

.history-item-delete {
    font-size: 15px;
    color: #c0c4d0;
    opacity: 0;
    transition: opacity 0.2s ease, color 0.2s ease;
}

.history-item:hover .history-item-delete {
    opacity: 1;
}

.history-item-delete:hover {
    color: #f56c6c;
}

/* ============ 侧边栏用户信息 ============ */
.sidebar-user {
    padding: 12px;
    border-top: 1px solid #eceef5;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.2s ease;
    outline: none;
}

.user-info:hover {
    background: #f5f6ff;
}

.user-avatar {
    background-color: #0aaeff;
    color: #fff;
    font-weight: 700;
    font-size: 16px;
    flex-shrink: 0;
}

.user-meta {
    flex: 1;
    min-width: 0;
}

.user-name {
    font-size: 14px;
    font-weight: 600;
    color: #1f2330;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.user-role {
    font-size: 12px;
    color: #a0a4b0;
    margin-top: 2px;
}

.user-arrow {
    font-size: 14px;
    color: #b0b4c2;
}

/* ============ 右侧主区域 ============ */
.chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    background: #f4f5fb;
}

.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: #ffffff;
    border-bottom: 1px solid #eceef5;
}

.chat-header-title {
    font-size: 16px;
    font-weight: 700;
    color: #1f2330;
}

.chat-header-sub {
    font-size: 13px;
    color: #a0a4b0;
}

/* ============ 消息区 ============ */
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* 空状态 */
.empty-state {
    margin: auto;
    text-align: center;
    max-width: 520px;
    padding: 40px 20px;
}

.empty-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: linear-gradient(135deg, #5b6ef0 0%, #7b4fd0 50%, #a351c9 100%);
    color: #fff;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 20px;
    box-shadow: 0 12px 28px rgba(91, 110, 240, 0.3);
}

.empty-title {
    font-size: 22px;
    font-weight: 700;
    color: #1f2330;
    margin-bottom: 10px;
}

.empty-desc {
    font-size: 14px;
    color: #8a8f9c;
    margin-bottom: 24px;
}

.empty-suggests {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
}

.suggest-chip {
    padding: 8px 16px;
    border-radius: 999px;
    background: #ffffff;
    border: 1px solid #e4e7f0;
    color: #5b6ef0;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.suggest-chip:hover {
    background: linear-gradient(135deg, #5b6ef0 0%, #8a4fd0 100%);
    color: #fff;
    border-color: transparent;
    box-shadow: 0 6px 16px rgba(91, 110, 240, 0.25);
}

/* 消息行 */
.message-row {
    display: flex;
    gap: 12px;
    max-width: 80%;
}

.message-row.user {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.message-avatar {
    background: #fff;
    color: #5b6ef0;
    font-weight: 700;
    flex-shrink: 0;
    border: 1px solid #eceef5;
}

.message-avatar.assistant {
    background: linear-gradient(135deg, #5b6ef0, #a351c9);
    color: #fff;
    border: none;
}

.message-body {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
}

.message-row.user .message-body {
    align-items: flex-end;
}

.message-role {
    font-size: 12px;
    color: #a0a4b0;
    padding: 0 4px;
}

.message-bubble {
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 14px;
    line-height: 1.65;
    word-break: break-word;
}

.message-bubble.assistant {
    background: #ffffff;
    border: 1px solid #eceef5;
    border-top-left-radius: 4px;
    box-shadow: 0 2px 8px rgba(31, 35, 48, 0.04);
    color: #33384a;
}

.message-bubble.user {
    background: linear-gradient(135deg, #5b6ef0 0%, #8a4fd0 100%);
    color: #fff;
    border-top-right-radius: 4px;
    box-shadow: 0 6px 16px rgba(91, 110, 240, 0.22);
}

/* Markdown 渲染样式 */
.markdown-body :deep(p) {
    margin: 0 0 8px;
}

.markdown-body :deep(p:last-child) {
    margin-bottom: 0;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
    margin: 12px 0 8px;
    font-weight: 700;
    color: #1f2330;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
    padding-left: 20px;
    margin: 4px 0 8px;
}

.markdown-body :deep(li) {
    margin: 3px 0;
}

.markdown-body :deep(pre) {
    background: #f6f7fb;
    border: 1px solid #eceef5;
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
    margin: 8px 0;
}

.markdown-body :deep(code) {
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 13px;
    background: #eef0ff;
    color: #4a5bda;
    padding: 2px 6px;
    border-radius: 4px;
}

.markdown-body :deep(pre code) {
    background: transparent;
    color: #33384a;
    padding: 0;
}

.markdown-body :deep(blockquote) {
    border-left: 3px solid #5b6ef0;
    margin: 8px 0;
    padding: 2px 12px;
    color: #8a8f9c;
    background: #f8f9fd;
    border-radius: 0 6px 6px 0;
}

.markdown-body :deep(a) {
    color: #5b6ef0;
}

.markdown-body :deep(strong) {
    color: #1f2330;
}

/* ============ 底部输入区 ============ */
.chat-input-area {
    display: flex;
    align-items: flex-end;
    gap: 12px;
    padding: 16px 24px 20px;
    background: #ffffff;
    border-top: 1px solid #eceef5;
}

.chat-input :deep(.el-textarea__inner) {
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 0 0 1px #e4e7ed inset;
    transition: box-shadow 0.2s ease;
    background: #f8f9fd;
}

.chat-input :deep(.el-textarea__inner:focus) {
    box-shadow: 0 0 0 1.5px #5b6ef0 inset;
    background: #fff;
}

.send-btn {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    border: none;
    background-image: linear-gradient(135deg, #5b6ef0 0%, #8a4fd0 100%);
    flex-shrink: 0;
}

.send-btn:not(.is-disabled):hover {
    background-image: linear-gradient(135deg, #4a5bda 0%, #7a42c2 100%);
}

.send-btn.is-disabled {
    background-image: linear-gradient(135deg, #c0c4d3 0%, #c9c2d6 100%);
}

.send-btn .el-icon {
    font-size: 20px;
}

/* 隐藏滚动条，保留滚动能力 */
.chat-messages {
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE / Edge */
}

.chat-messages::-webkit-scrollbar {
    display: none;
}
</style>
