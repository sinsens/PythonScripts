# 日常编写的Python代码集合
## 目录说明

python3/Database 有关数据库的脚本

### 详细说明

#### 2021-7-17
[读取文本文件并生成SQL](https://github.com/sinsens/PythonScripts/tree/master/Python3/Database/代码生成/读取文本文件并生成SQL.py)
虽然大多数 SQL 客户端管理工具可以直接导入各种各样的文本数据，不过偶尔我们也会喜欢自定义，此脚本因此而来。可以使用脚本里的 `get_insert_sql` 或 `get_update_sql` 方法生成插入/更新 SQL 语句

[ascx 模板文件代码清理工具](https://github.com/sinsens/PythonScripts/tree/master/文件处理/字段提取2.py)
之前在某公司工作时，用的 Asp.Net MVC 架构较老，业务经常变更，导致部分视图模板文件出现很多陈旧无用的注释代码，所以写了个脚本来执行清了操作。其中 `CForm`,`FormControl`,`ElementAgent`,`ElementData` 是 .NET 封装的表单生成类。

#### 2018-08-29
[python3/Database/Financius](https://github.com/sinsens/PythonScripts/tree/master/Python3/Database/Financius)
Financius是一个开源的安卓记账app，不过自身的统计功能太弱，
所以想把它导入到MySQL再进行统计分析，其中`financius.sql`是从MySQL对financius数据库的创建SQL文件。