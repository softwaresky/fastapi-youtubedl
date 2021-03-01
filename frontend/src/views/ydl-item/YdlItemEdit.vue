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
               @change="changedUrlInput"
               required>
        <label for="input-formats"></label>
        <select name="formats" id="input-formats" v-model="selectedFormat" @change="changedFormat($event.target.value)">
          <option value="0">-- format --</option>
          <option v-for="(format, index) in readUrlInfo.formats" :key="index" :value="format.format_id">{{format.format}} {{format.fps}} {{format.ext}} </option>
        </select>
      </div>
      <div class="form-group-check">
        <fieldset>
          <legend>Additional options </legend>
<!--          <input type="checkbox" v-model="isPlaylist" name="Playlist" @change="changedIsPlaylist($event.target.checked)">Playlist<br>-->
          <input type="checkbox" v-model="isPlaylist" name="Playlist" @change="changedIsPlaylist($event.target.checked)">Playlist<br>
          <input type="checkbox" v-model="isOnlyAudio" name="Only Audio" @change="changedAudioOnly($event.target.checked)">Only Audio<br>
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
                  v-model="ydlOptsStr"
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
import {YdlItemCreate, YdlItemUpdate, YdlUrlInfoCreate} from '@/store/ytdl_item/state';
import {dispatchCreateYdlItem, dispatchGetYdlItems, dispatchUpdateYdlItem, dispatchGetYdlUrlInfo} from '@/store/ytdl_item/actions'
import {readYtdItem, readYtdUrlInfo} from '@/store/ytdl_item/getters'

function JsonParse(value: string) {
  try {
    return JSON.parse(value);
  } catch (error) {
    console.log(error);
  }
}


@Component
export default class YdlItemEdit extends Vue {

  public ydlObj: YdlItemCreate = {
    url: "",
    'do_calculate_pattern': false,
    'ydl_opts': {},
    info: {},
    status: 1
  };
  public ydlOpts = {};
  public isPlaylist = false;
  public isOnlyAudio = false;
  public btnTitle = "Add New YoutubeDl item";
  public selectedFormat = 0;

  get currentYtdItem() {
    return readYtdItem(this.$store)(+this.$router.currentRoute.params.id)
  }

  get readUrlInfo() {
    return readYtdUrlInfo(this.$store);
  }

  get ydlOptsStr() {
    return JSON.stringify(this.ydlOpts);
  }

  public async mounted() {
    await dispatchGetYdlItems(this.$store);

    if (this.currentYtdItem) {
      this.btnTitle = 'Edit';
      this.ydlObj = {
        ...this.currentYtdItem
      };
    }

    this.ydlOpts = {
      ...this.ydlOpts,
      noplaylist: true,
    }
  }

  public async changedUrlInput() {

    if (this.ydlObj.url) {

      const urlInfo: YdlUrlInfoCreate = {
        url: this.ydlObj.url,
        'ydl_opts': this.ydlObj.ydl_opts
      }

      await dispatchGetYdlUrlInfo(this.$store, urlInfo);

    }
  }

  public changedFormat(value: number) {

    if (value > 0) {
      this.ydlOpts = {
        ...this.ydlOpts,
        format: value,
      };
    } else {
      if ("format" in this.ydlOpts) {
        delete this.ydlOpts["format"];
      }
    }
  }

  public changedIsPlaylist(checked: boolean) {

    if (checked) {
      if ('noplaylist' in this.ydlOpts) {
        delete this.ydlOpts["noplaylist"];
      }
    } else {
      this.ydlOpts = {
        ...this.ydlOpts,
        noplaylist: !checked,
      };
    }

  }

  public changedAudioOnly(checked: boolean) {

    if (checked) {

      this.ydlOpts = {
        ...this.ydlOpts,
        'format': 'bestaudio/best',
        'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
        }],
      }
      // if (!("format" in this.ydlOpts)) {
      //   this.ydlOpts = {
      //     ...this.ydlOpts,
      //     "format": 'bestaudio/best',
      //   }
      // }
    } else {
      if ("postprocessors" in this.ydlOpts) {
        delete this.ydlOpts["postprocessors"];
      }
      if ("format" in this.ydlOpts) {
        if (typeof this.ydlOpts["format"] === "string") {
          delete this.ydlOpts["format"];
        }

      }

    }

  }

  public async submitYdlItem() {

    if (this.currentYtdItem) {
      const ydlItemUpdate: YdlItemUpdate = {
        ...this.ydlObj,
        info: this.readUrlInfo
      }
      await dispatchUpdateYdlItem(this.$store, {id: this.currentYtdItem.id, ydlItem: ydlItemUpdate});
    } else {
      if (this.ydlObj.url) {

        this.ydlObj = {
          ...this.ydlObj,
          info: this.readUrlInfo
        }

        // let ydlOpts = {};

        // if (this.selectedFormat > 0) {
        //   ydlOpts = {
        //     ...ydlOpts,
        //     "format": this.selectedFormat
        //   }
        // }

        // if (!this.isPlaylist) {
        //   ydlOpts = {
        //     ...ydlOpts,
        //     'noplaylist': true
        //   }
        // }

        // if (this.isOnlyAudio) {
        //   ydlOpts = {
        //     ...ydlOpts,
        //     'format': 'bestaudio/best',
        //     'postprocessors': [{
        //       'key': 'FFmpegExtractAudio',
        //       'preferredcodec': 'mp3',
        //       'preferredquality': '192',
        //     }],
        //   }
        // }
        this.ydlObj['ydl_opts'] = this.ydlOpts;
        console.log(this.ydlObj);
        // await dispatchCreateYdlItem(this.$store, this.ydlObj);
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