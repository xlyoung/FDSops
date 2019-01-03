安装MySQL5.7.*
1.安装mysql源


$ yum localinstall  http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm

2.安装mysql


$ yum install mysql-community-server

确认一下mysql的版本，有时可能会提示mysql5.6
3.安装mysql的开发包，以后会有用


$ yum install mysql-community-devel

4.启动mysql


$ service mysqld start

Redirecting to /bin/systemctl start  mysqld.service
5.查看mysql启动状态


$ service mysqld status

出现pid
证明启动成功

6.获取mysql默认生成的密码

1
$ grep 'temporary password' /var/log/mysqld.log

2015-12-05T05:41:09.104758Z 1 [Note] A temporary password is generated for root@localhost: %G1Rgns!dD!v
加粗的就是生成的密码
7.换成自己的密码

1
$ mysql -uroot -p

Enter password:输入上面的密码
成功输入后进入一下步，这里你估计会输入 好几次才进去

8. 更换密码


mysql>  ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';

这个密码一定要足够复杂，不然会不让你改，提示密码不合法;
9.退出mysql;


mysql> quit;

10.用新密码再登录，试一下新密码


$ mysql -uroot -p

Enter password:输入你的新密码
11.确认密码正确后，退出mysql;


mysql> quit;

创建一个img数据库