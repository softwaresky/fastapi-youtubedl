<template>
  <div>
    <h4>List of download items</h4>
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
          :formatter="columnFormatter"
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

      >
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span style="margin-left: 10px">{{ columnFormatter(scope.row, scope.column) }} </span>
        </template>
      </el-table-column>
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
import moment from 'moment';

enum statusName {

  'Not Found' = 0,
  Pending = 1,
  Running = 2,
  Error = 3,
  Finished = 4,
}

@Component
export default class YdlItemsView extends Vue {

  public async mounted() {
    await dispatchGetYdlItems(this.$store);
  }

  get allYdlItems() {
    return readAllYtdItems(this.$store);
  }

  public columnFormatter(row: any, column: any) {

    const cellValue = row[column.property];

    if (column.property.includes('time')) {
      if (cellValue) {
        return moment(cellValue).format('MM/DD/YY HH:mm');
      } else if (column.property == 'elapsed_time' && row['start_time'] && row['end_time']) {
        return moment.utc(moment(row['end_time']).diff(moment(row['start_time']))).format('HH:mm:ss');
      } else {
        return ' N/A';
      }
    } else if (column.property === 'status') {
      return statusName[cellValue];
    }

    return cellValue;
  }
}
</script>

<style scoped>

</style>