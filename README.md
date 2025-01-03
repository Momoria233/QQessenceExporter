# QQessenceExporter——QQ群精华消息提取器

一个qq群的精华消息提取器，可以将群内精华消息的发送人头像，内容，时间以及设置精华消息的管理员提取出来，方便查看。

## 请在line12填写自己的cookie！否则无法使用！

cookie获取方法：进入qun.qq.com的网页下打开浏览器console，输入document.cookie

不过其实在啥要登陆qq的网页下都能获取到

### 根据需求不同请自行修改line103-113的部分！详细教程请见注释

该项目url的部分灵感来源于：User-Time/requests_qq_essence

默认将所有精华消息存入一个名为es_history+当前时间.xlsx的文件中

在终端运行python main.py即可