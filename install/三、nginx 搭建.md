## 安装需求包
```
yum -y install make zlib zlib-devel gcc-c++ libtool openssl openssl-devel gd-devel wget zip unzip
```
## pcre安装
- 下载压缩包
```
wget https://jaist.dl.sourceforge.net/project/pcre/pcre/8.42/pcre-8.42.tar.gz -O /usr/local/src/pcre-8.42.tar.gz
```
- pcre安装
```
cd /usr/local/src
tar -zxf pcre-8.42.tar.gz
cd pcre-8.42
./configure --prefix=/usr/local/pcre
make
make install
```
- 安装FastDFS与nginx 模块(由于有版本冲突，请使用附件里的)
```
cd /usr/local/src
git clone https://github.com/happyfish100/fastdfs-nginx-module.git
cd fastdfs-nginx-module/
cp src/mod_fastdfs.conf /etc/fdfs/
```
- 修改fastdfs-nginx-conf 配置，防止nginx编译失败
```
cd /usr/local/src/
vi fastdfs-nginx-module/src/config 
```
修改成一下内容
```
ngx_module_incs="/usr/include/fastdfs /usr/include/fastcommon/"
CORE_INCS="$CORE_INCS /usr/include/fastdfs /usr/include/fastcommon/"
```


- 修改mod_fastdfs.conf 
```
vi /etc/fdfs/mod_fastdfs.conf 
```
```
# 连接超时时间
connect_timeout=10

# Tracker Server
tracker_server=192.168.13.49:22122
tracker_server=192.168.13.50:22122

# StorageServer 默认端口
storage_server_port=23000

# 如果文件ID的uri中包含/group**，则要设置为true
url_have_group_name = true

# Storage 配置的store_path0路径，必须和storage.conf中的一致
store_path0=/home/fastdfs/storage
```

- 安装nix_cache_purge,做缓冲使用
```
cd /usr/local/src
git clone https://github.com/FRiCKLE/ngx_cache_purge.git
```

- 下载nginx
```
wget http://nginx.org/download/nginx-1.15.6.tar.gz -O /usr/local/src/nginx-1.15.6.tar.gz
tar -zxf nginx-1.15.6.tar.gz
```
- 复制图片水印模块到nginx
```
cp ngx_http_image_filter_module.c /usr/local/src/nginx-1.15.6/src/http/modules
```
- nginx 安装 
```
cd nginx-1.15.6
./configure --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre=../pcre-8.42 --with-stream --with-http_image_filter_module --with-http_gzip_static_module  --add-module=/usr/local/src/fastdfs-nginx-module/src  --add-module=/usr/local/src/ngx_cache_purge
make
make install
```
- 修改默认配置列表，增加子配置文件和修改端口,增加日志格式
```
worker_processes  auto;
http {
      ……..
    log_format  wwwlog  '[$remote_addr] - [$remote_user] [$time_local] ["$request"] '
        '[$status] [$body_bytes_sent] ["$http_referer"] '
        '["$http_user_agent"] [$http_x_forwarded_for] ';
###包含配置文件
    include /usr/local/nginx/conf/vhost.d/*.conf;
      …..
        server {
                   listen       18080;
 ```
- 复制 FastDFS 的部分配置文件到/etc/fdfs 目录
```
cd /usr/local/src/fastdfs-5.11/conf

cp anti-steal.jpg http.conf mime.types /etc/fdfs/
```


