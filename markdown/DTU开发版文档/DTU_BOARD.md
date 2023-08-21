

# **DTU上手说明_V2.0**



## 基本概述

本文档主要基于介绍DTU上手使用说明。
### DTU简介

- 英文全称**Data Transfer Unit**，数据传输单元。是专门用于将来自于设备端MCU的串口数据通过无线通信网络传送至服务器的无线终端设备。
- 业务逻辑：传感器采集数据发送给设备端MCU，设备端MCU通过串口将采集到的数据通过DTU发送到服务器；服务器接收到数据可以进行分析、处理、显示、保存等操作。

![](media\DTU_BOARD_000.png)

### DTU功能

- **支持本地参数配置**
- **通道支持TCP、MQTT、阿里云、腾讯云、移远云多种协议和云平台**
- **支持OTA升级**
- **支持数据离线存储**
	- 在网络连接不稳定情况下，将发送失败的数据暂存至本地，在网络恢复后优先将本地数据发送至云端
  

## 使用前准备

本案例使用EC600N开发板与CP2102 USB to TTL模块进行调试

### 接线

​	![](media\DTU_BOARD_001.png)

​		1、在NANO SIM卡座中插入SIM卡；

​		2、左边从上到下依次是VCC、GND、485A、485B；（注意：电源DC 5V-24V）

​		3、右边连接好天线；



### USB转串口线连接

使用2根杜邦线分别连接485A、485B针脚，将CP2102连接至电脑的USB口。

![DTU_BOARD_002](media\DTU_BOARD_002.png)

<img src="media\DTU_BOARD_003.jpg" alt="DTU_BOARD_003" style="zoom: 33%;" />



### 2.3. 使用USB数据线连接开发板至电脑USB接口
### 2.4. 设备开机与QPYcom下载请点击以下连接查看说明

