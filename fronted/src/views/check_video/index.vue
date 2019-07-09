<template>
  <div class="app-container" style="text-align: center">

    <el-autocomplete
      style="width: 50%;"
      clearable="True"
      v-model="input"
      prefix-icon="el-icon-search"
      :fetch-suggestions="querySearch"
      placeholder="请输入地址..."
      @select="getExceptionsVideoInfo"
      @keyup.enter.native="getExceptionsVideoInfo"
    ></el-autocomplete>


    <el-table
      :data="video_info"
      :default-sort="{prop: 'time', order: 'descending'}"
    >
      <el-table-column
        label="视频ID"
        align="center"
        prop="vid">
      </el-table-column>

      <el-table-column
        label="地址"
        align="center"
        prop="address">
      </el-table-column>

      <el-table-column
        label="异常人数"
        align="center"
        sortable
        prop="number">
      </el-table-column>

      <el-table-column
        label="时间"
        align="center"
        sortable
        prop="time">
      </el-table-column>

      <el-table-column
        label="查看视频"
        align="center"
      >
        <template slot-scope="scope">
          <!--<el-button type="success" icon="el-icon-check" circle-->
                     <!--@click="DialogVisible = true;">-->
          <!--</el-button>-->
           <video width="70%" height="70%" :src="scope.row.video_path" controls>
           </video>
        </template>

      </el-table-column>

    </el-table>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        video_info: [],
        addressList: [],
        input: '',
      }
    },
    mounted: function () {
      this.getAddressList();
    },
    methods: {
      getExceptionsVideoInfo() {
        // 在输入框输入address，点击回车后调用此方法
        this.$axios.get("/video_info/", {
            params: {
              address: this.input,
            },
          }
        ).then((response) => {
          this.video_info = response.data['video_info'];
        }).catch((error) => {

        })
      },

      getAddressList() {
        // 获取{"value":"这里是一个地址的值"}  用来提供地点的输入建议
        this.$axios.get("/address_value/").then((response) => {
          this.addressList = response.data['address_value'];
        }).catch((error) => {

        })
      },

      // 下边三个函数都是为了提供给输入建议的辅助函数(element-ui提供的)
      querySearch(queryString, cb) {
        var addressList = this.addressList;
        // 输入字符串： 则results==通过匹配输入的字符串所剩下的addressList
        // 不输入字符串： 返回addressList
        var results = queryString ? addressList.filter(this.createFilter(queryString)) : addressList;
        // 调用 callback 返回建议列表的数据  读取的是字典里键名为: value 所对应的键值
        cb(results);
      },
      createFilter(queryString) {
        return (addressList) => {
          return (addressList.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      log(vp) {
        console.log(vp);
      }
    },
  }
</script>

<style scoped>
  .line {
    text-align: center;
  }
</style>

