<template>
  <div class="input-container">
    <h3>Add new Youtube for download</h3>
    <form @submit.prevent="submitYdlItem">
      <div class="form-group">
        <label for="input-url">Enter an https://youtube.com/ URL</label>
        <input v-model="ydlObj.url"
               type="url"
               name="input-url"
               id="input-url"
               placeholder="https://www.youtube.com/..."
               size="30"
               required>
      </div>
      <div class="form-group-check">
        <fieldset>
          <legend>Additional options </legend>
          <input type="checkbox" v-model="isPlaylist" name="Playlist" >Playlist<br>
          <input type="checkbox" v-model="isOnlyAudio" name="Only Audio">Only Audio<br>
        </fieldset>
      </div>
      <div class="form-group-check">
        <input v-model="ydlObj.do_calculate_pattern"
               type="checkbox"
               name="input-do-calculate-pattern"
               id="input-do-calculate-pattern"/>
        <label for="input-do-calculate-pattern">Auto calculate pattern</label>
      </div>
      <div class="form-group">
        <label for="textarea-additional-options">Additional Options: </label>
        <textarea
                  v-model="ydlOpts"
                  name="textarea-additional-options"
                  id="textarea-additional-options"
                  placeholder="Enter Additional Options in JSON format."
                  rows="6"
                  cols="50"
        />

      </div>
      <div class="form-group">
        <button class="btn input">{{ btnTitle }}</button>
      </div>

    </form>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import {YdlItemCreate, YdlItemUpdate} from '@/store/ytdl_item/state';
import {dispatchCreateYdlItem, dispatchGetYdlItems, dispatchUpdateYdlItem} from '@/store/ytdl_item/actions'
import {readYtdItem} from '@/store/ytdl_item/getters'

@Component
export default class YdlItemEdit extends Vue {

  public ydlObj: YdlItemCreate = {
    url: "",
    'do_calculate_pattern': false,
    'ydl_opts': {},
    status: 1
  };
  public ydlOpts = "";
  public isPlaylist = false;
  public isOnlyAudio = false;
  public btnTitle = "Add New YoutubeDl item";

  get currentYtdItem() {
    return readYtdItem(this.$store)(+this.$router.currentRoute.params.id)
  }

  public async mounted() {
    await dispatchGetYdlItems(this.$store);

    if (this.currentYtdItem) {
      this.btnTitle = 'Edit';
      this.ydlObj = {
        ...this.currentYtdItem
      };
    }
  }


  public async submitYdlItem() {

    if (this.currentYtdItem) {
      const ydlItemUpdate: YdlItemUpdate = {
        ...this.ydlObj
      }
      await dispatchUpdateYdlItem(this.$store, {id: this.currentYtdItem.id, ydlItem: ydlItemUpdate});
    } else {
      if (this.ydlObj.url) {

        let ydlOpts = {};

        if (!this.isPlaylist) {
          ydlOpts = {
            ...ydlOpts,
            'noplaylist': true
          }
        }
        if (this.isOnlyAudio) {
          ydlOpts = {
            ...ydlOpts,
            'format': 'bestaudio/best',
            'postprocessors': [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'mp3',
              'preferredquality': '192',
            }],
          }
        }
        this.ydlObj['ydl_opts'] = ydlOpts;
        // console.log(this.ydlObj);
        // console.log(this.testOptions);
        await dispatchCreateYdlItem(this.$store, this.ydlObj);
      }
    }


  }

}
</script>

<style scoped>

.input-container {
  width: 740px;
  margin: 0 auto;
  text-align: left;
}

.form-group {
  margin: 10px 0;

}

.form-group label {
  display: block;
  padding: 5px 0;
}

.form-group input {
  width: 100%;
}

.form-group textarea {
  width: 100%;
}

.form-group-check {

}

.btn input {
  min-width: 100px;
}
</style>