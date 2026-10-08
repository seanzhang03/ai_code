import {createRouter,createWebHashHistory,createWebHistory} from "vue-router"

//创建路由对象
const router = createRouter({
    //配置路由的数组，每一个页面的路由都以js对象的形式定义在routes数组中，路由就是请求路径
    //使用hash模式，hash模式访问路径会多出一个#/
    //history:createWebHashHistory(),
    history:createWebHistory(),
    routes:[//后面要配路由直接写在routes里
        {
            path:"/",  //访问路径，拼接在http://localhost:5173/后面，5173是vite开发服务器的默认端口
            meta:{
                isLogin:false //不需要拦截处理，isLogin是一个标识符，可以任意起名
            },
            component:()=> import("../components/HelloWorld.vue")//通过上面的路径可以访问到这里的组件
        },
        {
            path:"/login",
            component:()=>import("../components/login.vue")
        },
        {
            path:"/chat",
            component:()=>import("../components/Chat.vue"),
            meta:{
                isLogin: true //需要拦截处理[登录了才可以访问]，需要授权
            }
        }
    ],
})




//导出路由对象，提供给其他模块来使用
export default router
