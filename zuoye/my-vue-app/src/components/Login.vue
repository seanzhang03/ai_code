<template>
    <div>
        <form>
            邮箱号：<input type="text" :disabled="isSend" v-model="email"> <br>
            验证码：<input type="text" :disabled="!isSend" v-model="captcha"> <br>
            <button type="button" :disabled="isSend" @click="sendCaptcha">发送</button>
            <button type="button" :disabled="!isSend">登录</button>
        </form>
    </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";

// 获取实例对象 --- 用于访问全局配置中的内容
let proxy = getCurrentInstance().proxy

// 定义一个变量控制邮箱号、验证码、发送按钮、登录按钮的显示与隐藏
let isSend = ref(false);
// 定义2个变量：邮箱号、验证码
let email = ref('3503294776@qq.com');
let captcha = ref('');


// 发送验证码
function sendCaptcha() {
    isSend.value = !isSend.value; // 修改状态
    proxy.$axios({ // 使用全局配置中的axios
        url: 'users/sendCaptcha', // 访问的接口地址，默认自动拼接上全局配置中的baseURL
        method: 'get', // 设置请求方式，默认get
        params: { // get请求设置客户端给服务器的参数，键值对格式，其中键需要和服务器端一致
            email: email.value,
        },
    }).then(res => { // then就是接收服务器响应内容、res就是响应的内容对象【形参】
        // let data = res.data // 取出res对象中的data属性的值
        console.log(res);
    });
}


</script>

<style scoped>

</style>