- 配置文件编写：
```
mkdir -p /usr/local/nginx/conf/vhost.d
mkdir -p /home/nginx_acccess_log
mkdir -p /home/cache/tmp
mkdir -p /home/cache/tmp1
mkdir -p /home/image/cache/uploads_thumb
cd /usr/local/nginx/conf/vhost.d
```
- 1、配置storage.conf 访问静态文件
```
        server {
        listen       8888;
        server_name  localhost;

        #FastDFS 文件访问配置(fastdfs-nginx-module模块)
        location ~/group([0-9])/M00 {
            default_type image/png;
            ngx_fastdfs_module;
        }
        }
```
- 2、配置tracker.conf 负载均衡2个storage
```

proxy_cache_path /home/cache/tmp levels=1:2 keys_zone=http-cache:10m max_size=50G;


    server {
        listen       80;
        server_name  localhost;
        #charset koi8-r;
        access_log  /home/nginx_acccess_log/tracker.log  wwwlog;

        #设置 group 的负载均衡参数
        location /group1/M00 {
            proxy_next_upstream http_502 http_504 error timeout invalid_header;
            proxy_cache http-cache;
            proxy_cache_valid  200 304 12h;
            proxy_cache_key $uri$is_args$args;
            proxy_pass http://fdfs_group1;
            expires 30d;
        }


        #设置清除缓存的访问权限
        location ~/purge(/.*) {
            allow 127.0.0.1;
            allow 192.168.13.0/24;
            deny all;
            proxy_cache_purge http-cache $1$is_args$args;
        }
}



    #设置 group1 的服务器
    upstream fdfs_group1 {
         server 192.168.13.49:8888 weight=1 max_fails=2 fail_timeout=30s;
         server 192.168.13.49:8888 weight=1 max_fails=2 fail_timeout=30s;
    }
```
- 配置图片img.conf
```
proxy_cache_path /home/image/cache/uploads_thumb levels=1:2 keys_zone=uploads_thumb:10m max_size=50G;


server
{
    listen 9999;
    server_name  localhost;
    index index.html index.htm ;
    root /home/image;
    default_type image/png;
    expires 7d;
    gzip_static on;
    add_header Cache-Control public;
    add_header X-Pownered "nginx_image_filter";
    #HTTP Response Header 增加 proxy_cache 的命中状态，以便于以后调试，检查问题
    add_header X-Cache-Status $upstream_cache_status;
    #将缩略图缓存在服务，避免每次请求都重新生成
    proxy_cache uploads_thumb;
    #当收到 HTTP Header Pragma: no-cache 的时候，忽略 proxy_cache
    #此配置能让浏览器强制刷新的时候，忽略 proxy_cache 重新生成缩略图
    proxy_cache_bypass $http_pragma;
    #由于 Upload 文件一般都没参数的，所以至今用 host + document_uri 作为
    proxy_cache_key "$host$document_uri";
    #有效的文件，在服务器缓存 7 天
    proxy_cache_valid 200 7d;
    proxy_cache_use_stale error timeout invalid_header updating;
    proxy_cache_revalidate on;
    #处理 proxy 的 error
    proxy_intercept_errors on;
    #error_page   415 = /assets/415.png;
    #error_page   404 = /assets/404.png;




  #定义好尺寸缩略图
  location ~*group1/M00/(.*)!(large|lg|md|sm|xs)$ {
    default_type image/png;
    set $filename $1;

    if (-f $filename) {
      break;
    }

    #根据 URL 地址 ! 后面的图片版本来准备好需要的参数（宽度、高度、裁剪或缩放）
    set $img_version $2;
    set $img_type resize;
    set $img_w    -;
    set $img_h    -;
    if ($img_version = 'large') {
      set $img_type resize;
      set $img_w    1920;
    }
    if ($img_version = 'lg') {
      set $img_type crop;
      set $img_w    192;
      set $img_h    192;
    }
    if ($img_version = 'md') {
      set $img_type crop;
      set $img_w    96;
      set $img_h    96;
    }
    if ($img_version = 'sm') {
      set $img_type crop;
      set $img_w    48;
      set $img_h    48;
    }
    if ($img_version = 'xs') {
      set $img_type crop;
      set $img_w    32;
      set $img_h    32;
    }
    rewrite ^ /_$img_type;
  }


#自定义图片
  location ~*group1/M00/(.*)!(r|c)/(\d+)/(\d+)$ {
    set $filename /$1;

    if (-f $filename) {
      break;
    }

    #根据 URL 地址 ! r|c/300/400
    set $img_version $2;
    set $img_w    $3;
    set $img_h    $4;
    if ($img_version = 'r') {
      set $img_type resize;
    }
    if ($img_version = 'c') {
      set $img_type crop;
    }
    rewrite ^ /_$img_type;
  }





  #原始图片
  location /group1/M00 {
    #alias /home/image/$filename;
    alias /home/fastdfs/file/data;
    default_type image/png;
    expires 7d;
    autoindex on;
  }





  #缩放图片的处理
  location /_resize {
    alias /home/fastdfs/file/data/$filename;
    #alias /home/image$filename;
    image_filter resize $img_w $img_h;
    image_filter_jpeg_quality 95;
    image_filter_buffer         20M;
    image_filter_interlace      on;
  }

  #裁剪图片的处理
  location /_crop {
    alias /home/fastdfs/file/data/$filename;
    image_filter crop $img_w $img_h;
    image_filter_jpeg_quality 95;
    image_filter_buffer         20M;
    image_filter_interlace      on;
  }
}
```



- 对外nginx配置
```
server {
    listen 80;
    server_name media.fastersoft.com.cn;
    rewrite ^(.*)$ https://${server_name}$1 permanent;
}
server {
        listen 443 ssl http2;
        server_name media.fastersoft.com.cn;
        root /home/media;
        ssl_certificate /usr/local/nginx/ssl/media.fastersoft.com.cn.pem;
        ssl_certificate_key /usr/local/nginx/ssl/media.fastersoft.com.cn.key;
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        resolver 8.8.8.8;
        location / {
                proxy_pass              http://media_fastersoft;
                proxy_set_header        Host $host;
                proxy_set_header        X-Real-IP $remote_addr;
                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_connect_timeout   150;
                proxy_send_timeout      100;
                proxy_read_timeout      100;
                proxy_buffers           4 32k;
                client_max_body_size    500m; # Big number is we can post big commits.
                client_body_buffer_size 128k;

         }
        access_log /home/logs/media.fastersoft.log;
}

    upstream media_fastersoft {
         server 192.168.1.122:9999 weight=1 max_fails=2 fail_timeout=30s;
         server 192.168.1.123:9999 weight=1 max_fails=2 fail_timeout=30s;
    }
```