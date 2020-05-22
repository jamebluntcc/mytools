# mytools
useful utils functions for python&amp;js for web development

## javascript

- ajaxSend 封装 jquery 底层 $.ajax;

- createTable & createTable2 根据传入数据headData, bodyData (js array ) 生成 table;

- 增加 django crsf token 保护;

- 添加 modal 控件;


## python

- isNumber 对传入字符串进行是否为数字判断;

- redis2redis2dict 接收 `redis` 的哈希字符串为参数，解析成 `python` 的字典数据类型;

- transtime 实现时间字符串与时间戳的相互转换;

- logger 定义简单的处理日志的方法;

- 添加多线程多进程使用方法;

- 添加基于 `redis` 的缓存方法;

- 添加异步获取url方法

## sh

- 设置了 `aws` 服务器 vpn 的搭建,最后需要在 `ec2` 控制台安全组设置入站与出站流量;

- 配置文件 `centos` 安装 `mongodb`;


## web

- 一个 demo 用于测试 `datatable`的分页服务;


## changelog

- 2020-05-22 (添加基于 `redis` 的缓存方法以及一个基于 `flask-sqlalchemy` 分页的 `datatable` 封装工场类;)
- 2019-04-24 (添加数据上传包含文件以及其他信息的post传递;)
