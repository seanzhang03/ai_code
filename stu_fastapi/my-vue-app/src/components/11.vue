<template>
<template>
    <div>
        <!-- ============ 左侧：历史记录 + 用户信息 ============ -->
        <aside>
            <!-- 顶部 Logo 与新建对话 -->
            <div>
                <div>RAG</div>
                <button @click="createNewChat">新对话</button>
            </div>

            <!-- 历史记录标题 -->
            <div>
                <span>历史记录</span>
            </div>

            <!-- 历史记录列表 -->
            <div>
                <div
                        v-for="item in historyList"
                        :key="item.historyId"
                        @click="selectHistory(item.historyId)"
                >
                    <div>
                        <div>{{ item.question }}</div>
                        <div>{{ item.createTime }}</div>
                    </div>
                    <button @click.stop="deleteHistory(item.historyId)">删除</button>
                </div>
            </div>

            <!-- 底部：当前用户信息 -->
            <div>
                <div>
                    <span>{{ nickname }}</span>
                    <select @change="handleUserCommand($event.target.value)">
                        <option value="profile">个人中心</option>
                        <option value="settings">设置</option>
                        <option value="logout">退出登录</option>
                    </select>
                </div>
            </div>
        </aside>

        <!-- ============ 右侧：对话主区域 ============ -->
        <main>
            <!-- 顶部标题栏 -->
            <header>
                <div>{{ currentTitle }}</div>
                <div>{{ nickname }} 与 RAG 助手</div>
            </header>

            <!-- 消息区 -->
            <div ref="messageBox">
                <!-- 空状态：欢迎引导 -->
                <div v-if="messages.length === 0">
                    <div>RAG</div>
                    <div>你好，{{ nickname }} 👋</div>
                    <div>我是 RAG 检索增强问答助手，可以基于知识库为你解答问题</div>
                    <div>
                        <span
                                v-for="q in suggestQuestions"
                                :key="q"
                                @click="quickAsk(q)"
                        >{{ q }}</span>
                    </div>
                </div>

                <!-- 消息列表 -->
                <div
                        v-for="(item, index) in messages"
                        :key="index"
                >
                    <div>
                        <div>{{ item.role === 'assistant' ? 'RAG 助手' : nickname }}</div>
                        <div>
                            <span v-if="item.role === 'user'">{{ item.content }}</span>
                            <div v-else v-html="$renderMarkdown(item.content)"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 底部输入区 -->
            <div>
                <textarea
                        v-model="question"
                        rows="1"
                        placeholder="向 cc 提问，Enter 发送，Shift + Enter 换行"
                        @keydown.enter.exact.prevent="handleEnter"
                ></textarea>
                <button
                        :disabled="isButtonDisabled"
                        @click="chat"
                >
                    <span v-show="!isLoading">发送</span>
                    <span v-show="isLoading">加载中...</span>
                </button>
            </div>
        </main>
    </div>
</template>

</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";

</script>

<style scoped>

</style>