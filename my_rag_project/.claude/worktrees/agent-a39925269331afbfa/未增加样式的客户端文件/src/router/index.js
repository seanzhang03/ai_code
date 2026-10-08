import {createRouter,createWebHistory} from "vue-router"

//创建路由对象
const router = createRouter({
    //配置路由的数组，每一个页面都以js对象形式定义在routes数组中，路由即请求路径
    //若使用hash模式，访问路径会多出一个#/
    history:createWebHistory(),
    routes:[//后面要配置请求路径直接写在routes里
        //登录页面路由配置
        {
            path:"/login",  //访问路径，拼接在http://localhost:5173/后面
            component:()=>import("../components/Login.vue")//通过前面设置的路径访问到该组件
        },
        //对话页面路由配置
        {
            path:"/chat",
            component:()=>import("../components/Chat.vue")
        },
        //用户注册页面路由配置
        {
            path:"/registration",
            component:()=>import("../components/Registration.vue")
        },
        //用户修改密码路由配置
        {
            path:"/password",
            component:()=>import("../components/Password.vue")
        },
        //管理员路由配置
        {
            path:"/admin",
            component:()=>import("../components/Admin.vue")
        },

    ]
})

//导出路由对象，提供给其他模块使用
export default router