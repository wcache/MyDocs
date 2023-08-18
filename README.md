# 韦伟的Documents

目录:

```reStructuredText
.
|-- README.md：this file
|-- images： 各种文档中嵌入的图片存放地址
|-- markdown： md文件
|-- outputs： md文件输出pdf存放目录
|-- visio：作图
|-- word：docx文件
|-- xmind：思维导图
```

------

URL类:

| 描述            | URL                                                          |
| --------------- | ------------------------------------------------------------ |
| QuecPython      | https://github.com/QuecPython                                |
| SW1P-QUECPYTHON | https://knowledge.quectel.com/display/SW1PQUECPYTHON/SW1P-QUECPYTHON |

共享盘

| 用途     | 路径                                                         |
| -------- | ------------------------------------------------------------ |
| 模块固件 | \\192.168.11.252\quectel2\Project\Module Project Files\LTE Project |



账号类:

| 类别     | 账号       | 密码              | 备注                                                         |
| :------- | ---------- | ----------------- | :----------------------------------------------------------- |
| P4       | QP         | Quecpython        | Server: 192.168.23.169:1666                                  |
| SVN      | dustin.wei | 3HWQHEhQ          | SVN服务地址：https://svn.quectel.com/svn                     |
| 亿赛通   | dustinWei  | Admin@123         | 服务器地址: 192.168.1.212<br />端口: 8888<br />亿赛通客户端存放在:  "\192.168.11.252\部门共享\IT部\免费软件安装包\研发软件\1、亿赛通" |
| pypi账号 | QuecPython | quecpython2023abc | pypi-AgEIcHlwaS5vcmcCJDVmNTJjNGQxLThkYWItNDFlOS04YWYyLWIzNTlkMjAyYjRkZQACKlszLCI5YzAzNDRkMC0wY2Y1LTQwOWQtOTY3Mi01OGFhMGMzMGE5OTEiXQAABiCeYzvYXR64ACpKS66yutF1H8bVHxXeE1XiHt2G8VcQzQ |

pip国内源

```txt
清华大学 https://pypi.tuna.tsinghua.edu.cn/simple

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

阿里云 http://mirrors.aliyun.com/pypi/simple/

豆瓣 http://pypi.douban.com/simple/

-------------------------------
一次性使用方式
pip install -i http://pypi.douban.com/simple/ SomePackage

# 提示不信任
pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com SomePackage

后面再要加参数的话就如这样：
pip install -i http://e.pypi.python.org --trusted-host e.pypi.python.org --upgrade pip #--upgrade 升级pip

```



===================临时记录====================



```text
@所有人 官网解决方案板块 资料填充下：
1. 概述：可以填充ppt每一页的截图，去除首页、末页
2. 参数：方案一些spec说明，如功耗、上先行速率、定位精度等等，任何与本方案相关的参数
3. 资料：github开源代码链接（github还没有代码的联系我）、说明文档、工具
4. FAQ：解决方案应用过程中遇到的一些问题


官网链接：http://192.168.29.126:9098/solutions

官网后台：192.168.29.126:9098/wp-login.php?loggedout=true&wp_lang=zh_CN
用户名：Brian
密码：V8*Wey(^qWdv2y3&%qSscdbJ

解决方案资料：https://knowledge.quectel.com/display/SWDOCUMENT/QuecPython

上传上的任何工具、文档等，都要填写标签，在解决方案后台编辑页面中关联了标签后，才能在前端页面显示对应的文档。

文档的名称以文案检查释放之后的版本为准；
后台页面编辑时，填充的名称不要包含版本号吧（实际上传的文件本身要带版本号）；
在专门的版本栏填充版本号；


-------作废--------
解决方案板块上传的文件的标签命名规范（不是文件名）：
解决方案推广ppt文档：solution_promotion_<solution_name>
解决方案应用指导文档：solution_app_guide_<solution_name>
解决方案工具：solution_tool_<solution_name>
如：solution_promotion_tracker、solution_app_guide_tracker、solution_tool_dtu
-------------------

IT设计与预期不符，这里的“标签命名规范”作废，板块关联关键词时，直接使用去除后缀的文件名作为关键词就OK了，多个关键词使用 英文 逗号 分隔。
```

![](./markdown/images/微信图片_20230506131032.png)

认真阅读下这个仓库的首页readme，把大家此前调试过的各类驱动都 提PR 上去
https://github.com/QuecPython/QuecPython_lib_bundles



https://github.com/QuecPython/umodbus

这个的readme.md抽空写下：
1. 协议概述
2. 接口说明
3. 应用说明









快速入门 和 应用指导 的目录结构 在 gitee 上做了调整：



1. 新建了分支：app_guide。



2. ！！！ 【wiki】 的 提交仍然在 【doc_center_v2.0】 分支。



3. ！！！ 【开发板文档】 提交到 【app_guide】 分支的 【docs\Getting_started\zh\evb】 目录下。



4. ！！！ 【应用指导文档】 提交到 【app_guide】 分支的 【docs\Application_guide\zh】 目录下。



5. 所有文档的图片统一放在对应板块的 【zh/media】 目录下。

    假如：有一个 md 文件，路径为 docs\Application_guide\zh\background\about-qpy.md，其中引用的所有图片，应放在 docs\Application_guide\zh\media\background\about-qpy 文件夹下。
    
    即：一个【md 文件】，在 media 目录中对应一个【文件夹】。
    
    图片【不要】在乱放、乱引用。



6. 大家所写的【应用指导文档】，我统一把名字改成了英文，单词之间使用【中划线】分隔，【不是】下划线。

    后续【文件命名】统一为【英文】。
    
    大家对照英文名称或文档内容，认领各自的文档。
    
    明天我也会在表格中，把 gitee 中的路径 与 表格中的标题 做对应。



7. 【应用指导文档】中引用的图片或md文件的路径，我都统一根据实际情况做了调整，大家再【check】下有没有遗漏、没修改的。



8. 【应用指导文档】最新的修改，大家对照【app_guide】 分支的内容，使用【beyond compare】比较差异后，把修改点合进去，【禁止】直接替换。

    因为引用路径都已更新，直接替换会回到老的错误版本。



9. 后续修改可以直接提交到gitee，方便我或jun查看，不用再发zip包。



希望大家能遵守这个规则 ！！！# MyDocs