[QuecPython开发环境搭建]([快速入门 - QuecPython (quectel.com)](https://python.quectel.com/doc/Quick_start/zh/index.html))

### 2.5. 获得阿里云连接参数

用户需要在阿里云上注册账户，新建项目，注册设备名称并获得以下参数

产品名称（ProductKey）

产品秘钥（ProductSecret）：使用一型一密认证时需要提供的参数，使用一机一密时不存在此参数

设备名称（Devicename）

设备秘钥（DeviceSecret）：使用一机一密认证时需要提供的参数，使用一型一密时不存在此参数

获得阿里云ProductKey和ProductSecret

![DTU_BOARD_004](media\DTU_BOARD_004.png)

获得DeviceName

![DTU_BOARD_005](media\DTU_BOARD_005.png)

## 3. 实验操作

### 3.1 打开代码库中的DTU文件夹，按需求编写配置文件

**配置文件格式与说明如下**

```json
{
    "system_config":
    {
        "cloud": "aliyun", # 云名称：quecthing、aliyun、txyun、hwyun、tcp_private_cloud、mqtt_private_cloud
        "usr_config": false,  # 是否启用用户配置模块，本项目暂无
        "base_function":      # 基础功能配置
        {
            "logger": true,   # log打印功能是否开启
            "offline_storage": true, # 网络中断历史数据存储开启
            "fota":true,     # 固件升级是否开启
            "sota":true      # 项目脚本文件升级是否开启
        },
        "peripheral_device":{}, # 外设，本项目暂无
        "peripheral_bus":   # 外设总线
        {
            "uart":0        # 串口0
        }
    },
    "usr_config": #用户配置具体配置项
    {
    
    },
    "aliyun_config": # 阿里云配置
    {	
        "server": "gzsi5zT5fH3.iot-as-mqtt.cn-shanghai.aliyuncs.com",
        "DK": "dtu_device1",                        # 设备名称
        "PK": "gzsi5zT5fH3",                        # 产品KEY
        "DS": "173f006cab770615346978583ac430c0",   # 设备密钥
        "PS": "D07Ujh1RvKAs6KEY",                   # 产品密钥
        "burning_method": 1,                        # 0：一型一密， 1：一机一密
        "keep_alive": 300,                          # 通信之间允许的最长时间段(以秒为单位), 范围(60-1200)
        "clean_session": false,                     # 清除会话
        "qos": 1,                                   # mqtt qos（服务质量）
        "client_id": "",                            # 自定义阿里云连接id，默认为模块IMEI号
        "subscribe": {"0": "/gzsi5zT5fH3/dtu_device1/user/get"},    # 订阅Topic字典，key值代表Topic id。
        "publish": {"0": "/gzsi5zT5fH3/dtu_device1/user/update"}    # 发布Topic字典，key值代表Topic id。
    },
    "txyun_config": # 腾讯云配置
    {	
        "DK": "dtu_device1",                    
        "PK": "I81T7DUSFF",                     
        "DS": "wF+b5NwEHI53crHmOqdyQA==",       
        "PS": "",                               
        "burning_method": 1,                    
        "keep_alive": 300,                      
        "clean_session": false,
        "qos": 1,
        "client_id":"",
        "subscribe": {"0": "I81T7DUSFF/dtu_device1/control"},
        "publish": {"0": "I81T7DUSFF/dtu_device1/event"}
    },
    "hwyun_config":
    {	
        "server": "a15fbbd7ce.iot-mqtts.cn-north-4.myhuaweicloud.com",
        "port": "1883",
        "DK": "625132b420cfa22b94c54613_dtu_device1_id",
        "PK": "",
        "DS": "a306255686a71e56ad53965fc2771bf8",
        "PS": "",
        "keep_alive": 300,
        "clean_session": false,
        "qos": 1,
        "subscribe": {"0": "$oc/devices/625132b420cfa22b94c54613_dtu_device1_id/sys/messages/down"},
        "publish": {"0": "$oc/devices/625132b420cfa22b94c54613_dtu_device1_id/sys/messages/up"}
    },
    "quecthing_config":
    {	
        "server":"iot-south.quectel.com",
        "port": "1883",
        "DK": "dtudevice1",
        "PK": "p11nKG",
        "DS": "",
        "PS": "TVRBd2FPaVk2Ny85",
        "keep_alive": 300,
        "clean_session": false,
        "qos": 1
    },
    "tcp_private_cloud_config":
    {
        "ip_type":"IPv4",
        "server": "220.180.239.212",
        "port": "18011",
        "keep_alive": 5 # 设置TCP保活包间隔时间，value 单位为分钟，范围：1-120
    },
    "mqtt_private_cloud_config":
    {
        "server": "a15fbbd7ce.iot-mqtts.cn-north-4.myhuaweicloud.com",
        "port": "1883",
        "client_id": "",
        "clean_session": false,
        "qos": "0",
        "keep_alive": 300,
        "subscribe": {"0": "oc/devices/625132b420cfa22b94c54613_dtu_device1_id/sys/messages/down"},
        "publish": {"0": "oc/devices/625132b420cfa22b94c54613_dtu_device1_id/sys/messages/up"}
    },
    "uart_config":
    {
        "baudrate": "115200",   # 波特率，常用波特率都支持，如4800、9600、19200、38400、57600、115200、230400等
        "databits": "8",        # 数据位（5 ~ 8），展锐平台当前仅支持8位
        "parity": "0",          # 奇偶校验（0 – NONE，1 – EVEN，2 - ODD）
        "stopbits": "1",        # 停止位（1 ~ 2）
        "flowctl": "0",         # 硬件控制流（0 – FC_NONE， 1 – FC_HW）
        "rs485_direction_pin": "8"   #使用RS485协议时，设置控制RX/TX方向引脚
    }
}
```
**注：**
 **1. MQTT协议配置中发布Topic字典中必须有key为"0"的Topic，在向云端发送历史数据时默认使用Topic id为"0"的Topic。
 2. MQTT协议中keep_alive配置单位为秒（s），TCP协议中keep_alive配置单位为分钟（min）**

按需求编写配置文件后将配置文件保存为"dtu_config.json"，并保存至DTU代码库中的"dtu"文件。
**注：json文件保存前需要移除注释**

### 3.2 下载代码到设备

#### 3.2.1 接上数据线，连接至电脑，短按开发板上的"PWK"按键启动设备，并在QPYcom上选择USB串行设备口连接

![DTU_BOARD_0057](E:\QuecPython网站搬移\开发板使用介绍\zh\media\DTU_BOARD_008.png)

#### 3.2.2 切换到下载选项卡，点击创建项目，并输入任意项目名称

![DTU_BOARD_007](media\DTU_BOARD_007.png)

#### 3.2.3 将代码包"dtu"文件夹内所有文件一键导入QPYcom

![DTU_BOARD_009](media\DTU_BOARD_009.png)



#### 3.2.4 单击箭头，选择"下载脚本"，并等待下载完成

![DTU_BOARD_0010](media\DTU_BOARD_0010.png)

#### 3.2.5 切换至"文件"选项卡，在右边选中"dtu.py"，点击运行按钮，即可开始dtu调试运行，如果需要上电自动运行，只需要将"dtu.py"更名为"main.py"即可实现上电自动运行

![DTU_BOARD_0011](media\DTU_BOARD_0011.png)

DTU运行成功，下面为读取的配置文件。

![DTU_BOARD_0012](media\DTU_BOARD_0012.png)

### 3.3 向云端发送消息

#### 3.3.1 打开串口调试工具，选择CP210X USB to UART 连接至CP2102转换板，并打开串口

![DTU_BOARD_0015](media\DTU_BOARD_0015.png)

#### 3.3.2 在uart调试工具中按指定格式传入topic_id, msg_length, msg, 需要发送的数据，并点击"发送";

![DTU_BOARD_0014](media\DTU_BOARD_0014.png)

#### 3.3.3 DTU收到数据，并发送至云端

#### 3.3.4 云端接收到的消息

![DTU_BOARD_0016](media\DTU_BOARD_0016.png)

### 3.4 云端向设备发送信息

#### 3.4.1 在阿里云topic列表中向自定义topic发送消息

![DTU_BOARD_0017](media\DTU_BOARD_0017.png)

#### 3.4.2 DTU成功收到消息并向串口透传数据

![DTU_BOARD_0013](media\DTU_BOARD_0013.png)

#### 3.4.3 串口收到透传消息

![DTU_BOARD_0018](media\DTU_BOARD_0018.png)

## 4 .报文格式
### 4.1 与MCU通信报文
针对和云端通信协议的不同，模块和外部设备（如MCU）通信协议也会不同。
当模块和云端通信使用TCP协议时，由于TCP和串口都是数据流的形式，所以直接透传数据，不做任何处理；当模块和云端通信使用MQTT协议时，
为了区分不同的数据帧，模块的串口对外协议采用简单的数据帧：`<topic_id>,<msg_len>,<msg_data>"`。
**注：移远云不支持Topic设置，`<topic_id>`统一为`"0"`**

**示例报文：**

- 上行报文：

`“1,6,abcedf”`

- 下行报文：

`“1,6,ijklmn”`

模块和外部设备（MCU）上行报文和下行报文都是采用字符串格式，数据项之间采用逗号（`,`）相隔。


### 4.2 与云端通信报文

DTU与云端通信报文使用字符串格式



 









# **DTU GUI工具使用说明**




## 1.基本概述

本文档主要介绍DTU GUI工具的使用。

DTU GUI工具现阶段主要为客户开发调试使用，DTU GUI工具提供基础的查询与设置功能，以及模拟MCU测试和DTU模块数据收发，用户可使用USB to TTL模块连接PC与DTU。

DTU GUI基于wxPython开发，现阶段已编译的dtu_gui.exe仅支持Windows系统，
用户在Linux/macOS配置Python环境并安装wxPython lib后可直接运行dtu_gui.py或自行编译对应版本的exe程序。

## 2. 运行DTU GUI 工具

**双击DTU GUI启动工具，打开串口**

![DTU_GUI_001](media\DTU_GUI_001.png)

****

## 3. DTU GUI 功能介绍

## 3.1 工具箱

**目前工具箱的功能如下：**

| **按键名**                 | **功能**                                                     |
| -------------------------- | ------------------------------------------------------------ |
| **获取当前参数**           | 获取DTU当前配置参数，并跳转到`参数配置`界面中显示具体参数    |
| **保存所有设置参数并重启** | 将当前`参数配置`界面中配置参数写入DTU，并重启DTU             |
| **恢复出厂参数设置并重启** | 删除所有配置参数，恢复出厂参数，并重启DTU                    |
| **查询IMEI号**             | 获取DTU模组IMEI号                                            |
| **查询本机号码**           | 获取DTU中SIM卡手机号码                                       |
| **查询信号强度**           | 获取csq信号强度，信号强度值范围0 ~ 31，值越大表示信号强度越好 |
| **设备重启**               | 重启DTU设备                                                  |

### 3.1.1 查询IMEI号：

- 查询IMEI号：

![DTU_GUI_002](media\DTU_GUI_002.png)

在左侧串口数据显示框中以字符串格式显示出详细的串口数据，右侧命令消息框显示出查询获得的IMEI号。

### 3.1.1 获取DTU当前配置参数：

点击`【获取当前参数】`按钮后，立即跳到参数配置界面。

![DTU_GUI_003](media\DTU_GUI_003.png)

![DTU_GUI_004](media\DTU_GUI_004.png)

## 3.3 导入配置参数

读取当前配置参数后，进入参数配置界面，可以根据实际需求修改配置（也可以不读取，直接填写配置）。

### 3.3.1基本参数配置

![DTU_GUI_005](media\DTU_GUI_005.png)
基本配置参数项如上图

| **参数名**     | **含义**                                                     |
| -------------- | ------------------------------------------------------------ |
| 云平台通道类型 | 云平台选择，可选项：`阿里云`、`腾讯云`、`华为云`、`移远云`、`TCP私有云`、`MQTT私有云` |
| 固件升级       | 是否开启固件OTA升级                                          |
| 脚本升级       | 是否开启项目脚本OTA升级                                      |
| 历史数据存储   | 当通信异常，DTU无法向云端发送数据时，将发送数据保存，待通信恢复正常后重新发送 |
| 串口号         | 外部MCU连接DTU串口号，可选项：`0`，`1`，`2`                  |
| 波特率         | 串口波特率                                                   |
| 数据位         | 奇偶校验                                                     |
| 停止位         | 停止位长度，可选项：`1`，`2`                                 |
| 流控           | 硬件控制流，可选项：`FC_NONE`，`FC_HW`                       |

| 控制485通信方向Pin | 串口发送数据之前和之后进行拉高拉低指定GPIO，用来指示485通信的方向。如`1`、 `2`代表`UART.GPIO1`、`UART.GPIO2`。

### 3.3.2 云参数配置

云参数配置项会根据基本`云平台通信类型`选择值变化。当`云平台通信类型`为阿里云时，云参数配置项如下：

![DTU_GUI_006](media\DTU_GUI_006.png)

## 3.4 数据发送框的格式要求

数据发送的格式与MCU和DTU通信格式一致。针对和云端通信协议的不同，模块和外部设备（如MCU）通信协议也会不同。当模块和云端通信使用TCP协议时，由于TCP和串口都是数据流的形式，所以直接透传数据，不做任何处理；当模块和云端通信使用MQTT协议时，为了区分不同的数据帧，模块的串口对外协议采用简单的数据帧：
`<topic_id>,<msg_len>,<msg_data>"`。
**注：移远云不支持Topic设置，`<topic_id>`统一为`"0"`**

**示例报文：**

- 上行报文：

`“1,6,abcedf”`

- 下行报文：

`“1,6,ijklmn”`

模块和外部设备（MCU）上行报文和下行报文都是采用字符串格式，数据项之间采用`,`相隔。

![DTU_GUI_007](media\DTU_GUI_007.png)



# **DTU 实验演示结果**



### 实验结果_aliyun_1

![实验结果_aliyun_1](media\实验结果_aliyun_1.jpg)



### 实验结果_aliyun_2

![实验结果_aliyun_2](media\实验结果_aliyun_2.jpg)



### 实验结果_MQTT私有云

![实验结果_MQTT私有云](media\实验结果_MQTT私有云.jpg)



### 实验结果_TCP私有云

![实验结果_TCP私有云](media\实验结果_TCP私有云.jpg)



### 实验结果_txyun_1

![实验结果_txyun_1](media\实验结果_txyun_1.jpg)



### 实验结果_txyun_2

![实验结果_txyun_2](media\实验结果_txyun_2.jpg)