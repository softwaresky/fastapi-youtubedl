<template>
  <div>
    <h4>List of download items</h4>
    <div class="table-controls">
      <el-button @click="clickedAddNew">Add New</el-button>
    </div>
    <data-tables
        :data="allYdlItems"
        :total="allYdlItems.length"
        :table-props="{rowKey: 'id', 'default-sort': {prop: 'timestamp', order: 'ascending'}}"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <p>{{ props.row.output_log }}</p>
        </template>
      </el-table-column>

      <el-table-column
          label="Url"
          prop="url"
          sortable
      >
        <template slot-scope="scope">
          <a :href="scope.row.url">{{scope.row.url}}</a>
        </template>
      </el-table-column>
      <el-table-column
          label="Progress"
          prop="tmp"
      >
        <template slot-scope="scope">
          <el-progress :text-inside="true" :stroke-width="26"
                       :percentage="customProgress(scope.row)">

          </el-progress>

        </template>
      </el-table-column>
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
      <el-table-column label="Actions" width="370">
        <template slot-scope="scope">
          <el-button v-for="button in customQueryButtonsForRow(scope.row)"
                     :key="button.name"
                     :type="button.type"
                     :icon="button.icon"
                     @click="button.handler"
                     size="medium"
          >
            {{ button.label }}
          </el-button>
        </template>
      </el-table-column>
    </data-tables>

  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import {dispatchCreateYdlItem, dispatchGetYdlItems, dispatchUpdateYdlItem, dispatchGetYdlItemsData, dispatchRemoveYdlItem} from '@/store/ytdl_item/actions';
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

  public isLoading = false;

  public async mounted() {
    // await dispatchGetYdlItems(this.$store);
    this.dispatchGetYdlItemsData();
    setInterval(this.dispatchGetYdlItemsData,6000);
  }

  public async dispatchGetYdlItemsData() {
    this.isLoading = true;
    await dispatchGetYdlItemsData(this.$store);
    this.isLoading = false;
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

  public customProgress(row: any) {
    let percentage = 0;

    if (row.output_log && row.output_log.hasOwnProperty('downloaded_bytes')) {
      percentage = ((row.output_log.downloaded_bytes / row.output_log.total_bytes) * 100);

    }
    return percentage;
  }

  public clickedAddNew() {
    this.$router.push("/ydl/new");
  }
  public async removeItem(id: number) {
    await dispatchRemoveYdlItem(this.$store, {id: id});
  }
  public customQueryButtonsForRow(row: any) {
    console.log(row);

    return [
      {
        type: 'primary',
        icon: 'el-icon-edit',
        name: 'edit',
        label: 'Edit',
        handler: (_: any) => {
          this.$router.push(`/ydl/edit/${row.id}`);
        }
      },
      {
        type: 'danger',
        icon: 'el-icon-remove',
        name: 'remove',
        label: 'Remove',
        handler: (_: any) => {
          this.removeItem(row.id);
        }
      }
    ];
  }
}
</script>

<style scoped>
.table-controls {
  width: 100%;
  display: inline-flex;
  justify-content: flex-start;
  margin: 5px 10px;
}
</style>