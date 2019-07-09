<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App',
    data() {
      return {
        timer: '',
      }
    },
    mounted() {
      this.timer = setInterval(this.getRealTimeWarning, 1000);   // 定时器，定时从后端获取实时异常信息
    },
    methods: {
      getRealTimeWarning() {
        console.log(this.$route.path);
        if (this.$route.path != "/warn") {
          this.$axios.get("/is_new/").then((response) => {
            if (response.data['is_new'] === 'true') {
              this.$notify({
                title: '警告',
                message: '收到一条异常警告,请及时处理',
                duration: 0,
                type: 'warning'
              });
            }

          }).catch((error) => {

          })
        }
      },
    },
    beforeDestroy() {
      clearInterval(this.timer);
    }

    // websocket方式 获取服务器端的消息推送
    // mounted() {
    //   this.connectSocket("ws://127.0.0.1:8080/realtime/");
    // },
    // methods: {
    //   connectSocket(host) {
    //     let webSocket = new WebSocket(host);
    //     /*建立连接*/
    //     webSocket.onopen = evt => {
    //       console.log("webSocket连接成功");
    //       let data = {"message": '客户端-1 的消息'};
    //       let json = JSON.stringify(data);
    //       webSocket.send(json);
    //     };
    //     /*连接关闭*/
    //     webSocket.onclose = evt => {
    //       console.log("webSocket连接关闭");
    //     };
    //     /*接收服务器推送消息*/
    //     webSocket.onmessage = evt => {
    //       let data = JSON.parse(evt.data);
    //       this.$notify({
    //         title: '警告',
    //         message: '收到一条异常警告',
    //         duration: 0,
    //         type: 'warning'
    //       });
    //       console.log(data)
    //     };
    //     /*连接发生错误时*/
    //     webSocket.onerror = (evt, e) => {
    //       console.log(evt);
    //     }
    //   }
    // }

  }
</script>
