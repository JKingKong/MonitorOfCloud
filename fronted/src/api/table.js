import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/exception_info/list',
    method: 'get',
    params
  })
}
