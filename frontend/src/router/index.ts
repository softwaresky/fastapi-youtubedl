import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    redirect: "/ydl/list"
  },
  {
    path: "/ydl/new",
    name: "ydl-new",
    component: () => import(/* webpackChunkName: "about" */ "@/views/ydl-item/YdlItemEdit.vue")
  },
  {
    path: "/ydl/edit/:id",
    name: "ydl-edit",
    component: () => import(/* webpackChunkName: "about" */ "@/views/ydl-item/YdlItemEdit.vue")
  },
  {
    path: "/ydl/list",
    component: () => import(/* webpackChunkName: "about" */ "@/views/ydl-item/YdlItemsView.vue")
  },
  // {
  //   path: "/*", redirect: "/",
  // },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
