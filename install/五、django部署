Python2.7安装

wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
tar zxf Python-2.7.13.tgz
cd Python-2.7.13
./configure
make && make install

默认 Python 2.7.13 会安装在 /usr/local/bin 目录下。
ll -tr /usr/local/bin/python*

更新系统默认 Python 版本
先把系统默认的旧版 Python 重命名。
mv /usr/bin/python /usr/bin/python.old

再删除系统默认的 python-config 软链接。
rm -f /usr/bin/python-config

最后创建新版本的 Python 软链接。
ln -s /usr/local/bin/python /usr/bin/python
ln -s /usr/local/bin/python-config /usr/bin/python-config
ln -s /usr/local/include/python2.7/ /usr/include/python2.7

以上步骤做完以后，目录 /usr/bin 下的 Python 应该是
ll -tr /usr/bin/python*


查看新的 Python 版本

python --version

返回 Python 2.7.13 为正常。
升级 Python 可能会导致 yum 命令不可用。解决方法如下：
编辑 /usr/bin/yum 文件，将开头第一行的
#!/usr/bin/python
改为
#!/usr/bin/python2.6

为新版 Python 安装 setuptools

wget https://bootstrap.pypa.io/ez_setup.py -O - | python

setuptools 正确安装完成后，easy_install 命令就会被安装在 /usr/local/bin 目录下了。
为新版 Python 安装 pip

easy_install pip

正确安装完成后，pip 命令就会被安装在 /usr/local/bin 目录下了。
为新版 Python 安装 distribute 包（可选）

pip install distribute

至此，新版 Python 即算安装完毕了


首先安装epel扩展源：
　　yum -y install epel-release
　　更新完成之后，就可安装pip：
　　yum -y install python-pip python-devel uwsgi mysql-devel  libcurl-devel
Django 安装
vi  requirements.txt

Django==1.11.14
fdfs-client-py==1.2.6
filetype==1.0.1
image==1.5.24
MySQL-python==1.2.5
Pillow==5.2.0
pytz==2018.5
qrcode==6.0
six==1.11.0
uWSGI==2.0.17.1

pip install --upgrade setuptools
pip install -r requirements.txt

上传代码上服务器


cd /home
unzip nginx_script.zip
mv nginx_script  media_server
cd media_server
#修改下面红色字体
vi upload_uwsgi.ini
chdir           = /home/media_server/
daemonize = /home/media_server/uwsgi9000.log

修改django的settings.py,修改红色部分

ALLOWED_HOSTS = ['*’]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'img_handle',
]








DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'img',
        'USER':'root',
        'PASSWORD':'1qa2ws#ED',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}


APPEND_SLASH=False

生成数据库文件，同步数据库

python manage.py migrate
 python manage.py makemigrations img_handle
python manage.py sqlmigrate img_handle 0001

启动命令
python manage.py runserver 0.0.0.0:9000


uwsgi 搭建

cd /home/uploadmodule

vi upload_uwsgi.ini
[uwsgi]

# Django-related settings

socket = :9000

# the base directory (full path)
chdir           = /home/uploadmodule/

# Django s wsgi file
module          = uploadmodule.wsgi

# process-related settings
# master
master          = true

# maximum number of worker processes
processes       = 4

# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true

#plugins = python

py-autoreload = 1
pidfile = /var/run/uwsgi9000.pid
daemonize = /home/uploadmodule/uwsgi9000.log


启动命令
uwsgi --ini /home/media_server/upload_uwsgi.ini &













