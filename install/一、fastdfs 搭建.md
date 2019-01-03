#fastdfs服务器安装

## 先安装FastDFS

## 安装基本工具
```
yum install wget git gcc zip unzip  make cmake  gcc-c++
```

## 下载安装 libfastcommon

- 安装libfastcommon
```
cd /usr/local/src
git clone https://github.com/happyfish100/libfastcommon.git
cd libfastcommon/
./make.sh
./make.sh install
```
- 下载安装FastDFS
```
wget https://codeload.github.com/happyfish100/fastdfs/zip/V5.11
```
解压
```
unzip V5.11
cd fastdfs-5.11/
```
编译、安装
```
./make.sh
./make.sh install
```
默认安装方式安装后的相应文件与目录
　　A、服务脚本：
```
/etc/init.d/fdfs_storaged
/etc/init.d/fdfs_tracker
```
　　B、配置文件（这三个是作者给的样例配置文件） :
```
/etc/fdfs/client.conf.sample
/etc/fdfs/storage.conf.sample
/etc/fdfs/tracker.conf.sample
```
　　C、命令工具在 /usr/bin/ 目录下：
```
fdfs_appender_test
fdfs_appender_test1
fdfs_append_file
fdfs_crc32
fdfs_delete_file
fdfs_download_file
fdfs_file_info
fdfs_monitor
fdfs_storaged
fdfs_test
fdfs_test1
fdfs_trackerd
fdfs_upload_appender
fdfs_upload_file
stop.sh
restart.sh
```
建立 /usr/bin 到 /usr/local/bin 的软链接，我是用这种方式。　
```
ln -s /usr/bin/fdfs_trackerd   /usr/local/bin
ln -s /usr/bin/fdfs_storaged   /usr/local/bin
ln -s /usr/bin/stop.sh         /usr/local/bin
ln -s /usr/bin/restart.sh      /usr/local/bin
```
3、配置FastDFS跟踪器(Tracker)

配置文件详细说明参考：FastDFS 配置文件详解
① 进入 /etc/fdfs，复制 FastDFS 跟踪器样例配置文件 tracker.conf.sample，并重命名为 tracker.conf。
```
cd /etc/fdfs
cp tracker.conf.sample tracker.conf
vim tracker.conf
```
② 编辑tracker.conf ，需要修改如下，其它的默认即可。
```
# 配置文件是否不生效，false 为生效
disabled=false
# 提供服务的端口
port=22122
# Tracker 数据和日志目录地址(根目录必须存在,子目录会自动创建)
base_path=/home/fastdfs/tracker

# HTTP 服务端口
http.server_port=80
```
③ 创建tracker基础数据目录，即base_path对应的目录
```
mkdir -p /home/fastdfs/tracker
```

⑤ 启动Tracker
初次成功启动，会在/home/fastdfs/tracker(配置的base_path)下创建 data、logs 两个目录。
可以用这种方式启动
```
# /etc/init.d/fdfs_trackerd start
```
也可以用这种方式启动，前提是上面创建了软链接，后面都用这种方式
```
service fdfs_trackerd start
```
查看 FastDFS Tracker 是否已成功启动 ，22122端口正在被监听，则算是Tracker服务安装成功。
```
# netstat -unltp|grep fdfs
```
关闭Tracker命令：
```
# service fdfs_trackerd stop
```
⑥ 设置Tracker开机启动
```
chkconfig fdfs_trackerd on
```
⑦ tracker server 目录及文件结构
Tracker服务启动成功后，会在base_path下创建data、logs两个目录。目录结构如下：
${base_path}
  |__data
  |   |__storage_groups.dat：存储分组信息
  |   |__storage_servers.dat：存储服务器列表
  |__logs
  |   |__trackerd.log： tracker server 日志文件
