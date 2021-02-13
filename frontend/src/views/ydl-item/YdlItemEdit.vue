<template>
  <div>
    <form @submit.prevent="submitYdlItem">
      <div class="form_control">
        <input v-model="ydlObj.url" type="text" name="url" id="url" placeholder="Url">
      </div>
      <div class="form_control">
        <input v-model="ydlObj.do_calculate_pattern"  type="checkbox" name="do-calculate-pattern" id="do-calculate-pattern" >
        <label for="do-calculate-pattern">Auto calculate pattern</label>
      </div>
      <div class="form_control">
        <input v-model="ydlObj.ydl_opts"  type="text" name="additional_options" id="additional_options" placeholder="Additional Options">
      </div>
      <button >{{btnTitle}}</button>
    </form>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import {YdlItemCreate} from '@/store/ytdl_item/state';
import {dispatchCreateYdlItem} from '@/store/ytdl_item/actions'

@Component
export default class YdlItemEdit extends Vue {

  public ydlObj: YdlItemCreate = {
    url: "",
    'do_calculate_pattern': false,
    'ydl_opts': {},
    status: 1
  };
  public btnTitle = "Add New";

  public async submitYdlItem(){
    if (this.ydlObj.url) {
      await dispatchCreateYdlItem(this.$store, this.ydlObj);
    }

  }

}
</script>

<style scoped>

</style>