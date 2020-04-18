# PostgreSQL安装(Zip版)

## 1.下载并解压
从官网（https://www.postgresql.org/）下载程序文件并解压到指定目录（如：D:\PGSQL）。

## 2.添加和设置Windows用户
### 2.1 添加用于启动PostgreSQL的Windows用户

	net user uname passswd /add /expires:never /passwordchg:no
	>> uname:用户名，一般为postgres
	>> passwd:用户密码
	
### 2.2 设置添加的用户不允许本地登录(非必须)
	
	net localgroup users uname /del
	
### 2.3 赋给用户访问PostgreSQL安装目录的权限
	
	cacls . /T /E /P uname:R
	
## 3.初始化数据目录
### 3.1 切换到创建的用户并启动CMD
	
	runas /noprofile /env /user:uname "cmd"
	
### 3.2 初始化数据库

	bin\initdb.exe -D "D:\PgSQL\data" -E UTF-8 --locale=chs -A md5 -U uname -W
	
### 3.3 启动和停止数据库
	
	启动：bin\pg_ctl -D "D:\PgSQL\data" -l logfile start
	停止：bin\pg_ctl -D "D:\PgSQL\data" stop
	
### 3.4 创建测试数据库
	
	bin\createdb testdb
	
## 4.添加为Windows服务
### 4.1 安装和卸载PostgreSQL服务
	
	安装：bin\pg_ctl register -D "D:\PgSQL\data" -N pgsql
	卸载：bin\pg_ctl unregister -N pgsql
	
### 4.2 启动和停止PostgreSQL服务
	
	启动：net start pgsql
	停止：net stop pgsql
	
## 5.PSQL基本用法
登陆后可以执行SQL语句；
### 5.1 psql登陆
	
	psql -U username -d database_name -h host -W
	>> -U 用户 -d 数据库 -h 主机 -W 数据密码


### 5.2 快捷命令
	
	\l：列举数据库，相当于mysql的show databases；
	\dt：列举表，相当于mysql的show tables
	\c dbname：切换数据库,相当于mysql的use dbname；
	\d tblname：查看表结构，相当于desc tblname；
	\di：查看索引

### 5.3 psql退出
	\q：退出psql
	
## 6.修改配置文件
postgresql默认情况下，远程访问不能成功，如果需要允许远程访问，需要修改配置文件：

### 6.1 postgresql.conf(位于data目录)
	
	port = 5432    #设置端口
	listen_addresses = 'localhost'/'*'   #*表示所有IP
	
### 6.2 pg_hba.conf(位于data目录)
	
	host all all ::1/128 password   #允许本机IPv6用户密码登陆
	host all all 0.0.0.0/32 password   #允许所有用户IPv4密码登陆
	host all all 127.0.0.1/32 password   #允许本机IPv4用户密码登陆
	
	
