//引入路由配置文件
import {createRouter,createWebHistory} from "vue-router";

//定义路由配置对象---数组
const routes=[
    {//一个页面的访问路径就是一个js对象，包含2个属性即可:path/component
        path :'/testOne', //访问路径，和服务器的请求访问规则一致
        component:()=>import('../components/TestOne.vue') //访问组件
    },
    {
        path :'/testTwo',
        component:()=>import('../components/TestTwo.vue')
    },
    {
        path :'',
        component:()=>import('../components/Login.vue')
    },
]

//设置路由模式为history 模式--默认hash模型，访问路径中有一   个#号
const router = createRouter({
    history:createWebHistory(),
    routes
})

//导出路由实例
export default router