迷宫辅助
## 说明
* 这是用于让玩家更轻松地打通凯瑞尔迷宫，从而获得卡背的辅助工具。
* [百度网盘下载](https://pan.baidu.com/s/1ff__bchLlMCYGFNYkj40OA?pwd=ydyd)
## 使用方法
1. 启动`hs_maze.exe`时，会检查炉石的日志配置文件。若提示重启，需重启游戏。
2. 右击窗口，详细阅读说明，按照提示的步骤操作。操作熟练的话，可以在30分钟内通关。
3. 使用完毕后，若不希望炉石在硬盘频繁写入数据，需自行删除日志配置文件。
## 能做但不想做
* 自动操作，免得被骂外挂。
## 已知问题但无所谓
* `Power.log`不存在时死循环。
* 使用了`PIL.Image.LANCZOS`，而非`PIL.Image.Resampling.LANCZOS`。
* 日志配置文件检查马虎，写入的版本较旧。
* 地图有少量错误。
## 鸣谢
* 与众多网友合作完成[地图](https://docs.qq.com/sheet/DUmFwSHlIRkl2WmVi?tab=5lfc46&u=231097e1ebb942d1be4a8b0f721b9803 )。
* 代码框架来自`MTGA_HOVER`和`MD_HOVER`。
* 地图数据来自[fbigame](https://hs.fbigame.com)的网页工具，有少量手动修复。
* 主角头像来自`Chadd Nervig`([@Celestalon](https://twitter.com/Celestalon ))。没经本人同意，但他肯定不会介意。
## 更新说明
* 第1版发布于`22-03-24 14:03`。
* 第2版发布于`22-03-25 17:01`。
* 第3版发布于`22-03-28 23:06`，修复断线重连后状态丢失的问题，自动判断出生点。