<template>
  <div class="app-container" style=" text-align: center">
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="选择边缘端要处理的视频">
        <el-select v-model="formInline.value" placeholder="请选择视频..." @change="selectOne">
          <el-option label="Test1.mp4"
                     value="1"
          >
          </el-option>
          <el-option label="Test2.mp4"
                     value="2"
          >
          </el-option>
          <el-option label="Test3.mp4"
                     value="3"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">开始处理</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        formInline: {
          value: '',
        },
        video_path: "",
        flag: true
      }
    },
    created: function () {

    },
    methods: {
      selectOne() {
        let video_list = {
          "1": {
            'address': 'Test_A',
            'video_path': 'edgeapp/Test_Video/t1.mp4'
          },
          "2": {
            'address': 'Test_B',
            'video_path': 'edgeapp/Test_Video/t2.mp4'
          },
          "3": {
            'address': 'Test_C',
            'video_path': 'edgeapp/Test_Video/t3.mp4'
          }
        };
        this.video_path = video_list[this.formInline.value]   // 根据选择框，得出一个video_path
      },
      onSubmit() {
        // console.log(JSON.stringify({"video_list":[this.video_path]}));
        if (this.flag === false) {
          this.$message.error('边缘端已经在处理任务,处理完成后才能再次请求');
        }
        if (this.video_path !== '' && this.flag) {
          this.flag = false;
          this.$axios({
            url: 'http://127.0.0.1:8000/start_recognize/',
            method: 'post',
            //发送格式为json
            data: JSON.stringify({"video_list": [this.video_path]}),
            headers: {
              'Content-Type': 'application/json'
            },
            timeout: 1000 * 60 * 5
          })
            .then((response) => {
              this.flag = true;
            }).catch((error) => {

          });
        }

      }
    },
  }
</script>
