import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import RouterComponent from '@/components/layout/RouterComponent.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
    // children: [
    //   {
    //     path: 'ydl',
    //     children: [
    //       {
    //         path: 'new',
    //         name: 'ydl-new',
    //         component: () => import(/* webpackChunkName: "about" */ "@/views/ydl-item/YdlItemEdit.vue")
    //       },
    //       {
    //         path: 'edit/:id',
    //         name: 'ydl-edit',
    //         component: () => import(/* webpackChunkName: "about" */ "@/views/ydl-item/YdlItemEdit.vue")
    //       }
    //     ]
    //   }
    // ]
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/ydl/new",
    component: () => import(/* webpackChunkName: "about" */ "@/views/ydl-item/YdlItemEdit.vue")
  },
  {
    path: '/*', redirect: '/',
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
