# Git&GitHub使用帮助
## 1、启动Git Bash
![start](/img/a100001.jpg)

## 2、创建SSH Key
	$ ssh-keygen -t rsa -C "email@email.com"

## 3、查看创建的SSH Key
    GitGUI -> Help -> Show SSH Key

## 4、将SSH Key配置到GitHub的SSH keys中
	GitHub(Web) -> Login -> SSH Keys -> New SSH Key

## 5、测试连接是否成功
	$ ssh -T git@github.com
	--- You've successfully authenticated...  表示已成功连上github。

## 6、设置username和email
	$ git config --global user.name "username"
	$ git config --global user.email "email@email.com"

## 7、切换工作目录
	$ cd E:/Projects/Git/test

## 8、配置远程地址
	$ git remote    列出所有远程主机
	$ git remote -v		参看远程主机的网址
	$ git remote show origin	查看"origin"主机的详细信息
	#添加origin主机并设置URL
	$ git remote add origin git@github.com:sone92cn/test.git   	
	#设置origin主机URL
	$ git remote set-url origin https://github.com/test/test.git
	$ git remote rename origin origin_new   修改远程主机名
	$ git remote rm origin	删除远程主机origin
	--- git remote rename <原主机名> <新主机名>

## 9、创建本地仓库
	$ git init <dirname>
	$ git clone https://github.com/sone92cn/test.git    HTTPS协议
	$ git clone git@github.com:sone92cn/test.git  	HHS协议，通常速度更安全
	--- git clone <版本库的网址> <本地目录名>

## 10、添加文件(修改)到Git本地仓库
	$ git add ./file/dir		添加新文件/修改的文件到本地仓库
	$ git commit -m "Comment Text"		应用更新
	#修改而未添加新文件时，可以用本命令代替以上两条命令
	$ git commit -am "Comment Text"  	

## 11、取回项目文件
	$ git fetch <远程主机名>  	将某个远程主机的更新，全部取回本地
	$ git fetch <远程主机名> <分支名>	取回特定分支的更新
	$ git merge <远程主机名>/<分支名>	将获取的分支更新与本地分支合并
	$ git pull	通过clone创建（唯一追踪）的项目，可以省略后面的参数
	#取回远程分支的更新，并与本地分支合并
	$ git pull <远程主机名> <远程分支名>:<本地分支名>
	#远程分支与当前分支合并，省略冒号后内容
	$ git pull <远程主机名> <远程分支名>
	--- fetch: 仅获取远程更新，不更改本地项目文件
	--- pull: 获取远程更新，并与本地分支核对。即先fetch，然后再merge。

## 12、提交更新到服务器
	$ git push 		通过clone创建（唯一追踪）的项目，可以省略后面的参数
	$ git push origin master	提交本地master分支到远程同名分支
	$ git push origin master:test   创建服务器分支test，并提交代码
	$ git push origin :test		删除远程分支test
	--- git push <远程主机名> <本地分支名>:<远程分支名>  

## 13、分支
	$ git branch <分支名>	从当前分支创建新的分支，但不选择
	$ git checkout <分支名>		选择已经创建的分支
	$ git checkout -b <分支名>	从当前分支新建分支并切换到改分支
	$ git merge <分支名>	将制定的分支合并到当前分支
	$ git branch -r 	查看远程的分支名
	$ git branch -a		查看所有的分支名
	$ git checkout -b <本地分支> <主机名>/<远程分支名>	用远程分支创建本地分支
	$ git branch -d <BranchName>	删除本地分支
	$ git push origin --delete <BranchName>		删除远程分支

## 14、追踪
	#创建分支并设置追踪，分支未创建
	$ git branch <分支名> --track origin/master		
	#手动设置追踪，分支已创建
	$ git branch <分支名> --set-upstream-to origin/master

## 15、删除本地分支
	$ git branch -d <BranchName>

## 16、合并分支到master
	$ git checkout master   切换到master分支
	$ git pull origin master   pull远程master上的代码
	$ git merge dev    把dev分支的代码合并到master上
