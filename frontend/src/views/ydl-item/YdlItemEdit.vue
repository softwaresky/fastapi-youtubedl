<template>
  <div class="input-container">
    <h3>Add new Youtube for download</h3>
    <el-form ref="form" :model="formInputs" :rules="rules" label-width="120px">
      <el-form-item label="Youtube Url: " prop="url">
        <el-input v-model="formInputs.url" @input="changedUrlInput"
                  placeholder="https://www.youtube.com/..."></el-input>
      </el-form-item>
      <el-form-item label="Format: ">
        <el-select v-model="formInputs.format">
          <el-option value="best" label="best"></el-option>
          <el-option v-for="(format, index) in readUrlInfo.formats" :key="index" :value="format.format_id"
                     :label="readUrlInfo.best_video_format.format_id === format.format_id ||
                     readUrlInfo.best_audio_format.format_id === format.format_id ?
                     format.format + ' ' + format.fps + ' ' + format.ext + ' (best)':
                     format.format + ' ' + format.fps + ' ' + format.ext">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="Pattern: " prop="pattern">
        <el-input v-model="formInputs.pattern" class="input-with-select"
                  placeholder="enter pattern ex. %(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s">
          <el-button slot="append" @click="clickedBtnHelp">?</el-button>
        </el-input>
      </el-form-item>

      <el-form-item label="">
        <el-checkbox v-model="formInputs.isPlaylist">Playlist</el-checkbox>
        <el-checkbox v-model="formInputs.isOnlyAudio">Only Audio</el-checkbox>
        <el-checkbox v-model="formInputs.doCalculatePattern">Auto calculate pattern</el-checkbox>
      </el-form-item>

      <el-form-item label="">
        <el-collapse>
          <el-collapse-item title="Advanced options">
            <el-input type="textarea" v-model="formInputs.ydlOptsAddStr" placeholder="Add more options"
                      :rows="5"></el-input>
          </el-collapse-item>
          <div v-if="!ydlOptsAddValidate" class="ydlAddOutputError">
            <p>
              * textarea value require JSON structure.
            </p>
          </div>
        </el-collapse>
      </el-form-item>
      <el-form-item label="">
        <el-collapse>
          <el-collapse-item title="Full Ydl Options">
            <div>
              <pre>{{ ydlOptsFull | pretty }}</pre>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitYdlItem">{{ btnTitle }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts">
import {Component, Vue, Emit, Prop} from "vue-property-decorator";
import {YdlItemCreate, YdlItemUpdate, YdlUrlInfoCreate, YdlItemState} from '@/store/ytdl_item/state';
import {
  dispatchCreateYdlItem,
  dispatchGetYdlItems,
  dispatchUpdateYdlItem,
  dispatchGetYdlUrlInfo
} from '@/store/ytdl_item/actions'
import {readYtdItem, readYtdUrlInfo} from '@/store/ytdl_item/getters'

@Component
export default class YdlItemEdit extends Vue {

  @Prop({type: Object as () => YdlItemState})
  public data!: YdlItemState

  public ydlObj: YdlItemCreate = {
    url: "",
    'do_calculate_pattern': false,
    'ydl_opts': {},
    info: {},
    status: 1
  };
  public formInputs = {
    url: "",
    pattern: "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",
    format: "best",
    isPlaylist: false,
    isOnlyAudio: false,
    doCalculatePattern: false,
    ydlOptsAddStr: "{}"
  };

  public rules = {
    url: [
      {required: true, message: 'Please input youtube url', trigger: 'blur'}
    ]
  };

  public ydlOptsAddStr = "{}";
  public ydlOptsAddValidate = true;

  get btnTitle() {
    if (this.currentYtdItem) {
      return "Edit"
    }
    return "Create"
  }

  get currentYtdItem() {

    if (this.data && this.data.id > 0) {
      return this.data;
    }
    return readYtdItem(this.$store)(+this.$router.currentRoute.params.id)
  }

  get readUrlInfo() {
    return readYtdUrlInfo(this.$store);
  }

  get ydlOptsValues() {

    let ydlOpts = {}

    ydlOpts = {
      ...ydlOpts,
      format: this.formInputs.format
    }

    if (this.formInputs.pattern) {
      ydlOpts = {
        ...ydlOpts,
        outtmpl: this.formInputs.pattern
      }
    }

    if (!this.formInputs.isPlaylist) {
      ydlOpts = {
        ...ydlOpts,
        noplaylist: true
      }
    }

    if (this.formInputs.isOnlyAudio) {
      ydlOpts = {
        ...ydlOpts,
        postprocessors: [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
        }],

      }

      if (this.formInputs.format === "best") {
        ydlOpts = {
          ...ydlOpts,
          format: 'bestaudio/best',
        }
      }
    }

    return ydlOpts;
  }

  get ydlOptsFull() {

    let ydlOptsAdd = {};
    try {
      ydlOptsAdd = JSON.parse(this.formInputs.ydlOptsAddStr);
      this.ydlOptsAddValidate = true;
    } catch (error) {
      this.ydlOptsAddValidate = false;
    }

    return {
      ...this.ydlOptsValues,
      ...ydlOptsAdd
    }
  }

  public async mounted() {
    await dispatchGetYdlItems(this.$store);

    if (this.currentYtdItem) {
      this.formInputs = {
        ...this.formInputs,
        ...this.currentYtdItem.ydl_opts,
        url: this.currentYtdItem.url,
        doCalculatePattern: this.currentYtdItem.do_calculate_pattern
      };
    }
  }

  public async dispatchUrlInfo() {

    if (this.formInputs.url) {
      // this.ydlObj.url = this.formInputs.url;
      // this.ydlObj['ydl_opts'] = this.ydlOptsFull;
      //
      // const urlInfo: YdlUrlInfoCreate = {
      //   url: this.ydlObj.url,
      //   'ydl_opts': this.ydlObj.ydl_opts
      // }

      const urlInfo: YdlUrlInfoCreate = {
        url: this.formInputs.url,
        'ydl_opts': this.ydlOptsFull
      }
      await dispatchGetYdlUrlInfo(this.$store, urlInfo);
    }
  }

  public async changedUrlInput() {
    await this.dispatchUrlInfo();
  }

  public clickedBtnHelp() {
    window.open("https://github.com/ytdl-org/youtube-dl#output-template", "_blank");
  }

  public async submitYdlItem() {

    const newYdl: YdlItemCreate = {
      url: this.formInputs.url,
      'do_calculate_pattern': this.formInputs.doCalculatePattern,
      'ydl_opts': this.ydlOptsFull,
      info: this.readUrlInfo,
      status: 1
    };

    if (this.currentYtdItem) {
      const ydlItemUpdate: YdlItemUpdate = {
        ...newYdl
      }
      await dispatchUpdateYdlItem(this.$store, {id: this.currentYtdItem.id, ydlItem: ydlItemUpdate});

    } else {
      if (this.formInputs.url) {

        if (!this.readUrlInfo || (this.readUrlInfo && Object.keys(this.readUrlInfo).length === 0)) {
          await this.dispatchUrlInfo();
        }

        // this.ydlObj = {
        //   ...this.ydlObj,
        //   info: this.readUrlInfo
        // }
        // this.ydlObj['do_calculate_pattern'] = this.formInputs.doCalculatePattern;
        // this.ydlObj['ydl_opts'] = this.ydlOptsFull;

        await dispatchCreateYdlItem(this.$store, newYdl);
      }
    }

    this.$router.push("/");

  }

}
</script>

<style scoped>

.input-container {
  /*width: 70%;*/
  margin: 0 auto;
  text-align: left;
}

</style>