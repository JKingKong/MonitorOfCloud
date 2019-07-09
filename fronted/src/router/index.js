import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/warn',
    children: [{
      path: 'warn',
      name: 'Info',
      component: () => import('@/views/warn/index'),
      meta: { title: '预警信息', icon: 'dashboard' }
    }]
  },
  // {
  //   path: '/',
  //   component: Layout,
  //   redirect: '/warn',
  //   children: [{
  //     path: 'warn',
  //     name: 'Dashboard',
  //     component: () => import('@/views/warn/index'),
  //     meta: { title: '预警信息', icon: 'warn' }
  //   }]
  // },

  {
    path: '/sort',
    component: Layout,
    children: [
      {
        path: 'info',
        name: 'Table',
        component: () => import('@/views/exception_info/index'),
        meta: { title: '异常地点排序', icon: 'table' }
      }
    ]
  },

  {
    path: '/video',
    component: Layout,
    children: [
      {
        path: 'info',
        name: 'Form',
        component: () => import('@/views/check_video/index'),
        meta: { title: '异常视频查看', icon: 'form' }
      }
    ]
  },
  {
    path: '/address',
    component: Layout,
    children: [
      {
        path: 'list',
        component: () => import('@/views/threshold/index'),
        meta: { title: '监控阈值设置',icon: 'nested' }
      }
    ]
  },
  {
    path: '/deal',
    component: Layout,
    children: [
      {
        path: 'edge_video',
        component: () => import('@/views/dealvideo/index'),
        meta: { title: '选择处理视频',icon: 'nested' }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
