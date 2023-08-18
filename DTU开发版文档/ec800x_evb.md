# EC800X开发板介绍

## 支持的模组列表

- [EC800N-CN](https://python.quectel.com/products/ec800n-cn)
- [EC800M-CN](https://python.quectel.com/products/ec800m-cn)
- [EC800G-CN](https://python.quectel.com/products/ec800g-cn)

## 功能列表

### 基本概述

EC800X_QuecPython_EVB 开发板是专门针对 QuecPython 制造的、小巧便携的“口袋型”开发板。其搭载Type-C接口，开发者仅需一条USB Type-C 数据线即可轻松玩转开发板。

### 功能说明

开发板的主要组件、接口布局见下图

![](media\800X_产品功能.png)

## 资料下载

- [EC800M系列硬件设计手册（PDF）](https://images.quectel.com/python/2023/04/Quectel_EC800M-CN_QuecOpen_硬件设计手册_V1.1.pdf)
- [EC800M系列模块产品规格书（PDF）](https://images.quectel.com/python/2023/04/Quectel_EC800M-CN_LTE_Standard_模块产品规格书_V1.1.pdf)
- [EC800M系列模组封装（ZIP）](https://images.quectel.com/python/2023/05/Quectel_EC800M-CN_FootprintPart_V1.1.zip)
- [EC800M系列模组参考设计手册（PDF)](https://images.quectel.com/python/2023/05/Quectel_EC800M-CN_Reference_Design_V1.1.pdf)

## 模组资源

### 开发板接口

**J5排针管脚分配表**

| 排针 | 编号 | 名称 | 引脚  | 功能                  |
| ---- | ---- | ---- | ----- | --------------------- |
| J5   | 1    | GND  | -     | 接地                  |
| J5   | 2    | GND  | -     | 接地                  |
| J5   | 3    | RX0  | 38    | GPIO34<br />UART0_RXD |
| J5   | 4    | TX0  | 39    | GPIO35<br />UART0_TXD |
| J5   | 5    | RX1  | 28    | GPIO32                |
| J5   | 6    | TX1  | 29    | GPIO33                |
| J5   | 7    | RX2  | 17    | GPIO25<br />UART2_RXD |
| J5   | 8    | TX2  | 18    | GPIO26<br />UART2_TXD |
| J5   | 9    | SCL  | 67    | GPIO24<br />I2C0_SCL  |
| J5   | 10   | SDA  | 66    | GPIO23<br />I2C0_SDA  |
| J5   | 11   | P19  | 19    | GPIO27                |
| J5   | 12   | P20  | 20    | GPIO28                |
| J5   | 13   | P21  | 21    | GPIO29                |
| J5   | 14   | P22  | 22    | GPIO30                |
| J5   | 15   | ADC1 |       |                       |
| J5   | 16   | ADC0 | 9     | ADC0                  |
| J5   | 17   | GND  |       |                       |
| J5   | 18   | VBAT | 42/43 |                       |

**J6排针管脚分配表**

| 排针 | 编号 | 名称 | 引脚 | 功能                 |
| ---- | ---- | ---- | ---- | -------------------- |
| J6   | 1    | 5V   | -    | 5V                   |
| J6   | 2    | 3V3  | -    | 3.3V                 |
| J6   | 3    | EXT  | 24   | 接地                 |
| J6   | 4    | MISO | 33   | GPIO4<br />SPI0_MISO |
| J6   | 5    | MOSI | 32   | GPIO3<br />SPI0_MOSI |
| J6   | 6    | CS   | 31   | GPIO2<br />SPI0_CS   |
| J6   | 7    | CLK  | 30   | GPIO1<br />SPI0_CLK  |
| J6   | 8    | P23  | 23   | GPIO31               |
| J6   | 9    | IN0  | 28   | GPIO32               |
| J6   | 10   | IN1  | 87   | GPIO22               |
| J6   | 11   | IN2  | 77   | GPIO18               |
| J6   | 12   | IN4  | 83   | GPIO20               |
| J6   | 13   | IN5  | 75   |                      |
| J6   | 14   | OUT0 | 29   | GPIO33               |
| J6   | 15   | OUT1 | 86   | GPIO21               |
| J6   | 16   | OUT2 | 76   | GPIO17               |
| J6   | 17   | OUT4 | 82   | GPIO19               |
| J6   | 18   | OUT5 | 74   |                      |

**J3排针管脚分配表**

| 排针 | 编号 | 名称 | 引脚 | 功能                                |
| ---- | ---- | ---- | ---- | ----------------------------------- |
| J3   | 1    | GND  | -    | 接地                                |
| J3   | 2    | 3V3  | -    | 3.3V                                |
| J3   | 3    | CLK  | 53   | GPIO9<br />SPI1_CLK                 |
| J3   | 4    | SDA  | 50   | GPIO6<br />UART1_TX<br />SPI1_MOSI  |
| J3   | 5    | RST  | 49   | GPIO5<br />PWM3                     |
| J3   | 6    | DC   | 51   | GPIO7<br />UART1_RXD<br />SPI1_MISO |
| J3   | 7    | BLK  |      |                                     |
| J7   | 8    | CS   | 52   | GPIO8<br />SPI1_CS                  |



开发板主要管脚布局见下图

![](media/800M外设.png)

| <font color='red'>小提示</font>                              |
| ------------------------------------------------------------ |
| 开发板的更多资料，请访问 <https://python.quectel.com/download> |

### 开发板配置

开发板配备了多种传感器，以及其他外设。外设资源管脚分配表明细如下：

| 序号 | 名称                         | 型号          | 是否支持 | 接口类型 | 引脚  |
| ---- | ---------------------------- | ------------- | -------- | -------- | ----- |
| 1    | 温湿度传感器                 | AHT20         | 是       | I2C      | 66,67 |
| 2    | 光敏电阻                     | GT36528       | 是       | ADC      | 9     |
| 3    | 麦克风                       | GMI6050P-66DB | 是       | SPK      | 3,4   |
| 4    | 功放芯片                     | NS4160        | 是       | SPK      | 5,6   |
| 5    | LCD 显示屏（需选择含屏套餐） | ST7789        | 是       | SPI      | 49~53 |

## 上手准备

首先需要有一台运行有 Windows 10 以上 操作系统的电脑

- **Step1：天线安装**

安装开发板配套的天线,安装位置为LTE天线座位置,并将SIM卡插入开发板上的SIM卡座，如需使用GNSS或者BTWIFI功能，则需在对应的天线座安装天线

- **Step2：开发板连接**

使用USB Type-C数据线连接开发板的Type-C接口和电脑USB口即可完成供电

- **Step3：开发板电源设置**

开发板上USB和DC的电源选择开关拨到USB处,开发板上的PWK_ON跳帽短接AUTO(上电自动开机)

- **Step4：开发板开机**

按住PWK直至主板上电源指示灯亮（主板上丝印为POW的灯）,如果上一步短接PWK_ON则无需长按PWK自动开机