4、配置 FastDFS 存储 (Storage)
① 进入 /etc/fdfs 目录，复制 FastDFS 存储器样例配置文件 storage.conf.sample，并重命名为 storage.conf
```
cd /etc/fdfs
cp storage.conf.sample storage.conf
```
vim storage.conf
② 编辑storage.conf
标红的需要修改，其它的默认即可。
```
# 配置文件是否不生效，false 为生效
disabled=false

# 指定此 storage server 所在 组(卷)
group_name=group1

# storage server 服务端口
port=23000

# 心跳间隔时间，单位为秒 (这里是指主动向 tracker server 发送心跳)
heart_beat_interval=30

# Storage 数据和日志目录地址(根目录必须存在，子目录会自动生成)
base_path=/home/fastdfs/storage

# 存放文件时 storage server 支持多个路径。这里配置存放文件的基路径数目，通常只配一个目录。
store_path_count=1


#检查是否配合dht，检查文件(这里是配置dht)
check_file_duplicate=1
keep_alive=1
#注意原有配置是## ，现在改成1个#号
#include /etc/fdht/fdht_servers.conf

# 逐一配置 store_path_count 个路径，索引号基于 0。
# 如果不配置 store_path0，那它就和 base_path 对应的路径一样。
store_path0=/home/fastdfs/storage

# FastDFS 存储文件时，采用了两级目录。这里配置存放文件的目录个数。
# 如果本参数只为 N（如： 256），那么 storage server 在初次运行时，会在 store_path 下自动创建 N * N 个存放文件的子目录。
subdir_count_per_path=256

# tracker_server 的列表 ，会主动连接 tracker_server
# 有多个 tracker server 时，每个 tracker server 写一行
tracker_server=192.168.1.122:22122
tracker_server=192.168.1.123:22122

#include /etc/fdht/fdht_servers.conf
# 允许系统同步的时间段 (默认是全天) 。一般用于避免高峰同步产生一些问题而设定。
sync_start_time=00:00
sync_end_time=23:59
# 访问端口
http.server_port=8888
```
增加hosts解析
```
vi /etc/hosts

172.172.172.111 tracker.com
```
③ 创建Storage基础数据目录，对应base_path目录
```
mkdir -p /home/fastdfs/storage
```
⑤ 启动 Storage
启动Storage前确保Tracker是启动的。初次启动成功，会在 /ljzsg/fastdfs/storage 目录下创建 data、 logs 两个目录

可以用这种方式启动
```
/etc/init.d/fdfs_storaged start
```
也可以用这种方式，后面都用这种
```
 service fdfs_storaged start
```
查看 Storage 是否成功启动，23000 端口正在被监听，就算 Storage 启动成功。
```
# netstat -unltp|grep fdfs
```
关闭Storage命令：
```
# service fdfs_storaged stop
```
查看Storage和Tracker是否在通信：
```
/usr/bin/fdfs_monitor /etc/fdfs/storage.conf
```
⑥ 设置 Storage 开机启动
```
# chkconfig fdfs_storaged on
```

⑦ Storage 目录
同 Tracker，Storage 启动成功后，在base_path 下创建了data、logs目录，记录着 Storage Server 的信息。
在 store_path0 目录下，创建了N*N个子目录：

5、文件上传测试

① 修改 Tracker 服务器中的客户端配置文件
```
cd /etc/fdfs
cp client.conf.sample client.conf
```
vim client.conf
修改如下配置即可，其它默认。
```
# Client 的数据和日志目录
base_path=/home/fastdfs/client

# Tracker端口
tracker_server=tracker.com:22122
```
创建文件jia
```
mkdir -p /home/fastdfs/client
```

② 上传测试
 在linux内部执行如下命令上传 namei.jpeg 图片
 ```
# /usr/bin/fdfs_upload_file /etc/fdfs/client.conf namei.jpeg
```
上传成功后返回文件ID号：group1/M00/00/00/wKgz6lnduTeAMdrcAAEoRmXZPp870.jpeg

返回的文件ID由group、存储目录、两级子目录、fileid、文件后缀名（由客户端指定，主要用于区分文件类型）拼接而成。


制作软链接
```
ln -s /home/fastdfs/storage/data /home/fastdfs/storage/data/M00
```