<template>
  <div>
    <h4>asdasdasd</h4>
    <data-tables
        :data="allYdlItems"
        :total="allYdlItems.length"
    >
      <el-table-column
          label="Url"
          prop="url"
          sortable
      />
      <el-table-column
          label="Status"
          prop="status"
          sortable
      />
      <el-table-column
          label="Auto cal. pattern"
          prop="do_calculate_pattern"
      />
      <el-table-column
          label="Timestamp"
          prop="timestamp"
          sortable
      />
      <el-table-column
          label="Add. Options"
          prop="ydl_opts"
      />
    </data-tables>

  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import {dispatchCreateYdlItem, dispatchGetYdlItems, dispatchUpdateYdlItem} from '@/store/ytdl_item/actions';
import {readAllYtdItems} from '@/store/ytdl_item/getters';

/*
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    do_calculate_pattern = Column(Boolean, default=False)
    status = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    ydl_opts = Column(JSON)
    output_log = Column(JSON)
 */

@Component
export default class YdlItemsView extends Vue {

  public async mounted() {
    await dispatchGetYdlItems(this.$store);
  }

  get allYdlItems() {
    return readAllYtdItems(this.$store);
  }
}
</script>

<style scoped>

</style>