# EXP-weibo  
微博实验版 2017课设项目  

## 描述  
移动web端微博平台  
推荐配置：Chrome for Android  
参照安卓端"微博国际版"的设计与交互  
遵循新浪微博H5版链接定义  

## 设计  
主题色 蓝 #008afe  
使用sketch重绘，全矢量图标  
全css3 transition动画  
  
## 前端  
纯手工布局，近2000行的css  
除信息编辑界面使用jQuery，其余使用Zepto.js  
使用开源组件  
[cropper](https://github.com/fengyuanchen/cropper) *定制样式  
[photoswipe](https://github.com/dimsemenov/photoswipe)  

## 后台  
支持语言python 3.4+  
框架要求aiohttp 1.0+  
依赖自建模板文件  
附加邮箱验证模块 (使用sendcloud平台服务)  

## 数据库  
数据库版本mysql 5.5  
数据表 x6, 触发器 x10  

## 部署  
架设于腾讯云主机  
运行系统ubuntu 14.04  
使用supervisor部署  
配置nginx反向代理  
开启HTTPS  
[exp.chasedreams.cn](https://exp.chasedreams.cn/)  

## 许可  
GPL v3.0  

## 最后  
感谢 [@我皓](https://github.com/smilesooo) 参与后台代码编写、与前端业务实现  
感谢 [@我健](http://weibo.com/u/1816465523) 参与前端页面布局  
感谢 [@我竞](http://weibo.com/mzjlolikon) 参与数据库设计  
系统级软件综合课程设计项目  
2017/5/25  