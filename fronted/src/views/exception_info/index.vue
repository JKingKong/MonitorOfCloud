<template>
  <div class="app-container">
    <el-table
      :data="ExceptionsInfo"
      stripe
      :default-sort = "{prop: 'exception_times', order: 'descending'}"
    >
      <el-table-column
        label="地址"
        align="center"
        prop="address">

      </el-table-column>

      <el-table-column
        label="异常次数"
        width="500"
        align="center"
        sortable
        prop="exception_times">
      </el-table-column>

    </el-table>
  </div>
</template>

<script>

export default {
    data() {
      return {
        // tableData: [{
        //   address: 'A',
        //   exception_times: '10'
        // }, {
        //   address: 'B',
        //   exception_times: '23'
        // },
        //   {
        //   address: 'C',
        //   exception_times: '15'
        // }],
        ExceptionsInfo:[]
      }
    },
    mounted: function () {
        this.getExceptionsInfo();
    },
    methods: {
            getExceptionsInfo() {
                    this.$axios.get("/exceptions_info/").then((response) => {
                        this.ExceptionsInfo = response.data['exceptions_info'];
                    }).catch((error) => {

                    })
            }
    },
}
</script>
