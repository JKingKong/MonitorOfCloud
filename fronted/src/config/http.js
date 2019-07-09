//  配置axios  首先：cnpm install axios --save
import axios from 'axios'

// 超时时间
axios.defaults.timeout = 5000

//  服务器url
// axios.defaults.baseURL = 'http://47.107.171.177'
//  本地测试url
axios.defaults.baseURL = 'http://127.0.0.1:8080'

// 带上cookie请求
axios.defaults.withCredentials = true

//  请求头
// axios.defaults.headers = {'Content-Type': 'application/x-www-check_video-urlencoded;charset=UTF-8'};

// // request拦截器
// axios.interceptors.request.use(
//   config => {
//     // 发送请求之前，要做的业务
//     return config
//   },
//   error => {
//     // 错误处理代码
//
//     return Promise.reject(error)
//   }
// );
//
// // response拦截器
// axios.interceptors.response.use(
//   response => {
//     // 数据响应之后，要做的业务
//     return response
//   },
//   error => {
//     return Promise.reject(error)
//   }
// );

export default axios
