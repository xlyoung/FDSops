              # FastDHT


# 安装前的准备
```
yum install \
vim \
git \
gcc \
gcc-c++ \
wget \
make \
automake \
autoconf \
libtool \
libdb \
libdb-devel \
libevent \
libevent-devel \
-y
```
## 安装Berkley db-6.2.23
```
cd /usr/local/src/
wget http://download.oracle.com/berkeley-db/db-6.2.23.tar.gz
tar -zxvf db-6.2.23.tar.gz
cd db-6.2.23
./dist/configure --prefix=/usr/local/db
make
make install
```
## 安装FastDHT（修改yum python 版本2.7）
```
cd /usr/local/
git clone https://github.com/happyfish100/fastdht.git
cd fastdht
#修改make.sh
vim make.sh
CFLAGS='-Wall -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE'
#改为:
CFLAGS='-Wall -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE -I/usr/local/db/include/ -L/usr/local/db/lib/'

./make.sh
./make.sh install
```

7. 配置fdht_client.conf
```
vim /etc/fdht/fdht_client.conf

#本选项关联 storaged.conf文件
keep_alive=1
base_path=/home/fastdfs/storage
#include /etc/fdht/fdht_servers.conf

ESC
:wq
```
8. 配置fdht_servers.conf（11411）
```
vim /etc/fdht/fdht_servers.conf
###必须是0开始
group_count=1
group0 = 192.168.13.49:11411
group0 = 192.168.13.50:11411

ESC
:wq
```
9. 配置fdhtd.conf
```
vim /etc/fdht/fdhtd.conf

bind_addr=192.168.1.122
port=11411
base_path=/home/fastdfs/storage
cache_size=64MB
#include /etc/fdht/fdht_servers.conf

ESC
:wq
```
10. 引入libdb.so
```
ln -s /usr/local/db/lib/libdb-6.2.so /usr/lib/libdb-6.2.so
ln -s /usr/local/db/lib/libdb-6.2.so /usr/lib64/libdb-6.2.so
```
12. 启动FastDHT
```
cp /usr/local/fastdht/init.d/fdhtd /etc/init.d/
```
13. 启动服务
```
/etc/init.d/fdhtd restart
```
14. 开机启动
```
chkconfig fdhtd on
```