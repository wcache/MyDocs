# 《QuecPython串口通信二次开发》





```text
1、未来先生需求： OTA升级，mcu固件升级流程中，新增传输文件前握手阶段。
解决方案：间隔200ms，最多重发10次。模组发送b"+++++"，只要接收到一次来自mcu的响应b"+++++"，就算握手成功，继续后续文件传输流程。待客户与其硬件合作商沟通后反馈。
仓库链接：https://github.com/wcache/DTU_solution_with_ota.git

2、QuecPython包管理器
初版github仓库地址：https://github.com/wcache/package_cmd.git

3、简单版本DTU框架：SimpleDTU
仓库链接：https://github.com/wcache/SimpleDTU.git

4、洗衣机控制器(pending)
```

