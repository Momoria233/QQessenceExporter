# QQessenceExporter——QQ群精华消息提取器

一个qq群的精华消息提取器，可以将群内精华消息的发送人头像，内容，时间以及设置精华消息的管理员提取出来，方便查看。

### 关于cookie:

本项目需要用户在脚本中填写自己的cookie

若未填写则会输出Please enter your cookie in the script.

### cookie 获取方法：

进入qun.qq.com的网页下打开浏览器console，输入document.cookie

（或者其他需要登陆qq的地方也可以）

### 根据需求不同请自行修改data_list.append的部分！详细教程请见注释

该项目url的部分灵感来源于：User-Time/requests_qq_essence

默认将所有精华消息存入一个名为es_history+当前时间.xlsx的文件中

在终端运行python main.py即可