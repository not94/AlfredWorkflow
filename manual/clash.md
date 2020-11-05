# clash VPN 自动切换脚本

在使用该Workflow之前请先确保：

1. 已经安装了ClashX Mac版本
2. 确保配置中已经开启了 [RESTful API](https://clash.gitbook.io/doc/restful-api) 的端口，默认端口为9090
3. 确保系统中存在/usr/local/bin/python3，且Python版本需大于3.7

## 使用手册
alfred快捷键为cx，其中后续命令空格键可省略。

1. 模式切换
- 切换为全局代理 cx global -> cxg
- 切换为规则代理 cx rule -> cxr

需要注意的是默认的代理名称为BosLife，需要改变名称的同学可自行配置workflow中相关变量
2. 自动寻找最快代理 
- cx rule -> cxr

如果当前模式为全局代理，则遍历全局代理中所有的节点，找到最快的节点并切换该节点，否则则遍历指定的代理配置执行相同的操作

### 相关变量配置

| Variable | Default | Comment |
| ---------------|----------------|---------------|
| BASE_URL | http://127.0.0.1:9090 | 本地启动clash之后提供Restful API的端口 |
| delay_test_timeout |1000|延迟测试超时时间|
| delay_test_url |http://cp.cloudflare.com/generate_204|延迟测试url|
| proxy_name |BosLife|代理策略组名称|


## 截图演示
![演示](https://blog-1252269821.cos.ap-shanghai.myqcloud.com/WX20201107-230943%402x.png)

## Q & A
1. ClashX里面已经有切换的快捷键了，实现的必要性？
ClashX里面的快捷键切换并不是监听全局键盘事件，也就是说你得先选中ClashX图标才能使用快捷键，这在头部栏隐藏的时候就不是很方便，而alfred可以随时唤醒。
2. ClashX里面有定时自动寻找最快节点的模式，实现的必要性？
频繁的切换节点容易导致IP地址被封，我还是比较喜欢自己手动切换多一点。