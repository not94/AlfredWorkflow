# kroki 解码小工具

由于[Notion](https://www.notion.so/) 目前还不支持PlantUML等形式的图表，因此在[Reddit](https://www.reddit.com/r/Notion/comments/jk4sd4/embedded_diagram_hack_with_kroki/) 上有人提出了通过[kroki](https://kroki.io/) + Notion Embed的方法展示图表。
Kroki会将编写图表的代码通过base64编码存储于url后缀之中，这意味着当持有url时：
- 直接打开url在浏览器中能够直接展示图表
- 对url后缀进行解码能够得到编写图表的代码

本工具主要用于后者对url进行解码，使用场景比如对已有的图表链接进行部分调整。

## 使用手册
Alfred快捷键为kde + 完整的图表url，之后拿到的图表编码会自动复制到粘贴板之中。