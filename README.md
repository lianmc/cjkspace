## 2007-8-26
**cjkspace** 是编写**LaTeX**文档辅助工具，在中英文之间插入波纹号(~)，也可以是其他符号如空白或问号等。中英文之间空白的讨论可以参考**李果正**先生的博文：中英文字间空白。虽然这里说的是中英文，但程序中汉字的定义使用的是Unicode的 CJK 字符集，因此应该也支持日文和韩文。程序对中英文的定义都可以重新定义或扩展，如对德文或法文的支持等。cjkspace使用的是**Python**的内置编码器，支持大部分的文字编码，如gbk、gb18030、big5等，不指明的话，使用utf8，可以使用`cjkspace -l`查询已知编码。

程序在插入间隔符前，将删除中英文之间的所有空格。在多文件输入时，输出文件名由程序自动在原文件名后加.out后缀，若此时使用`-o`指定输出文件名，程序将予以警告，不会出错。