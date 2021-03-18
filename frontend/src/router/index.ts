import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import YdlItemEdit from "@/views/ydl-item/YdlItemEdit.vue";
import YdlItemsView from "@/views/ydl-item/YdlItemsView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    redirect: "/ydl/list"
  },
  {
    path: "/ydl/new",
    name: "ydl-new",
    component: YdlItemEdit
  },
  {
    path: "/ydl/edit/:id",
    name: "ydl-edit",
    component: YdlItemEdit
  },
  {
    path: "/ydl/list",
    component: YdlItemsView
  },
  {
    path: "/*",
    redirect: "/"
  },
];

const router = new VueRouter({
  // mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
