# PL/SQL Developer常用技巧

## 1.类SQL PLUS窗口
File->New->Command Window，这个类似于oracle的客户端工具sql plus，但比它好用

## 2.关键字自动大写
Tools->Preferences->Editor：将Keyword case选择Uppercase。这样在窗口中输入sql语句时，关键字会自动大写，而其它都是小写。这样阅读代码比较容易，且保持良好得编码风格;

同理，在Tools->Preferences->Code Assistant：里可以设置代码提示延迟时间、输入几个字符时提示、数据库对象的大写、小写，首字母大写等。	

## 3.查看执行计划
选中需要分析的SQL语句，然后点击工具栏的Explain plan按钮(即执行计划)，或者直接按F5；这个主要用于分析SQL语句执行效率，分析表的结构，便于为sql调优提供直观依据；

## 4.自动替换
Tools–>Preferences–>Editor–>AutoReplace–>Edit：快捷输入SQL语句，例如输入s，按下空格，自动替换成SELECT；再例如，输入sf，按下空格，自动替换成SELECT * FROM，非常方便，节省了大量的时间去编写重复的SQL语句。

1)、建立shortcuts.txt，并写入如下内容，并复制到安装路径下的PlugIns目录：
	
	i=INSERT
	u=UPDATE
	s=SELECT
	f=FROM
	w=WHERE
	o=ORDER BY
	d=DELETE
	df=DELETE FROM
	sf=SELECT * FROM
	sc=SELECT COUNT(*) FROM
	sfu=SELECT * FROM FOR UPDATE
	cor=CREATE OR REPLACE
	p=PROCEDURE
	fn=FUNCTION
	t=TIGGER
	v=VIEW
	
2)、在AutoReplace选中Enable复选框，浏览文件选中shortcuts.txt，并点击Apply。
	
3)、重启PL/SQL Developer，在sql窗口中输入s+空格，sc+空格做测试。
	
>>注意：shortcuts.txt不可删除掉，否则快捷键无法用

## 5.执行单条/选中语句:
选中需要执行的语句或者单行语句所在的行，按F8键。