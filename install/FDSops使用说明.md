#使用说明
##1.1上传图片接口
###手动测试方式：
- 测试地址 http://fdsops.fastersoft.com.cn/api/upload/image/
- 测试流程：
  - 注册用户： 
	 - 使用地址http://fdsops.fastersoft.com.cn/codes/，填写邮箱地址，根据邮件获取code
	 ![avatar](https://media.fastersoft.com.cn/group1/M00/00/00/wKgBelwjC8KAQ9bHAAAyFDccYUQ2031539)
	 - 使用地址：http://fdsops.fastersoft.com.cn/users/，填写用户信息注册新用户。
	 ![avatar](https://media.fastersoft.com.cn/group1/M00/00/00/wKgBe1wjA2OAS4g6AACE5lN2q0k2401202)
  - 登陆用户：
	 - 登陆用户：创建成功后，使用页面右上角Login 登陆
	 ![avatar](http://media.fastersoft.com.cn/group1/M00/00/00/wKgBe1wjA9iAAFjaAACPrydp3Co7687590)
  - 上传图片：
 	 - 域名地址：http://fdsops.fastersoft.com.cn/api/upload/image/
 	 - 选择图片文件：
 	 ![avatar](http://media.fastersoft.com.cn/group1/M00/00/00/wKgBelwjDbiAVXf6AABa1DQ1gG80671736)
 - 参数说明：
	```json
	{
	HTTP 201 Created
	Allow: POST, OPTIONS
	Content-Type: application/json
	Vary: Accept

	{
    "id": 7,
    "name": "选择图片文件.png",
    "creat_time": "2018-12-26 13:12",
    "image_url": "group1/M00/00/00/wKgBelwjDbiAVXf6AABa1DQ1gG80671736",
    "file": null,
    "space": "",
    "file_desc": ""
}
}
```
| 名称         | 说明                   |
| ------------ | ---------------------- |
| HTTP       | 上传状态               |
| Allow		  | 允许的方法					|
| id			  | id						|
| name         | 上传图片名称           |
| image_url    | 上传服务器文件位置          |
| fds_path     | 图片真实路径（暂为null） |
| space	    | 空间名称（可用来做项目分类） |
| file_desc   | 文件备注         			|

### 接口测试方法：
 - 获取用户jwt的token值（前提是已经注册用户，请参考手动测试的注册用户）
 - 请求地址：http://fdsops.fastersoft.com.cn/login/
 - post输入用户名密码,返回的是jwt的token值
	![avatar](http://media.fastersoft.com.cn/group1/M00/00/00/wKgBelwjDbiAVXf6AABa1DQ1gG80671736)
 - 参数说明：
 
	```json

	{
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept
}
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Inlhbmd6aHVvaHVhIiwiZXhwIjoxNTQ2NDA2ODc5LCJlbWFpbCI6Inlhbmd6aHVvaHVhQGZhc3RlcnNvZnQuY29tLmNuIn0.oekpz_XwIiSFZSbpeEgVcraP4yXRHXtHbS7aBpzZzD4"
}
	```
	```
| 名称         | 说明                   |
| ------------ | ---------------------- |
| HTTP       | 上传状态               |
| Allow		  | 允许的方法					|
| token		|	token值					|
    ```
- 根据token值去调用上传图片
 - 上传接口地址：http://fdsops.fastersoft.com.cn/api/upload/image/
 - 传入参数：1、http协议的Headers(Authorization)，Body(fds_path,space, file_desc)
 
   | 名称         | 说明                   |
   | ------------ | ---------------------- |
   | Authorization | 传入jwt 的认证token（必填）格式：JWT $token   |
   | fds_path		  | 传入图片文件（必填）	|
   |space		|	项目名称（选填）	|
	|file_desc|文件备注（选填）|
 - Headers信息参考截图
	![avatar](http://media.fastersoft.com.cn/group1/M00/00/00/wKgBelwjGeGAVDpBAACH7QgstWw8374719)
 - Body信息参考截图
	![avatar](http://media.fastersoft.com.cn/group1/M00/00/00/wKgBelwjGi6AKxraAADehSzEsCI4222697)
  - 返回参数说明
  与手动上传参数一致，可以参考。
  
  ## 1.2显示上传图片
  ### 图片列表接口
  - 接口地址：http://fdsops.fastersoft.com.cn/list/images/
  - 传入参数说明：
  
| 名称         | 说明                   |
| ------------ | ---------------------- |
|page|	页码|
|page_size|	一页显示多少数据|
|id	|图片id|
|name	|图片名称|
|fds_path|	上传图片位置|
|space	|项目名称|
|user	|用户id|
|search	|搜索|
|ordering	|排序|

  - 返回参数说明：
  
  	```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
{
    "count": 12,
    "next": "http://fdsops.fastersoft.com.cn/list/images/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "IMG_0265.JPG",
            "fds_path": "http://media.fastersoft.com.cn/group1/M00/00/00/wKgBe1wfot-ADk-HAAFw8FGzBzI4324169",
            "upload_time": "2018-12-23T23:37:41.256267",
            "space": "",
            "file_desc": "",
            "user": 2
        },
        {
            "id": 2,
            "name": "IMG_0265.JPG",
            "fds_path": "http://media.fastersoft.com.cn/group1/M00/00/00/wKgBe1wfo1CAJUJ2AAFw8ClKgjM3409052",
            "upload_time": "2018-12-23T23:39:34.224989",
            "space": "",
            "file_desc": "",
            "user": 2
        }
     }
	```
	```
| 名称         | 说明                   |
| ------------ | ---------------------- |
| HTTP       | 请求状态               |
| Allow		  | 允许的方法					|
| count			  | 图片总数			|
| next         | 下一页地址           |
| results    | 结果参数          |
| id     | 图片真实路径（暂为null） |
|name|文件名称|
|fds_path|图片地址|
|upload_time|上传时间|
| space	    | 空间名称（可用来做项目分类） |
| file_desc   | 文件备注         			|
|user|上传用户id|
```
  
 ###后台管理系统地址：
  - 地址：http://fdsops.fastersoft.com.cn/xadmin/
  - 账号密码：XXXXX XXXXX
  ##更详细的文档说明，也可以参考：
 - 文档地址：http://fdsops.fastersoft.com.cn/docs/ 
 - 里面有参数说明，前端js示例代码
   ![avatar](http://media.fastersoft.com.cn/group1/M00/00/00/wKgBelwjG-qAAHhDAAX6qjTulLA8942593)

	 
  
  

  